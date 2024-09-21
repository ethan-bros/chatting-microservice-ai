from abc import ABC, abstractmethod

class ChatExtractor(ABC):
    @abstractmethod
    def extract_from(self, image: bytes):
        pass