import json
import re

def validate_json(response_text):
    try:
        data = json.loads(response_text)
        if "status" not in data:
            raise ValueError("Campo 'status' obrigatório")
        return True, data
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON: {e}")


def detectar_prompt_injection(user_input):
    """
    Detecta tentativas de prompt injection analisando padrões suspeitos na entrada do usuário.
    
    Retorna:
        bool: True se detectar tentativa de injection, False caso contrário
    """
    
    # Padrões de detecção para prompt injection
    injection_patterns = [
        # Tentar acessar system prompt
        r"system\s+prompt",
        r"sistema\s+prompt",
        r"sua\s+system\s+prompt",
        r"qual\s+é?\s*a?\s*sua\s+system",
        r"mostre?\s+seu\s+prompt",
        r"qual\s+é\s+o\s+seu\s+prompt",
        
        # Instruções para ignorar comportamento
        r"ignore\s+as\s+instruções",
        r"esqueça\s+as\s+instruções",
        r"cancele\s+o\s+contexto",
        r"forget\s+.*instructions",
        r"ignore\s+.*instructions",
        
        # Tentar fazer role-play
        r"você\s+agora\s+é",
        r"atue\s+como",
        r"pretenda\s+que",
        r"from\s+now\s+on",
        
        # Tentar ver contexto/conhecimento
        r"mostre\s+o\s+contexto",
        r"qual\s+é\s+o\s+conhecimento",
        r"que\s+informações\s+você\s+tem",
        r"liste\s+seus\s+arquivos",
        r"show\s+.*knowledge",
        
        # Tentar fazer ações maliciosas
        r"código\s+malicioso",
        r"execute\s+script",
        r"comando\s+shell",
        r"bash\s+command",
        
        # Jailbreak comum
        r"desenvolva\s+um\s+malware",
        r"como\s+fazer\s+exploit",
        r"crie\s+um\s+vírus",
    ]
    
    # Converter entrada para minúsculas para comparação case-insensitive
    normalized_input = user_input.lower().strip()
    
    # Verificar cada padrão
    for pattern in injection_patterns:
        if re.search(pattern, normalized_input):
            return True
    
    return False
        