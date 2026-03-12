import json
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import APIError, AuthenticationError, Groq

from tools import TOOL_DEFINITIONS, execute_tool

MAX_HISTORY_MESSAGES = 10
HISTORY_FILE = Path(__file__).with_name("historico.json")
SYSTEM_PROMPT = (
    "Você é um assistente formal e profissional. "
    "Responda com clareza, objetividade e educação. "
    "Quando uma solicitação puder ser resolvida com mais precisão por uma ferramenta disponível, "
    "use a ferramenta antes de responder. "
    "Nunca invente resultados de ferramentas."
)

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def carregar_historico():
    if not HISTORY_FILE.exists():
        return []

    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as file:
            dados = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []

    if not isinstance(dados, list):
        return []

    historico_valido = []
    for mensagem in dados:
        if not isinstance(mensagem, dict):
            continue
        role = mensagem.get("role")
        content = mensagem.get("content")
        if role in {"user", "assistant"} and isinstance(content, str):
            historico_valido.append({"role": role, "content": content})

    return historico_valido[-MAX_HISTORY_MESSAGES:]


historico_mensagens = carregar_historico()


def persistir_historico():
    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(historico_mensagens, file, ensure_ascii=False, indent=2)


def limitar_historico():
    global historico_mensagens
    historico_mensagens = historico_mensagens[-MAX_HISTORY_MESSAGES:]


def salvar_mensagem(role, content):
    historico_mensagens.append({"role": role, "content": content})
    limitar_historico()
    persistir_historico()


def limpar_historico():
    historico_mensagens.clear()
    persistir_historico()


def construir_contexto():
    return [{"role": "system", "content": SYSTEM_PROMPT}, *historico_mensagens]


def serializar_tool_call(tool_call):
    return {
        "id": tool_call.id,
        "type": tool_call.type,
        "function": {
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments,
        },
    }


def executar_tool_calls(mensagens, tool_calls):
    for tool_call in tool_calls:
        try:
            argumentos = json.loads(tool_call.function.arguments or "{}")
            resultado = execute_tool(tool_call.function.name, argumentos)
        except (TypeError, ValueError, json.JSONDecodeError) as error:
            resultado = {"erro": str(error)}
        mensagens.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(resultado, ensure_ascii=False),
            }
        )


def chat(pergunta):
    salvar_mensagem("user", pergunta)
    mensagens = construir_contexto()

    for _ in range(3):
        try:
            resposta = client.chat.completions.create(
                model=MODEL,
                messages=mensagens,
                tools=TOOL_DEFINITIONS,
            )
        except AuthenticationError:
            resposta_conteudo = "A GROQ_API_KEY esta invalida ou expirada. Atualize a chave no arquivo .env e tente novamente."
            salvar_mensagem("assistant", resposta_conteudo)
            return resposta_conteudo
        except APIError as error:
            resposta_conteudo = f"Ocorreu um erro na API da Groq: {error}"
            salvar_mensagem("assistant", resposta_conteudo)
            return resposta_conteudo
        except Exception as error:
            resposta_conteudo = f"Ocorreu um erro inesperado ao consultar o modelo: {error}"
            salvar_mensagem("assistant", resposta_conteudo)
            return resposta_conteudo

        mensagem = resposta.choices[0].message

        if not mensagem.tool_calls:
            resposta_conteudo = mensagem.content or "Não consegui gerar uma resposta no momento."
            salvar_mensagem("assistant", resposta_conteudo)
            return resposta_conteudo

        mensagens.append(
            {
                "role": "assistant",
                "content": mensagem.content or "",
                "tool_calls": [serializar_tool_call(tool_call) for tool_call in mensagem.tool_calls],
            }
        )
        executar_tool_calls(mensagens, mensagem.tool_calls)

    resposta_conteudo = "Não consegui concluir a resposta com as ferramentas disponíveis."
    salvar_mensagem("assistant", resposta_conteudo)
    return resposta_conteudo


def main():
    while True:
        pergunta = input("Você: ").strip()

        if not pergunta:
            print("Assistente: Digite uma mensagem ou use /limpar para apagar o histórico.")
            continue

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("Encerrando o chat. Até mais!")
            break

        if pergunta == "/limpar":
            limpar_historico()
            print("Assistente: Memória da conversa apagada.")
            continue

        resposta = chat(pergunta)
        print("Assistente:", resposta)


if __name__ == "__main__":
    main()
