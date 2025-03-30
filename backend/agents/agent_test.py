from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd
from dotenv import find_dotenv, load_dotenv
import streamlit as st

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

def run_pandas_agent(input_text: str, generate_excel: bool = False):
    # Carregar o dataset para agente pandas
    df = pd.read_csv(
        "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
    )

    # Criar o agente para pandas (dados)
    pandas_agent = create_pandas_dataframe_agent(
        ChatOpenAI(temperature=0, model="gpt-4o-mini"),
        df,
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        allow_dangerous_code=True
    )

    # Chamar o agente para invocar uma consulta
    response = pandas_agent.invoke(input_text)

    # Se for solicitado gerar um arquivo Excel
    if generate_excel:
        try:
            # Converter resposta para DataFrame (caso seja uma string descritiva, ajustamos)
            if isinstance(response, pd.DataFrame):
                result_df = response
            else:
                # Tentar extrair os dados numéricos da resposta para um DataFrame
                result_df = pd.DataFrame([response])

            # Criar o arquivo Excel
            excel_filename = "dados_resumidos.xlsx"
            result_df.to_excel(excel_filename, index=False)

            # Retornar o caminho do arquivo
            return response, excel_filename
        except Exception as e:
            return f"Erro ao gerar o arquivo Excel: {e}", None

    return response, None
