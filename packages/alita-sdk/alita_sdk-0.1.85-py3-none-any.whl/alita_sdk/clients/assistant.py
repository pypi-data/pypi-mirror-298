
from typing import Any
from langchain.agents import (
    AgentExecutor, create_react_agent, 
    create_openai_tools_agent, 
    create_openai_functions_agent)
from ..agents.mixedAgentParser import MixedAgentOutputParser
from ..agents.llama_agent import LLamaAssistantRunnable
from ..agents.autogen_agent import AutoGenAssistantRunnable
from ..agents.mixedAgentRenderes import render_react_text_description_and_args
from ..agents.alita_agent import AlitaAssistantRunnable
from ..agents.langraph_agent import LGAssistantRunnable
from langchain_core.messages import (
    BaseMessage,
)
from langchain_core.prompts import ChatPromptTemplate

class Assistant:
    def __init__(self, client: Any, 
                 prompt: ChatPromptTemplate, 
                 tools: list, 
                 chat_history: list[BaseMessage] = []):
        self.prompt = prompt
        self.client = client
        self.tools = tools
        self.chat_history = chat_history

    def _agent_executor(self, agent: Any):
        return AgentExecutor.from_agent_and_tools(agent=agent, tools=self.tools,
                                                  verbose=True, handle_parsing_errors=True,
                                                  max_execution_time=None, return_intermediate_steps=True)

    def getAgentExecutor(self):
        agent = create_react_agent(llm=self.client, tools=self.tools, prompt=self.prompt,
                                   output_parser=MixedAgentOutputParser(), 
                                   tools_renderer=render_react_text_description_and_args)
        return self._agent_executor(agent)
        
    def getOpenAIToolsAgentExecutor(self):
        agent = create_openai_tools_agent(llm=self.client, tools=self.tools, prompt=self.prompt)
        return self._agent_executor(agent)
    
    def getLLamaAgentExecutor(self):
        agent = LLamaAssistantRunnable.create_assistant(client=self.client, tools=self.tools,
                                                        prompt=self.prompt)
        return self._agent_executor(agent)

    def getOpenAIFunctionsAgentExecutor(self):
        agent = create_openai_functions_agent(llm=self.client, tools=self.tools, prompt=self.prompt)
        return self._agent_executor(agent)
    
    def getAlitaExecutor(self):
        agent = AlitaAssistantRunnable().create_assistant(
            client=self.client, tools=self.tools, prompt=self.prompt,
        )
        return AgentExecutor.from_agent_and_tools(agent=agent, tools=self.tools,
                                                  verbose=True, handle_parsing_errors=True,
                                                  max_execution_time=None,
                                                  return_intermediate_steps=True)
    
    def getLGExecutor(self):
        agent = LGAssistantRunnable.create_assistant(
            client=self.client, 
            tools=self.tools, 
            prompt=self.prompt,
            chat_history=self.chat_history)
        return self._agent_executor(agent)
    
    def getAutoGenExecutor(self):
        agent = AutoGenAssistantRunnable.create_assistant(client=self.client, tools=self.tools, prompt=self.prompt)
        return self._agent_executor(agent)

    # This one is used only in Alita and OpenAI
    def apredict(self, messages: list[BaseMessage]):
        yield from self.client.ainvoke(messages)

    def predict(self, messages: list[BaseMessage]):
        return self.client.invoke(messages)
