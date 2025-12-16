from pydantic import BaseModel

class InferenceRequest(BaseModel):
    model: str
    prompt: str

class InferenceResponse(BaseModel):
    generated_text: str