# System Architecture

## Call Flow — Step by Step

```
┌─────────────────────────────────────────────────────────────────────┐
│                         INBOUND PHONE CALL                          │
└─────────────────────────┬───────────────────────────────────────────┘
                          │  SIP / PSTN
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ASTERISK PBX                                   │
│  extensions.conf → AGI(call_handler.py)                             │
│  • Answers the call                                                  │
│  • Records caller audio (silence-detected chunks, WAV 8kHz)         │
│  • Plays synthesised reply WAV files                                │
└─────────────────────────┬───────────────────────────────────────────┘
                          │  HTTP (multipart audio upload)
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                                   │
│  POST /calls/start   → creates session, returns session_id          │
│  POST /calls/speech  → STT → LLM → TTS pipeline                    │
│  POST /calls/{id}/end→ finalises call, triggers background tasks    │
└──────┬────────────────────────────┬──────────────────────┬──────────┘
       │                            │                      │
       ▼                            ▼                      ▼
┌──────────────┐         ┌──────────────────┐   ┌─────────────────────┐
│ WHISPER STT  │         │   OLLAMA LLM     │   │    PIPER TTS        │
│ (local model)│         │ (llama3/mistral) │   │  (wyoming-piper)    │
│              │         │                  │   │                     │
│ WAV → Text   │────────►│ Text + history   │──►│ Text → WAV (8kHz)   │
│              │         │ → reply text     │   │                     │
└──────────────┘         └──────────────────┘   └─────────────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
                    ▼                            ▼
        ┌───────────────────┐        ┌────────────────────┐
        │   SUPABASE /      │        │     CAL.COM /      │
        │   POSTGRESQL      │        │  GOOGLE CALENDAR   │
        │                   │        │                    │
        │ • call_sessions   │        │ Book appointment   │
        │ • leads           │        │ Send invite email  │
        │ • outreach_log    │        └────────────────────┘
        │ • suppression     │
        └─────────┬─────────┘
                  │  webhook
                  ▼
        ┌─────────────────────┐
        │     n8n WORKFLOWS   │
        │                     │
        │ • Email follow-up   │
        │ • Slack alerts      │
        │ • Lead status update│
        │ • Booking confirm   │
        └─────────────────────┘
```

## Component Responsibilities

### Asterisk
- Receives SIP calls from your VoIP provider (Twilio SIP, VoIP.ms, etc.)
- Records audio chunks using `Record()` with silence detection
- Plays reply audio using `STREAM FILE`
- All SIP/RTP processing stays within Asterisk — the backend only sees WAV files

### FastAPI Backend
- Stateless HTTP API (session state in memory; swap for Redis in production)
- Orchestrates the STT → LLM → TTS pipeline per turn
- Writes all data to PostgreSQL (PII is SHA-256 hashed before storage)
- Fires n8n webhook on call end

### Whisper STT
- Runs the `openai-whisper` Python package locally (no API key)
- Model loaded once at startup; transcription runs in a thread executor
- `base` model: ~74M params, ~1s transcription on CPU for a 10s clip
- Upgrade to `small` or `medium` for better accuracy (needs more RAM)

### Ollama LLM
- Runs llama3 (8B) or mistral (7B) locally via the Ollama daemon
- 8B model: needs ~8GB RAM (CPU) or ~5GB VRAM (GPU)
- Conversation history passed on every turn for context continuity
- Temperature 0.3 keeps responses consistent and on-script

### Piper TTS
- wyoming-piper Docker container exposes port 10200
- Produces natural-sounding speech at 22kHz; backend downsamples to 8kHz for Asterisk
- Voices: `en_US-lessac-medium` (neutral), `en_US-ryan-high` (male), `en_GB-alan-medium` (British)

### Supabase / PostgreSQL
- All PII (phone numbers, emails) stored as SHA-256 hashes only
- JSONB column stores full call transcript per session
- Suppression list checked before any outbound action

### Cal.com
- Self-hosted on Docker (or use cloud free tier)
- API used to look up event type ID and create bookings
- Sends calendar invite emails automatically

### n8n
- Triggered by FastAPI webhook on call end
- Routes workflow based on call outcome (booked / callback / not interested)
- Sends confirmation emails via Brevo, updates lead status, pings Slack

## Scaling

| Concurrent Calls | Recommended Setup |
|---|---|
| 1–5 | Single Docker host, CPU inference |
| 5–20 | Dedicated GPU for Whisper + Ollama, Redis for session state |
| 20+ | Multiple FastAPI workers behind nginx, Whisper on separate GPU server |

For high call volumes, move Whisper inference to a faster-whisper server
(uses CTranslate2 — 4× faster than original Whisper on CPU).
