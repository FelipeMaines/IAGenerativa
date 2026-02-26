"""
Módulo de validação para garantir que o classificador está em nível de produção.
"""

import json
from typing import Dict, Any, Optional


CATEGORIAS_PERMITIDAS = ["Suporte", "Vendas", "Financeiro", "Geral"]
CATEGORIA_FALLBACK = "Geral"


def parse_json_response(resposta_raw: str) -> Optional[Dict[str, Any]]:
    """
    Parse a resposta JSON retornada pelo modelo LLM.
    
    Args:
        resposta_raw: String contendo a resposta JSON do modelo
        
    Returns:
        Dict com a resposta parseada ou None se falhar
        
    Raises:
        Trata exceções internamente e registra logs
    """
    try:
        # Remove espaços em branco extras
        resposta_limpa = resposta_raw.strip()
        
        # Tenta fazer parse do JSON
        resposta_json = json.loads(resposta_limpa)
        
        # Valida se é um dicionário
        if not isinstance(resposta_json, dict):
            print(f"❌ Erro: Resposta não é um objeto JSON válido")
            return None
            
        return resposta_json
        
    except json.JSONDecodeError as e:
        print(f"❌ Erro ao fazer parse JSON: {e}")
        print(f"   Resposta recebida: {resposta_raw[:100]}...")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado ao processar resposta: {e}")
        return None


def validar_categoria(resposta_json: Optional[Dict[str, Any]]) -> Optional[str]:
    """
    Valida se a categoria está na lista de categorias permitidas.
    
    Args:
        resposta_json: Dicionário com a resposta parseada
        
    Returns:
        String com a categoria validada ou None se inválida
    """
    if resposta_json is None:
        print(f"Resposta JSON é None")
        return None
    
    if "categoria" not in resposta_json:
        print(f"Erro: Campo 'categoria' não encontrado na resposta")
        return None
    
    categoria = resposta_json.get("categoria")
    
    if not isinstance(categoria, str):
        print(f"Erro: 'categoria' não é uma string")
        return None
    
    categoria_limpa = categoria.strip()
    
    if categoria_limpa not in CATEGORIAS_PERMITIDAS:
        print(f"Erro: Categoria '{categoria_limpa}' não está na lista permitida")
        print(f"   Categorias permitidas: {', '.join(CATEGORIAS_PERMITIDAS)}")
        return None
    
    return categoria_limpa


def processar_resposta_com_fallback(resposta_raw: str) -> str:
    """
    Pipeline completo de validação com fallback seguro.
    
    Args:
        resposta_raw: String contendo a resposta JSON do modelo
        
    Returns:
        String com a categoria validada ou categoria fallback se tudo falhar
    """
    resposta_json = parse_json_response(resposta_raw)
    
    categoria = validar_categoria(resposta_json)
    
    if categoria is None:
        print(f"Usando categoria fallback: {CATEGORIA_FALLBACK}")
        return CATEGORIA_FALLBACK
    
    print(f"✅ Categoria validada: {categoria}")
    return categoria


def validar_estrutura_json(resposta_raw: str) -> bool:
    """
    Verifica se a resposta tem a estrutura esperada (sem fazer fallback).
    Útil para diagnóstico e testes.
    
    Args:
        resposta_raw: String contendo a resposta JSON do modelo
        
    Returns:
        True se válida, False caso contrário
    """
    resposta_json = parse_json_response(resposta_raw)
    if resposta_json is None:
        return False
    
    categoria = validar_categoria(resposta_json)
    return categoria is not None
