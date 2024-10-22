from abc import ABC, abstractmethod
from typing import List
from app.adapter.output.messaging.models.line_component import LineComponent


class ChatExtractor(ABC):
    @abstractmethod
    def extract_from(self, image: bytes)-> List[LineComponent]:
        pass
