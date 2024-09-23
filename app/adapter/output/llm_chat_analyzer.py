import os
import json
from langchain.callbacks import get_openai_callback
from langchain_core.output_parsers import JsonOutputParser

from app.adapter.output.dto.recommend_message_parameter import RecommendMessageParameter
from app.adapter.output.dto.request.chat_recommend_request import ChatRecommendRequest
from app.adapter.output.factories.chain_factory import ChainFactory
from app.domain.chat_context import ChatContext
from app.domain.enums.chain_type import ChainType
from app.port.output.chat_analyzer import ChatAnalyzer

class LLMChatAnalyzer(ChatAnalyzer):
    def recommend_reply_based_on(self, request: ChatRecommendRequest):
        # 체인 생성
        param = RecommendMessageParameter(question=os.getenv("LLM_CHAT_RECOMMEND_QUESTION"), context=ChatContext(**request.model_dump()))
        chain = ChainFactory.get_chain(type=ChainType.RECOMMEND, human_msg_param=param)

        # 콜백을 사용하여 토큰 사용량 추적
        with get_openai_callback() as cb:
            response = chain.run(format_instructions=JsonOutputParser().get_format_instructions())

            # 토큰 사용량 출력
            print(f"=============== 채팅 추천 AI =====================")
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")

        # 응답에서 JSON 추출 시도
        try:
            return response

        except json.JSONDecodeError:
            print("JSON 파싱 오류. API 출력:")
            print(response.content)
            return None