import secrets
import string

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calcular_imc",
            "description": "Calcula o IMC a partir do peso em quilogramas e da altura em metros.",
            "parameters": {
                "type": "object",
                "properties": {
                    "peso": {
                        "type": "number",
                        "description": "Peso da pessoa em quilogramas.",
                    },
                    "altura": {
                        "type": "number",
                        "description": "Altura da pessoa em metros.",
                    },
                },
                "required": ["peso", "altura"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gerar_senha",
            "description": "Gera uma senha aleatória segura com o tamanho solicitado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "comprimento": {
                        "type": "integer",
                        "description": "Quantidade de caracteres da senha, entre 4 e 64.",
                    },
                    "incluir_maiusculas": {
                        "type": "boolean",
                        "description": "Se verdadeiro, inclui letras maiúsculas na senha.",
                    },
                    "incluir_numeros": {
                        "type": "boolean",
                        "description": "Se verdadeiro, inclui números na senha.",
                    },
                    "incluir_simbolos": {
                        "type": "boolean",
                        "description": "Se verdadeiro, inclui símbolos na senha.",
                    },
                },
                "required": ["comprimento"],
            },
        },
    },
]


def classificar_imc(imc):
    if imc < 18.5:
        return "abaixo do peso"
    if imc < 25:
        return "peso normal"
    if imc < 30:
        return "sobrepeso"
    if imc < 35:
        return "obesidade grau 1"
    if imc < 40:
        return "obesidade grau 2"
    return "obesidade grau 3"


def calcular_imc(peso, altura):
    peso = float(peso)
    altura = float(altura)

    if peso <= 0 or altura <= 0:
        raise ValueError("Peso e altura devem ser maiores que zero.")

    imc = peso / (altura ** 2)
    return {
        "peso": round(peso, 2),
        "altura": round(altura, 2),
        "imc": round(imc, 2),
        "classificacao": classificar_imc(imc),
    }


def gerar_senha(
    comprimento,
    incluir_maiusculas=True,
    incluir_numeros=True,
    incluir_simbolos=False,
):
    comprimento = int(comprimento)
    if comprimento < 4 or comprimento > 64:
        raise ValueError("O comprimento da senha deve estar entre 4 e 64 caracteres.")

    grupos = [string.ascii_lowercase]
    if incluir_maiusculas:
        grupos.append(string.ascii_uppercase)
    if incluir_numeros:
        grupos.append(string.digits)
    if incluir_simbolos:
        grupos.append("!@#$%&*?-_")

    caracteres_obrigatorios = [secrets.choice(grupo) for grupo in grupos]
    caracteres_disponiveis = "".join(grupos)

    senha = caracteres_obrigatorios[:]
    while len(senha) < comprimento:
        senha.append(secrets.choice(caracteres_disponiveis))

    secrets.SystemRandom().shuffle(senha)
    senha_final = "".join(senha[:comprimento])

    return {
        "senha": senha_final,
        "comprimento": comprimento,
        "criterios": {
            "minusculas": True,
            "maiusculas": incluir_maiusculas,
            "numeros": incluir_numeros,
            "simbolos": incluir_simbolos,
        },
    }


def execute_tool(tool_name, arguments):
    if tool_name == "calcular_imc":
        return calcular_imc(arguments["peso"], arguments["altura"])
    if tool_name == "gerar_senha":
        return gerar_senha(
            comprimento=arguments.get("comprimento", 12),
            incluir_maiusculas=arguments.get("incluir_maiusculas", True),
            incluir_numeros=arguments.get("incluir_numeros", True),
            incluir_simbolos=arguments.get("incluir_simbolos", False),
        )

    raise ValueError(f"Ferramenta não suportada: {tool_name}")
