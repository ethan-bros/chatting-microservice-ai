from pydantic import BaseModel, Field
from typing import List, Dict

from app.adapter.output.messaging.models.line_component import LineComponent


class ContentSaveMessage(BaseModel):
    conversationId: str = Field(..., description="전체 대화 ID")
    lines: List[LineComponent] = Field(default_factory=list, description="대화 내용")
