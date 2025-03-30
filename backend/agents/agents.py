import sys
import os

# Adiciona o caminho absoluto do backend ao sys.path
sys.path.append(os.path.abspath("C:/Users/Eduar/langflow/backend"))
sys.path.append(os.path.abspath(os.getcwd()))
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.agent import AgentFinish
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from tools.tools import busca_wikipedia, actual_temperature_seach, find_cep, currency_search

memory = ConversationBufferMemory(return_messages=True, memory_key='chat_history')

def run_agent(input_text: str, session_memory=None):
    # A inicialização do chat (OpenAI Chat) 
    chat = ChatOpenAI()

    # Definindo as ferramentas que o agente pode utilizar
    tools = [busca_wikipedia, actual_temperature_seach, find_cep, currency_search]
    tools_json = [convert_to_openai_function(tool) for tool in tools]
    tool_run = {tool.name: tool for tool in tools}

    # Prompt com histórico de conversa
    template = [
        ('system', 'You are a friendly assistant called Ribamar. Use the conversation history to remember details about the user, like their name.'),  # 🔴 Prompt alterado para garantir que o nome do usuário seja lembrado
        MessagesPlaceholder(variable_name="chat_history"),  # Histórico de conversa
        ('user', '{input}'),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ]

    # Construção do prompt
    prompt = ChatPromptTemplate.from_messages(template)

    # Recuperando o histórico da memória
    pass_through = RunnablePassthrough.assign(
        agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps']),
        chat_history=lambda x: session_memory.load_memory_variables({})['chat_history'] if session_memory else memory.chat_memory.messages
    )

    # Executando a cadeia de agentes com ferramentas
    agent_chain = pass_through | prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()

    # Executor do agente
    agent_executor = AgentExecutor(
        agent=agent_chain,
        tools=tools,
        memory=memory,
        verbose=True
    )

    # Invocando o agente para gerar a resposta
    response = agent_executor.invoke({'input': input_text})

    # Aqui estamos tentando verificar se o nome está sendo mantido corretamente
    print("Nome do Usuário na Memória:", response)

    return response

