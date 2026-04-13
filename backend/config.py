from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    secret_key: str = "change_me"

    # Ollama
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "llama3"
    ollama_temperature: float = 0.3
    ollama_max_tokens: int = 512

    # Whisper
    whisper_model: str = "base"
    whisper_device: str = "cpu"

    # Piper TTS
    piper_model_path: str = "/models/piper/en_US-lessac-medium.onnx"
    piper_sample_rate: int = 22050

    # Database
    database_url: str = "postgresql+asyncpg://postgres:password@db:5432/voiceai"
    supabase_url: str = ""
    supabase_anon_key: str = ""

    # Asterisk
    asterisk_host: str = "asterisk"
    asterisk_ami_port: int = 5038
    asterisk_ami_user: str = "admin"
    asterisk_ami_secret: str = "change_me"

    # Booking
    calcom_base_url: str = "http://calcom:3000"
    calcom_api_key: str = ""
    google_calendar_credentials_path: str = "/secrets/google_credentials.json"
    google_calendar_id: str = "primary"

    # Email
    brevo_api_key: str = ""
    email_from_address: str = "receptionist@yourdomain.com"
    email_from_name: str = "AI Receptionist"

    # n8n
    n8n_webhook_base_url: str = "http://n8n:5678/webhook"

    # Audio
    audio_sample_rate: int = 8000
    audio_temp_dir: str = "/tmp/audio"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
