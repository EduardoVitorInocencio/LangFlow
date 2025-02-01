import sys
import os

# Adiciona o caminho absoluto do backend ao sys.path
sys.path.append(os.path.abspath("C:/Users/edinocencio/langflow/backend"))
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

def run_agent(input_text: str):

    chat = ChatOpenAI()
    tools = [busca_wikipedia, actual_temperature_seach, find_cep, currency_search]
    tools_json = [convert_to_openai_function(tool) for tool in tools]
    tool_run = {tool.name: tool for tool in tools}

    template = [
        ('system', 'You are a friendly assistent called Ribamar' +
                    'Use the conversation hostory to remember details about the user.'),  # 🔴 Forçamos a AI considerar o histórico no prompt
                    MessagesPlaceholder(variable_name="chat_history"),  # 🔴 Adicionamos o histórico ao prompt
        ('user', '{input}'),
        MessagesPlaceholder(variable_name='agent_scratchpad')
    ]

    prompt = ChatPromptTemplate.from_messages(template)

    pass_through = RunnablePassthrough.assign(
        agent_scratchpad = lambda x: format_to_openai_function_messages(x['intermediate_steps']),
        chat_history=lambda x: memory.chat_memory.messages  # 🔴 Pegamos o histórico da memória
    )
    agent_chain = pass_through | prompt | chat.bind(functions=tools_json) | OpenAIFunctionsAgentOutputParser()

    agent_executor = AgentExecutor(
        # '''
        #     agent=agent_chain: Esse parâmetro recebe um agente (agent_chain), que é a cadeia de execução do agente.
        #     O agente é o componente responsável por decidir quais ferramentas usar e como estruturar a resposta com base na entrada do usuário.

        #     tools=tools: Aqui, passamos uma lista de ferramentas (tools) que o agente pode usar para realizar tarefas.
        #     As ferramentas podem ser APIs externas, consultas a bancos de dados, modelos de machine learning, entre outras funcionalidades.

        #     verbose=True: Ativa a saída detalhada (modo verboso), útil para debugging, pois imprime logs sobre o funcionamento do agente.
        # '''
        agent=agent_chain,
        tools=tools,
        memory=memory, # 🔴 Mantemos a mesma instância de memória
        verbose=True
    )

    return agent_executor.invoke({'input': input_text})

resposta = run_agent(input_text='Quantos reais são 10000 dólares hoje?')
print(resposta)
