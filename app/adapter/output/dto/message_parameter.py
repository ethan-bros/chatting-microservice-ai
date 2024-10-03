from abc import ABC
from pydantic import BaseModel


class MessageParameter(ABC, BaseModel):
    question: str
