import streamlit as st
from agents.agents import run_agent
from agents.agent_test import run_pandas_agent
from langchain.memory import ConversationBufferMemory
from dotenv import find_dotenv, load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Configuração da Página
st.set_page_config(page_title="Chatbot Ribamar", page_icon="🤖")

st.title("🤖 Chatbot Ribamar")
st.markdown("**Fale com o assistente inteligente ou consulte dados!**")

# Inicializa o estado da sessão para o histórico do chat
if "messages" not in st.session_state:
    st.session_state.messages = []  
    
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = ConversationBufferMemory(return_messages=True, memory_key='chat_history')

if "awaiting_excel_confirmation" not in st.session_state:
    st.session_state.awaiting_excel_confirmation = False

if "last_user_input" not in st.session_state:
    st.session_state.last_user_input = ""

if "excel_file_path" not in st.session_state:
    st.session_state.excel_file_path = None  # Armazena o caminho do Excel gerado pela LLM

# Exibir mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada do usuário
user_input = st.chat_input("Digite sua pergunta...")

# Função para escolher o agente apropriado
def select_agent(user_input):
    if any(keyword in user_input.lower() for keyword in ["titanic", "rows", "data", "quantas", "colunas"]):
        return run_pandas_agent
    else:
        return run_agent

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    selected_agent = select_agent(user_input)

    if selected_agent == run_pandas_agent:
        st.session_state.awaiting_excel_confirmation = True
        st.session_state.last_user_input = user_input  # Salva a pergunta para processar depois
        
    else:
        bot_response = selected_agent(user_input, session_memory=st.session_state.chat_memory).get("output", "Erro ao obter resposta.")

        with st.chat_message("assistant"):
            st.markdown(bot_response)

        st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Se estamos esperando a confirmação do Excel, exibe os botões
if st.session_state.awaiting_excel_confirmation:
    st.markdown("Deseja gerar um arquivo Excel com os dados resumidos?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅ Sim"):
            response, excel_file = run_pandas_agent(st.session_state.last_user_input, generate_excel=True)
            with st.chat_message("assistant"):
                
                st.markdown(response)
            if excel_file and os.path.exists(excel_file):
                st.session_state.excel_file_path = excel_file
           
            st.session_state.awaiting_excel_confirmation = False  # Reseta o estado

    with col2:
        if st.button("❌ Não"):
            response, _ = run_pandas_agent(st.session_state.last_user_input, generate_excel=False)
            with st.chat_message("assistant"):
                st.markdown(response)

            st.session_state.awaiting_excel_confirmation = False  # Reseta o estado

# Se o arquivo foi gerado pela LLM, exibe botão de download
if st.session_state.excel_file_path and os.path.exists(st.session_state.excel_file_path):
    with open(st.session_state.excel_file_path, "rb") as file:
        st.download_button(label="📥 Baixar Excel",
                           data=file,
                           file_name=os.path.basename(st.session_state.excel_file_path),  # Nome original do arquivo
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
