"""
Script para gerar relatório comparativo em Markdown dos testes.
"""

import json
from datetime import datetime


def gerar_relatorio(arquivo_json="teste_resultados.json", arquivo_saida="RELATORIO_TESTES.md"):
    """
    Gera um relatório Markdown a partir dos resultados dos testes.
    """
    try:
        with open(arquivo_json, "r", encoding="utf-8") as f:
            resultados = json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo {arquivo_json} não encontrado. Execute test_classifier.py primeiro.")
        return
    
    # Cria o relatório
    relatorio = []
    relatorio.append("# 📋 Relatório Comparativo - Classificador Production Ready")
    relatorio.append("")
    relatorio.append(f"**Data/Hora:** {resultados.get('timestamp', 'N/A')}")
    relatorio.append(f"**Mensagens testadas:** {resultados.get('mensagens_testadas', 0)}")
    relatorio.append(f"**Repetições por mensagem:** {resultados.get('repeticoes', 0)}")
    relatorio.append("")
    relatorio.append("---")
    relatorio.append("")
    
    # Resumo executivo
    relatorio.append("## 📊 Resumo Executivo")
    relatorio.append("")
    
    temps_dados = resultados.get("resultados_por_temperatura", {})
    if temps_dados:
        relatorio.append("### Consistência por Temperatura")
        relatorio.append("")
        relatorio.append("| Temperatura | Consistência Média | Variação Média |")
        relatorio.append("|-------------|-------------------|----------------|")
        
        for temp, dados in sorted(temps_dados.items(), key=lambda x: float(x[0])):
            stats = dados.get("estatisticas", {})
            consistencia = stats.get("consistencia_media", "N/A")
            variacao = stats.get("variacao_media", "N/A")
            relatorio.append(f"| {temp} | {consistencia}% | {variacao} |")
        
        relatorio.append("")
        
        # Análise comparativa
        relatorio.append("## 🔍 Análise Comparativa")
        relatorio.append("")
        
        temps_lista = sorted(temps_dados.items(), key=lambda x: float(x[0]))
        temp_menor = float(temps_lista[0][0])
        temp_maior = float(temps_lista[-1][0])
        
        consistencia_menor = temps_dados[str(temp_menor)]["estatisticas"]["consistencia_media"]
        consistencia_maior = temps_dados[str(temp_maior)]["estatisticas"]["consistencia_media"]
        
        relatorio.append(f"### Temperatura Baixa vs Alta")
        relatorio.append("")
        relatorio.append(f"- **Temperatura {temp_menor}** (Baixa - Mais determinística)")
        relatorio.append(f"  - Consistência: {consistencia_menor}%")
        relatorio.append(f"  - Categorias encontradas: {temps_dados[str(temp_menor)]['estatisticas']['categorias_encontradas']}")
        relatorio.append("")
        relatorio.append(f"- **Temperatura {temp_maior}** (Alta - Mais criativa)")
        relatorio.append(f"  - Consistência: {consistencia_maior}%")
        relatorio.append(f"  - Categorias encontradas: {temps_dados[str(temp_maior)]['estatisticas']['categorias_encontradas']}")
        relatorio.append("")
        
        diferenca = abs(consistencia_menor - consistencia_maior)
        relatorio.append(f"**Diferença de consistência:** {diferenca:.2f}%")
        relatorio.append("")
    
    # Testes detalhados
    relatorio.append("## 📝 Resultados Detalhados")
    relatorio.append("")
    
    for temp, dados in sorted(temps_dados.items(), key=lambda x: float(x[0])):
        relatorio.append(f"### Temperatura: {temp}")
        relatorio.append("")
        
        testes = dados.get("testes_por_mensagem", {})
        for mensagem, resultado in testes.items():
            relatorio.append(f"**Mensagem:** \"{mensagem}\"")
            relatorio.append("")
            relatorio.append(f"- **Categoria mais frequente:** {resultado.get('categoria_mais_frequente', 'N/A')}")
            relatorio.append(f"- **Consistência:** {resultado.get('consistencia_percentual', 'N/A')}%")
            relatorio.append(f"- **Variação:** {resultado.get('variacao', 0)} categoria(s)")
            relatorio.append("")
            
            # Distribuição de categorias
            contagem = resultado.get("contagem", {})
            if contagem:
                relatorio.append("  **Distribuição:**")
                for categoria, count in sorted(contagem.items(), key=lambda x: x[1], reverse=True):
                    pct = (count / resultado.get('consistencia_percentual', 100) * 100) if resultado.get('consistencia_percentual', 0) > 0 else 0
                    relatorio.append(f"  - {categoria}: {count}x (≈{pct:.0f}%)")
                relatorio.append("")
        
        relatorio.append("---")
        relatorio.append("")
    
    # Conclusões e recomendações
    relatorio.append("## 💡 Conclusões e Recomendações")
    relatorio.append("")
    
    melhor_temp = max(temps_dados.items(), key=lambda x: x[1]["estatisticas"]["consistencia_media"])
    relatorio.append(f"### Temperatura Recomendada em Produção")
    relatorio.append("")
    relatorio.append(f"**Temperatura {melhor_temp[0]}** apresenta a melhor consistência ({melhor_temp[1]['estatisticas']['consistencia_media']}%)")
    relatorio.append("")
    
    relatorio.append("### Pontos Fortes da Implementação")
    relatorio.append("")
    relatorio.append("✅ **Parser JSON robusto** - Trata erros de parsing com graciosidade")
    relatorio.append("✅ **Validação de categorias** - Garante que apenas categorias permitidas são retornadas")
    relatorio.append("✅ **Fallback seguro** - Utiliza categoria 'Geral' quando validação falha")
    relatorio.append("✅ **Logging detalhado** - Facilita diagnóstico de problemas")
    relatorio.append("✅ **Tratamento de exceções** - Captura erros inesperados")
    relatorio.append("")
    
    relatorio.append("### Recomendações para Produção")
    relatorio.append("")
    relatorio.append("1. **Usar temperatura baixa** (0.1) para maior consistência")
    relatorio.append("2. **Monitorar fallbacks** - Registrar quando categoria 'Geral' é usada")
    relatorio.append("3. **Audit trail** - Manter logs de todas as classificações para análise")
    relatorio.append("4. **Testes periódicos** - Executar este script regularmente para validar performance")
    relatorio.append("5. **Versioning** - Manter histórico de mudanças no prompt do classificador")
    relatorio.append("")
    
    # Metadados
    relatorio.append("---")
    relatorio.append("")
    relatorio.append(f"*Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}*")
    
    # Salva o relatório
    conteudo_final = "\n".join(relatorio)
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        f.write(conteudo_final)
    
    print(f"✅ Relatório gerado com sucesso: {arquivo_saida}")
    print("")
    print("=" * 70)
    print(conteudo_final)
    print("=" * 70)


if __name__ == "__main__":
    gerar_relatorio()
