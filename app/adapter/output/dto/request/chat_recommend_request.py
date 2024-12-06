from pydantic import BaseModel, Field
from typing import List, Dict

from app.adapter.output.messaging.models.line_component import LineComponent


class ChatRecommendRequest(BaseModel):
    # 상대방, 페르소나 등은 추후에...
    id: str = Field(..., description="ID")
    purpose: str = Field(..., description="대화 목적")
    contents: List[LineComponent] = Field(default_factory=list, description="대화 내용")
