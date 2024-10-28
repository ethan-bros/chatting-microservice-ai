from pydantic import BaseModel, Field
from typing import List

from app.adapter.output.messaging.models.line_component import LineComponent


class ContentComponent(BaseModel):
    lines: List[LineComponent] = Field(..., description="대화 리스트")