from typing import Protocol

from backend.application.dtos.ai_inference import InferenceRequest, InferenceResponse


class AIGateway(Protocol):
    async def generate_text(self, request: InferenceRequest) -> InferenceResponse:
        ...