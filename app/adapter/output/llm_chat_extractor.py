import json
import os

from langchain.callbacks import get_openai_callback

from app.adapter.output.dto.image_message_parameter import ImageMessageParameter
from app.adapter.output.factories.chain_factory import ChainFactory
from app.adapter.output.messaging.models.line_component import LineComponent
from app.domain.enums.chain_type import ChainType
from app.port.output.chat_extractor import ChatExtractor


class LLMChatExtractor(ChatExtractor):
    def extract_from(self, image: bytes):
        # 체인 생성
        param = ImageMessageParameter(
            question=os.getenv("LLM_CHAT_EXTRACT_QUESTION"), image=image
        )
        chain = ChainFactory.get_chain(type=ChainType.EXTRACT, human_msg_param=param)

        # 콜백을 사용하여 토큰 사용량 추적
        with get_openai_callback() as cb:
            response = chain.invoke({})

            parsed_response = [
                LineComponent(**item)
                for item in response
                if all(key in item for key in LineComponent.__annotations__)
            ]

            # 토큰 사용량 출력
            print(f"Total Tokens: {cb.total_tokens}")
            print(f"Prompt Tokens: {cb.prompt_tokens}")
            print(f"Completion Tokens: {cb.completion_tokens}")
            print(f"Total Cost (USD): ${cb.total_cost}")

        # 응답에서 JSON 추출 시도
        try:
            return parsed_response

        except json.JSONDecodeError:
            print("JSON 파싱 오류. API 출력:")
            print(response.content)
            return None
