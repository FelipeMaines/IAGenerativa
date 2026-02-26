from llm_client import gerar_resposta
from validator import processar_resposta_com_fallback, CATEGORIAS_PERMITIDAS

CATEGORIAS = CATEGORIAS_PERMITIDAS


def classificar_mensagem(mensagem, temperature=0.2):
    """
    Classifica a mensagem em uma categoria com validação robusta.
    
    Args:
        mensagem: String com a mensagem a ser classificada
        temperature: Temperatura do modelo (0.0 a 1.0)
        
    Returns:
        String com a categoria validada ou fallback "Geral"
    """
    prompt = f"""
        Classifique a mensagem abaixo em uma das seguintes categorias: {', '.join(CATEGORIAS)}.
        Retorne apenas um JSON no formato:
        {{
            "categoria": "nome_categoria"
        }}

        Mensagem: "{mensagem}"
    """
    
    try:
        resposta_raw = gerar_resposta(prompt, temperature)
        categoria_validada = processar_resposta_com_fallback(resposta_raw)
        return categoria_validada
    except Exception as e:
        print(f"❌ Erro crítico na classificação: {e}")
        print(f"   Usando fallback: Geral")
        return "Geral"
