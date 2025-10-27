from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    aws_region: str = os.getenv("AWS_REGION", "ap-southeast-2")

    llm_provider: str = os.getenv("LLM_PROVIDER", "openai")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

    git_remote: str = os.getenv("GIT_REMOTE", "origin")
    git_main_branch: str = os.getenv("GIT_MAIN_BRANCH", "main")
    git_user_name: str = os.getenv("GIT_USER_NAME", "agent-bot")
    git_user_email: str = os.getenv("GIT_USER_EMAIL", "agent-bot@example.com")

    lookback_days: int = int(os.getenv("LOOKBACK_DAYS", "14"))
    min_util: float = float(os.getenv("MIN_UTIL", "0.15"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "5"))

    max_p95_latency_ms: int = int(os.getenv("MAX_P95_LATENCY_MS", "200"))
    max_error_rate: float = float(os.getenv("MAX_ERROR_RATE", "0.01"))

    freeze_window_cron: str = os.getenv("FREEZE_WINDOW_CRON", "")

settings = Settings()
