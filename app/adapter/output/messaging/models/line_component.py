from pydantic import BaseModel, Field


class LineComponent(BaseModel):
    order: int = Field(..., description="순서")
    speaker: str = Field(..., description="화자")
    line: str = Field(..., description="내용")

    class Config:
        arbitrary_types_allowed = True