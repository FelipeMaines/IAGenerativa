"""
Script de testes para validar o classificador em nível de produção.
Executa múltiplas repetições com diferentes temperaturas.
"""

import json
from datetime import datetime
from classifier import classificar_mensagem


# Mensagens de teste
MENSAGENS_TESTE = [
    "O sistema está com erro",
    "Quero cancelar minha assinatura",
    "Vocês trabalham no sábado"
]

# Temperaturas a testar
TEMPERATURAS = [0.1, 0.5, 0.9]

# Número de repetições
NUM_REPETICOES = 10


def run_tests():
    """
    Executa testes com múltiplas repetições e temperaturas.
    """
    resultados = {
        "timestamp": datetime.now().isoformat(),
        "mensagens_testadas": len(MENSAGENS_TESTE),
        "repeticoes": NUM_REPETICOES,
        "temperaturas": TEMPERATURAS,
        "resultados_por_temperatura": {}
    }
    
    print("=" * 70)
    print("🧪 INICIANDO TESTES DO CLASSIFICADOR")
    print("=" * 70)
    print(f"Data/Hora: {resultados['timestamp']}")
    print(f"Mensagens: {len(MENSAGENS_TESTE)}")
    print(f"Repetições por mensagem: {NUM_REPETICOES}")
    print(f"Temperaturas: {TEMPERATURAS}")
    print("=" * 70)
    
    for temperatura in TEMPERATURAS:
        print(f"\n🌡️  TESTANDO COM TEMPERATURA: {temperatura}")
        print("-" * 70)
        
        resultados_temp = {
            "temperatura": temperatura,
            "total_testes": len(MENSAGENS_TESTE) * NUM_REPETICOES,
            "testes_por_mensagem": {},
            "estatisticas": {}
        }
        
        categorias_encontradas = {}
        
        for mensagem in MENSAGENS_TESTE:
            print(f"\n📝 Mensagem: '{mensagem}'")
            resultados_msg = {
                "categorias": [],
                "contagem": {}
            }
            
            for repeticao in range(1, NUM_REPETICOES + 1):
                categoria = classificar_mensagem(mensagem, temperature=temperatura)
                resultados_msg["categorias"].append(categoria)
                
                if categoria not in resultados_msg["contagem"]:
                    resultados_msg["contagem"][categoria] = 0
                resultados_msg["contagem"][categoria] += 1
                
                if categoria not in categorias_encontradas:
                    categorias_encontradas[categoria] = 0
                categorias_encontradas[categoria] += 1
                
                print(f"   Repetição {repeticao:2d}: {categoria}")
            
            # Calcula estatísticas por mensagem
            categoria_mais_frequente = max(resultados_msg["contagem"].items(), key=lambda x: x[1])[0]
            consistencia = (resultados_msg["contagem"][categoria_mais_frequente] / NUM_REPETICOES) * 100
            
            resultados_msg["categoria_mais_frequente"] = categoria_mais_frequente
            resultados_msg["consistencia_percentual"] = round(consistencia, 2)
            resultados_msg["variacao"] = len(resultados_msg["contagem"])
            
            print(f"   ✓ Categoria mais frequente: {categoria_mais_frequente}")
            print(f"   ✓ Consistência: {consistencia:.1f}%")
            print(f"   ✓ Variação: {len(resultados_msg['contagem'])} categoria(s) diferente(s)")
            
            resultados_temp["testes_por_mensagem"][mensagem] = resultados_msg
        
        # Estatísticas gerais da temperatura
        resultados_temp["estatisticas"]["categorias_encontradas"] = categorias_encontradas
        resultados_temp["estatisticas"]["consistencia_media"] = round(
            sum([msg["consistencia_percentual"] for msg in resultados_temp["testes_por_mensagem"].values()]) / len(MENSAGENS_TESTE),
            2
        )
        resultados_temp["estatisticas"]["variacao_media"] = round(
            sum([msg["variacao"] for msg in resultados_temp["testes_por_mensagem"].values()]) / len(MENSAGENS_TESTE),
            2
        )
        
        resultados["resultados_por_temperatura"][str(temperatura)] = resultados_temp
        
        print(f"\n📊 Resumo para temperatura {temperatura}:")
        print(f"   Consistência média: {resultados_temp['estatisticas']['consistencia_media']:.2f}%")
        print(f"   Variação média: {resultados_temp['estatisticas']['variacao_media']:.2f} categorias")
        print(f"   Categorias encontradas: {dict(resultados_temp['estatisticas']['categorias_encontradas'])}")
    
    print("\n" + "=" * 70)
    print("✅ TESTES CONCLUÍDOS")
    print("=" * 70)
    
    return resultados


def salvar_resultados(resultados, filename="teste_resultados.json"):
    """
    Salva os resultados em um arquivo JSON.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"\n📁 Resultados salvos em: {filename}")


if __name__ == "__main__":
    resultados = run_tests()
    salvar_resultados(resultados)
