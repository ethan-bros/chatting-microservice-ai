from pydantic import BaseModel, Field
from typing import List, Dict
import json


class ChatContext(BaseModel):
    # 상대방, 페르소나 등은 추후에...
    purpose: str = Field(..., description="대화 목적")
    contents: List[Dict] = Field(default_factory=list, description="대화 내용")

    def to_json_string(self) -> str:
        return json.dumps(self.model_dump(), ensure_ascii=False, indent=2)
