import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

class PromptFactory:
    @staticmethod
    def get_prompt(human_message: HumanMessage) -> ChatPromptTemplate:
        system_message = SystemMessage(content=os.getenv("LLM_SYSTEM_ORDER"))
        return ChatPromptTemplate.from_messages([system_message, human_message])