import os
from langchain.chains.llm import LLMChain
from langchain_core.output_parsers import JsonOutputParser

from app.adapter.output.dto.message_parameter import MessageParameter
from app.domain.enums.chain_type import ChainType
from app.adapter.output.factories.llm_factory import LLMFactory
from app.adapter.output.factories.message_factory import MessageFactory
from app.adapter.output.factories.prompt_factory import PromptFactory


class ChainFactory:
    @staticmethod
    def get_chain(type: ChainType, human_msg_param: MessageParameter) -> LLMChain:
        llm = LLMFactory.get_llm(os.getenv("LLM_PROVIDER"))

        if type == ChainType.EXTRACT:
            prompt = PromptFactory.get_prompt(human_message=MessageFactory.get_message(param=human_msg_param))
            return LLMChain(llm=llm, prompt=prompt, output_parser=JsonOutputParser())

        elif type == ChainType.RECOMMEND:
            prompt = PromptFactory.get_prompt(human_message=MessageFactory.get_message(param=human_msg_param))
            return LLMChain(llm=llm, prompt=prompt, output_parser=JsonOutputParser())