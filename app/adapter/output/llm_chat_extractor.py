import os
import json
from langchain.callbacks import get_openai_callback
from langchain_core.output_parsers import JsonOutputParser

from app.adapter.output.dto.image_message_parameter import ImageMessageParameter
from app.adapter.output.factories.chain_factory import ChainFactory
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
            response = chain.run(
                format_instructions=JsonOutputParser().get_format_instructions()
            )

            # 토큰 사용량 출력
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
