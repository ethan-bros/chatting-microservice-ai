from abc import ABC, abstractmethod
from typing import List

from app.adapter.output.messaging.models.line_component import LineComponent


class MessageProducer(ABC):
    @abstractmethod
    async def send_content_save_message(self, topic: str, content: List[LineComponent]) -> bool:
        pass

    @abstractmethod
    async def close(self):
        pass