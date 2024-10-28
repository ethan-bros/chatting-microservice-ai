import os

from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from app.domain.enums.llm_provider import LLMProvider


class LLMFactory:
    @staticmethod
    def get_llm(llm_provider: str) -> BaseChatModel:
        model_name = os.getenv("LLM_MODEL")
        temperature = os.getenv("LLM_TEMPERATURE")
        max_tokens = os.getenv("LLM_MAX_TOKENS")

        if llm_provider == LLMProvider.OPEN_AI.value:
            return ChatOpenAI(
                model_name=model_name, temperature=temperature, max_tokens=max_tokens
            )
        # elif llm_provider == LLMProvider.ANTHROPIC.value:
        #     return ChatAnthropic(
        #         model_name=model_name, temperature=temperature, max_tokens=max_tokens
        #     )
