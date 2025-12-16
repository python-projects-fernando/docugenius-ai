from openai import OpenAI
from backend.application.ai_gateway.ai_gateway import AIGateway
from backend.application.dtos.ai_inference import InferenceRequest, InferenceResponse

class HuggingFaceOpenAIAIGateway(AIGateway):
    def __init__(self, hf_token: str, base_url: str = "https://router.huggingface.co/v1"):
        self._client = OpenAI(base_url=base_url, api_key=hf_token)

    async def generate_text(self, request: InferenceRequest) -> InferenceResponse:
        try:
            completion = self._client.chat.completions.create(
                model=request.model,
                messages=[
                    {"role": "user", "content": request.prompt}
                ],
            )
            generated_text = completion.choices[0].message.content
            return InferenceResponse(generated_text=generated_text)
        except Exception as e:
            raise RuntimeError(f"Error calling Hugging Face Inference API via OpenAI client: {e}")