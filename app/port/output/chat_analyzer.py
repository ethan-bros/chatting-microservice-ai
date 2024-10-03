from abc import ABC, abstractmethod

from app.adapter.output.dto.request.chat_recommend_request import ChatRecommendRequest


class ChatAnalyzer(ABC):
    @abstractmethod
    def recommend_reply_based_on(self, request: ChatRecommendRequest):
        pass
