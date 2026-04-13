# Voice AI Receptionist + Sales Automation System

A production-ready, fully open-source Voice AI Receptionist system that answers calls, books appointments, logs data, and automates outreach — with zero paid APIs.

---

## Stack

| Layer | Technology |
|---|---|
| Phone / Telephony | Asterisk (SIP) |
| Speech-to-Text | OpenAI Whisper (local) |
| LLM | Ollama (LLaMA 3 / Mistral) |
| Text-to-Speech | Piper TTS |
| Backend API | Python + FastAPI |
| Database / CRM | Supabase (PostgreSQL) |
| Booking | Cal.com (self-hosted) or Google Calendar API |
| Automation | n8n (self-hosted) |
| Email | Brevo (free tier) |
| Containerisation | Docker + Docker Compose |

---

## Architecture Overview

```
Inbound Call (SIP)
       │
       ▼
  Asterisk PBX
       │  AGI script
       ▼
  FastAPI Backend  ◄──── System Prompt (sales_prompt.txt)
       │
  ┌────┴────────────────┐
  │                     │
  ▼                     ▼
Whisper STT         Piper TTS
  │                     ▲
  ▼                     │
Ollama LLM ────────────►│
  │
  ▼
Supabase DB (logs, leads, transcripts)
  │
  ▼
n8n Workflows (email follow-ups, booking triggers)
  │
  ▼
Cal.com / Google Calendar (appointment booking)
```

---

## Quick Start

```bash
# 1. Clone and configure
git clone <this-repo>
cd voice-ai-receptionist
cp .env.example .env
# Edit .env with your values

# 2. Start all services
docker compose up -d

# 3. Pull an LLM model
docker exec -it ollama ollama pull llama3

# 4. Run database migrations
psql $DATABASE_URL < database/schema.sql

# 5. Configure Asterisk (see docs/deployment.md)
```

---

## Directory Structure

```
.
├── backend/               # FastAPI application
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── routers/
│   │   ├── calls.py
│   │   ├── leads.py
│   │   └── bookings.py
│   ├── services/
│   │   ├── stt.py         # Whisper speech-to-text
│   │   ├── tts.py         # Piper text-to-speech
│   │   ├── llm.py         # Ollama LLM integration
│   │   ├── crm.py         # Supabase CRM
│   │   └── booking.py     # Cal.com / Google Calendar
│   └── prompts/
│       └── system_prompt.txt
├── asterisk/
│   ├── agi/               # AGI scripts (Python)
│   └── dialplan/          # extensions.conf
├── n8n/
│   └── workflows/         # Exportable n8n workflow JSON
├── database/
│   └── schema.sql
├── docs/
│   ├── architecture.md
│   └── deployment.md
├── docker-compose.yml
└── .env.example
```

---

## Full documentation

- [Architecture](docs/architecture.md)
- [Deployment Guide](docs/deployment.md)
