# Responsável por conectar com a API.

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Usa GROQ se disponível, senão tenta OpenAI
api_key = groq_api_key or openai_api_key
base_url = "https://api.groq.com/openai/v1" if groq_api_key else None

if not api_key:
    raise ValueError("❌ Erro: Configure GROQ_API_KEY ou OPENAI_API_KEY no arquivo .env")

client = OpenAI(api_key=api_key, base_url=base_url)


def gerar_resposta(prompt, temperature=0.2):
    resposta = client.responses.create(
        model="openai/gpt-oss-20b",
        temperature=temperature,
        input=prompt
    )

    return resposta.output_text
