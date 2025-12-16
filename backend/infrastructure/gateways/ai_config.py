from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AIConfiguration:
    def __init__(self):
        self.hf_token = self._get_env_var("HF_API_TOKEN", required=True)
        self.base_url = os.getenv("HF_OPENAI_BASE_URL", "https://router.huggingface.co/v1")

    def _get_env_var(self, key: str, required: bool = False) -> Optional[str]:
        value = os.getenv(key)
        if required and not value:
            raise ValueError(f"Environment variable '{key}' is required but not set.")
        return value

def get_ai_configuration() -> AIConfiguration:
    return AIConfiguration()