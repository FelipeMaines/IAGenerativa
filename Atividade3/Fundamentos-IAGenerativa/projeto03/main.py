from llm_client import LLMClient
from retriever import load_conhecimento, gerar_embeddings, busca_similaridade
from validator import validate_json, detectar_prompt_injection
from prompt import build_system_prompt


def main():
    provider = input("Escolha o provedor (openai/groq): ").strip().lower()
    client = LLMClient(provider=provider)

    # Carrega o conhecimento e gera embeddings em memória
    conhecimento = load_conhecimento()
    gerar_embeddings(conhecimento)

    while True:
        query = input("\nDigite sua pergunta (ou 'sair' para encerrar): ").strip()
        if query.lower() == "sair":
            break

        # --- Proteção contra Prompt Injection ---
        if detectar_prompt_injection(query):
            print("⚠️  Solicitação não permitida. Por favor, faça perguntas relacionadas ao suporte.")
            continue

        # --- Busca por Similaridade (RAG) ---
        contexto = busca_similaridade(query)
        system_prompt = build_system_prompt()

        response_text = client.generate_text(system_prompt, contexto)

        try:
            is_valid, data = validate_json(response_text)
            if is_valid:
                print(f"Resposta: {data['resposta']}")
        except ValueError as e:
            print(f"Erro de validação: {e}")


if __name__ == "__main__":
    main()

