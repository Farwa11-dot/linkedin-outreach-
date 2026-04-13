-- Voice AI Receptionist — PostgreSQL Schema
-- Run once: psql $DATABASE_URL < database/schema.sql
-- Compatible with Supabase (hosted) and self-hosted PostgreSQL 14+.

-- ─── Extensions ──────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─── Leads ────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS leads (
    id                  UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_name       TEXT        NOT NULL,
    owner_name          TEXT,
    phone_hash          TEXT        NOT NULL,    -- SHA-256 of phone number (PII rule)
    email_hash          TEXT,                    -- SHA-256 of email address
    industry            TEXT,
    city                TEXT,
    country             TEXT        NOT NULL DEFAULT 'US',
    source              TEXT        NOT NULL DEFAULT 'inbound_call',
    status              TEXT        NOT NULL DEFAULT 'new',
    consent_status      TEXT        NOT NULL DEFAULT 'unknown',
    icp_score           INTEGER,
    notes               TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_leads_phone_hash  ON leads (phone_hash);
CREATE INDEX IF NOT EXISTS idx_leads_status      ON leads (status);
CREATE INDEX IF NOT EXISTS idx_leads_industry    ON leads (industry);

-- ─── Call Sessions ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS call_sessions (
    session_id          UUID        PRIMARY KEY,
    call_id             TEXT        NOT NULL,    -- Asterisk UniqueID
    caller_number       TEXT        NOT NULL,    -- SHA-256 hashed (PII)
    called_number       TEXT        NOT NULL,
    started_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at            TIMESTAMPTZ,
    duration_seconds    INTEGER,
    outcome             TEXT        NOT NULL DEFAULT 'completed',
    transcript          JSONB       NOT NULL DEFAULT '[]',
    summary             TEXT,
    lead_id             UUID        REFERENCES leads(id),
    booking_id          TEXT,
    recording_path      TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sessions_lead_id     ON call_sessions (lead_id);
CREATE INDEX IF NOT EXISTS idx_sessions_outcome     ON call_sessions (outcome);
CREATE INDEX IF NOT EXISTS idx_sessions_started_at  ON call_sessions (started_at);

-- ─── Outreach Log ─────────────────────────────────────────────────────────────
-- Tracks every email, LinkedIn message, and call attempt sent.
CREATE TABLE IF NOT EXISTS outreach_log (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id         UUID        NOT NULL REFERENCES leads(id),
    channel         TEXT        NOT NULL,    -- email | linkedin | phone
    template_id     TEXT,
    touch_number    INTEGER     NOT NULL DEFAULT 1,
    sent_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    opened_at       TIMESTAMPTZ,
    replied_at      TIMESTAMPTZ,
    outcome         TEXT,                   -- replied | opened | bounced | opted_out
    message_hash    TEXT,                   -- SHA-256 of sent content (audit)
    jurisdiction    TEXT        NOT NULL DEFAULT 'US',
    gdpr_basis      TEXT
);

CREATE INDEX IF NOT EXISTS idx_outreach_lead_id ON outreach_log (lead_id);
CREATE INDEX IF NOT EXISTS idx_outreach_sent_at ON outreach_log (sent_at);

-- ─── Suppression List ─────────────────────────────────────────────────────────
-- Any contact in this table must NEVER be contacted (compliance Rule 1).
CREATE TABLE IF NOT EXISTS suppression_list (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    contact_hash    TEXT        NOT NULL UNIQUE,  -- SHA-256 of email or phone
    channel         TEXT,                         -- email | phone | all
    reason          TEXT        NOT NULL,
    added_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source          TEXT                          -- opt_out | spam | bounce | manual
);

CREATE INDEX IF NOT EXISTS idx_suppression_hash ON suppression_list (contact_hash);

-- ─── Bookings ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS bookings (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_id      TEXT        NOT NULL UNIQUE,  -- Cal.com UID or Google event ID
    lead_id         UUID        REFERENCES leads(id),
    session_id      UUID        REFERENCES call_sessions(session_id),
    calendar_link   TEXT,
    meeting_url     TEXT,
    confirmed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    outcome         TEXT        DEFAULT 'scheduled'  -- scheduled | no_show | completed
);

-- ─── Audit Log ────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_log (
    id              UUID        PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type      TEXT        NOT NULL,
    entity_type     TEXT,
    entity_id       UUID,
    operator_id     TEXT,
    payload         JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ─── Trigger: auto-update updated_at on leads ─────────────────────────────────
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS leads_updated_at ON leads;
CREATE TRIGGER leads_updated_at
    BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
