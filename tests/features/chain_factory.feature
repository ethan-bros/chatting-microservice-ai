Feature: Chain Factory
  As a developer
  I want to get LLM chain by chain type
  So that they can provide instances of LLMChain depends on user's purpose

  Scenario: Provide a LLM chain by valid chain type and message parameter
    Given I have a ChatOpenAI from LLMFactory
    And I have a valid chain type
    And I have a valid message parameter
    When I get a ChatPromptTemplate from PromptFactory
    And I provide a LLM chain
    Then I should get a instance of LLMChain