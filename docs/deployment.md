# Deployment Guide

## Prerequisites

| Requirement | Minimum |
|---|---|
| OS | Ubuntu 22.04 LTS (or Debian 12) |
| RAM | 16 GB (8B LLM model needs ~8–10 GB) |
| CPU | 4 cores |
| Disk | 40 GB free |
| Docker | 24+ with Compose v2 |
| SIP provider | VoIP.ms, Twilio SIP, Vonage, or any SIP trunk |

---

## 1. Local Setup (Development)

```bash
# Clone the repo
git clone <your-repo-url> voice-ai
cd voice-ai

# Copy and configure environment
cp .env.example .env
nano .env           # set your Supabase, Cal.com, and email keys

# Start all services
docker compose up -d

# Verify services are up
docker compose ps

# Pull the LLM (run once — downloads ~4.7 GB)
docker exec -it ollama ollama pull llama3

# (Optional) try a smaller/faster model
docker exec -it ollama ollama pull mistral
docker exec -it ollama ollama pull phi3

# Download Piper voice model into the volume
docker exec -it piper_tts \
  wget -O /data/en_US-lessac-medium.onnx \
  https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx

# Run database migrations
docker exec -it voice_db \
  psql -U postgres voiceai < /docker-entrypoint-initdb.d/schema.sql

# Confirm backend is healthy
curl http://localhost:8000/health
```

---

## 2. Test the Voice Pipeline Without a Phone

```bash
# Synthesise a test response (TTS check)
curl -X POST http://localhost:8000/calls/start \
  -d "call_id=test001&caller_number=+15551234567&called_number=+15559876543"

# Record a WAV file with your microphone (requires sox)
sox -d -r 8000 -c 1 -b 16 /tmp/test_input.wav trim 0 5

# Send it through the full pipeline
SESSION_ID="<session_id from above>"
curl -X POST http://localhost:8000/calls/speech \
  -F "session_id=$SESSION_ID" \
  -F "caller_number=+15551234567" \
  -F "audio=@/tmp/test_input.wav"

# The response JSON contains audio_path — play it
aplay $(curl ... | jq -r .audio_path)
```

---

## 3. Asterisk Configuration

### 3a. Install Asterisk (if not using Docker)

```bash
sudo apt update
sudo apt install -y asterisk asterisk-modules python3-pip
pip3 install requests asterisk-agi
```

### 3b. Configure SIP trunk (pjsip.conf)

```ini
; /etc/asterisk/pjsip.conf

[transport-udp]
type=transport
protocol=udp
bind=0.0.0.0:5060

[your-sip-trunk]
type=registration
transport=transport-udp
outbound_auth=your-sip-trunk-auth
server_uri=sip:sip.voip.ms
client_uri=sip:YOUR_ACCOUNT@sip.voip.ms
retry_interval=60

[your-sip-trunk-auth]
type=auth
auth_type=userpass
username=YOUR_ACCOUNT
password=YOUR_PASSWORD

[your-sip-trunk-aor]
type=aor
contact=sip:sip.voip.ms

[your-sip-trunk-identify]
type=identify
endpoint=your-sip-trunk
match=sip.voip.ms
```

### 3c. Copy the AGI script

```bash
sudo cp asterisk/agi/call_handler.py /var/lib/asterisk/agi-bin/
sudo chmod +x /var/lib/asterisk/agi-bin/call_handler.py

# Set BACKEND_URL in the script or as an env var
export BACKEND_URL=http://127.0.0.1:8000
```

### 3d. Copy the dialplan

```bash
sudo cp asterisk/dialplan/extensions.conf /etc/asterisk/extensions.conf
sudo asterisk -rx "dialplan reload"
```

### 3e. Test a call

```bash
# Originate a test call from Asterisk CLI
sudo asterisk -rx "channel originate Local/100@default application Echo"
```

---

## 4. n8n Workflow Import

```bash
# Open n8n at http://localhost:5678
# Login: admin / change_me (set in docker-compose.yml)

# Import the workflow:
# Settings → Import from file → select n8n/workflows/follow_up_workflow.json

# Set these environment variables in n8n settings:
#   BACKEND_URL    = http://backend:8000
#   BREVO_API_KEY  = your key
#   SLACK_WEBHOOK_URL = your webhook URL (optional)

# Activate the workflow (toggle at top right)
```

---

## 5. Cal.com Self-Hosted Setup

```bash
# Add to docker-compose.yml (or run separately):
#
# calcom:
#   image: calcom/cal.com:latest
#   ports: ["3000:3000"]
#   environment:
#     DATABASE_URL: postgresql://postgres:password@db:5432/calcom
#     NEXTAUTH_SECRET: change_me
#     NEXTAUTH_URL: http://localhost:3000
#     NEXT_PUBLIC_WEBAPP_URL: http://localhost:3000

# After startup:
# 1. Go to http://localhost:3000
# 2. Create an account
# 3. Create an event type with slug "demo-call" (30 mins)
# 4. Copy your API key from Settings → Developer → API Keys
# 5. Set CALCOM_API_KEY in .env
```

---

## 6. Production Deployment (Linux VPS)

```bash
# 1. Point your domain at the server
# 2. Install nginx + certbot for HTTPS

sudo apt install -y nginx certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com

# 3. Create nginx reverse proxy for FastAPI
cat > /etc/nginx/sites-available/voiceai << 'EOF'
server {
    listen 443 ssl;
    server_name api.yourdomain.com;
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 50M;   # allow audio uploads
    }
}
EOF
sudo ln -s /etc/nginx/sites-available/voiceai /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 4. Start services
docker compose -f docker-compose.yml up -d

# 5. Set BACKEND_URL in Asterisk AGI to https://api.yourdomain.com
```

---

## 7. GPU Acceleration (Optional — for faster inference)

```bash
# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list \
  | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker

# Uncomment GPU section in docker-compose.yml for the ollama service
# Also set WHISPER_DEVICE=cuda in .env
```

---

## 8. Monitoring

```bash
# View live logs
docker compose logs -f backend
docker compose logs -f ollama

# Check call sessions in the database
docker exec -it voice_db psql -U postgres voiceai \
  -c "SELECT session_id, outcome, summary FROM call_sessions ORDER BY created_at DESC LIMIT 10;"

# Check leads
docker exec -it voice_db psql -U postgres voiceai \
  -c "SELECT business_name, status, icp_score FROM leads ORDER BY created_at DESC LIMIT 20;"
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Ollama times out | Model too large for RAM — switch to `phi3` (3.8B) or add swap space |
| Whisper slow | Use `WHISPER_MODEL=tiny` for dev; `small` for prod CPU |
| Piper TTS not connecting | Check `docker compose ps piper` — may need voice model downloaded |
| AGI script not found | Check permissions: `chmod +x /var/lib/asterisk/agi-bin/call_handler.py` |
| No audio from Asterisk | Confirm RTP port range 10000–20000 is open in firewall |
| Supabase connection refused | Use `DATABASE_URL` with `asyncpg` dialect in `.env` |
