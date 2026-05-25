import json
import os

from dotenv import load_dotenv
from google import genai

# carregar variáveis
load_dotenv()

# cliente Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# carregar FAQ
with open("faq.json", "r", encoding="utf-8") as f:
    faq = json.load(f)


def montar_contexto():

    contexto = ""

    for item in faq:

        contexto += f"""
Pergunta: {item['pergunta']}
Resposta: {item['resposta']}

"""

    return contexto


def responder(pergunta_usuario):

    contexto = montar_contexto()

    prompt = f"""
Você é um assistente virtual especialista em consórcio do Santander.

Seu papel é responder dúvidas de maneira:
- natural
- conversacional
- amigável
- clara
- consultiva

IMPORTANTE:
- NÃO copie exatamente o texto da base.
- REESCREVA as informações de maneira humana e fluida.
- Responda como um atendente especializado explicaria ao cliente.
- Organize respostas longas em tópicos quando fizer sentido.
- Nunca invente informações que não estejam na base.
- Utilize apenas as informações fornecidas abaixo.
- Você é um assistente focado apenas em consórcio, se o usuário perguntar qualquer outro assunto responda educadamente que você é especializado apenas em consórcio.

Base de conhecimento:
{contexto}

Pergunta do usuário:
{pergunta_usuario}

INSTRUÇÕES DE FORMATAÇÃO (CRÍTICO):
1. Use quebras de linha e espaçamento entre os parágrafos para a leitura não ficar cansativa.
2. Use tópicos (bullet points) com emojis discretos e adequados para listar passos ou vantagens.
3. Use **negrito** nas palavras-chave mais importantes (como "sem juros", "sorteio", "lance", "carta de crédito").
4. Deixe a resposta visualmente limpa, organizada e elegante.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text