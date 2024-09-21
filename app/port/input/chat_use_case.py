from abc import ABC, abstractmethod

class ChatUseCase(ABC):
    @abstractmethod
    async def recommend(self, input: str) -> str:
        pass