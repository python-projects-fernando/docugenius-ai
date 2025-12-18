from pydantic import BaseModel
from typing import List

class EnumValue(BaseModel):
    name: str
    value: str

class EnumListResponse(BaseModel):
    enum_name: str
    values: List[EnumValue]