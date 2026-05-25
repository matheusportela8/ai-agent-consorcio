import streamlit as st
import time
import unicodedata
# Importa a função do seu arquivo chatbot.py
from chatbot import responder

def limpar_texto(texto):

    texto = unicodedata.normalize("NFKC", texto)

    return texto

# 1. Configuração da página
LOGO_URL = "https://assets.abstra.cloud/connectors/logos/santander.png"

st.set_page_config(
    page_title="Consórcio Santander", 
    page_icon=LOGO_URL,
    layout="centered"
)

# 2. Estilização CSS Customizada (Visual Santander)
st.markdown("""
    <style>
        /* Altera a cor de foco do input para o vermelho Santander */
        div[data-baseweb="input"] {
            border-color: #CC0000 !important;
        }
        
        /* Container do cabeçalho usando Flexbox para alinhar lado a lado */
        .header-container {
            background-color: #CC0000;
            padding: 15px 25px;
            border-radius: 12px;
            color: white;
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 25px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        
        /* Estilização da Logo */
        .brand-logo {
            width: 45px;
            height: auto;
            filter: brightness(0) invert(1);
        }
        
        /* Bloco de texto do cabeçalho */
        .header-text-block {
            display: flex;
            flex-direction: column;
        }
        
        .header-title {
            font-size: 22px;
            font-weight: bold;
            margin: 0;
            line-height: 1.2;
        }
        
        .header-subtitle {
            font-size: 13px;
            opacity: 0.85;
            margin-top: 2px;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Renderização do Cabeçalho
st.markdown(f"""
    <div class="header-container">
        <img class="brand-logo" src="{LOGO_URL}" alt="Logo Santander">
        <div class="header-text-block">
            <div class="header-title">Consórcio Santander</div>
            <div class="header-subtitle">Espaço exclusivo para esclarecimento de dúvidas</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. Inicialização do Histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Olá! Sou o assistente virtual do Santander. Este é um canal exclusivo para tirar suas dúvidas sobre consórcios. Qual informação você gostaria de esclarecer hoje? Pode me perguntar sobre lances, taxas, prazos ou o processo de contemplação!"
        }
    ]

# 5. Exibição das Mensagens Salvas (Histórico)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 6. Campo de Entrada de Mensagens e Conexão com o Gemini
if user_input := st.chat_input("Digite sua dúvida sobre consórcio aqui..."):
    
    # Mostra a mensagem que o usuário acabou de digitar
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Resposta real do Assistente usando o Gemini + FAQ
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Mostra um spinner de carregamento enquanto o Gemini processa a resposta
        with st.spinner("Analisando sua dúvida..."):
            # CHAMADA REAL DA SUA IA DO CHATBOT.PY
            response = responder(user_input)

            response = limpar_texto(response)
            
        # Efeito visual de digitação fluida para a resposta retornada pela IA
        # Efeito visual de digitação preservando markdown
        full_response = ""

        for char in response:

            full_response += char

            time.sleep(0.002)

            message_placeholder.markdown(
                full_response + "▌"
            )

        message_placeholder.markdown(full_response)
        
    # Salva a resposta gerada pela IA no histórico da sessão
    st.session_state.messages.append({"role": "assistant", "content": full_response})