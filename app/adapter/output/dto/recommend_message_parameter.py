from app.adapter.output.dto.message_parameter import MessageParameter
from app.domain.chat_context import ChatContext


class RecommendMessageParameter(MessageParameter):
    context: ChatContext