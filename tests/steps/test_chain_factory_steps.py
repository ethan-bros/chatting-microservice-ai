from langchain.chains.llm import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pytest_bdd import scenario, given, when, then
from unittest.mock import patch, Mock

from app.adapter.output.dto.image_message_parameter import ImageMessageParameter
from app.adapter.output.factories.chain_factory import ChainFactory
from app.adapter.output.factories.llm_factory import LLMFactory
from app.adapter.output.factories.prompt_factory import PromptFactory
from app.domain.enums.chain_type import ChainType


@scenario('../features/chain_factory.feature', 'Provide a LLM chain by valid chain type and message parameter')
def test_provide_chain():
    pass

@given('I have a ChatOpenAI from LLMFactory')
def valid_llm():
    patcher = patch.object(LLMFactory, 'get_llm', return_value=Mock(spec=ChatOpenAI))
    patcher.start()
    yield
    patcher.stop()

@given('I have a valid chain type')
def valid_chain_type():
    return ChainType.EXTRACT

@given('I have a valid message parameter')
def valid_message_param():
    return ImageMessageParameter(question='MOCK_QUESTION', image=bytes())

@when('I get a ChatPromptTemplate from PromptFactory')
def get_prompt_template():
    patcher = patch.object(PromptFactory, 'get_prompt', return_value=Mock(spec=ChatPromptTemplate))
    patcher.start()
    yield
    patcher.stop()

@when('I provide a LLM chain')
def provide_llm_chain():
    return ChainFactory.get_chain(valid_chain_type(), valid_message_param())

@then('I should get a instance of LLMChain')
def check_llm_chain():
    assert isinstance(provide_llm_chain(), LLMChain)