from classifier import classificar_mensagem

mensagens_cliente = [
    "Quero contratar o plano premium",
    "O sistema está com erro",
    "Quero cancelar minha assinatura",
    "Quero falar com um atendente",
    "Preciso de ajuda com meu pagamento",
    "Gostaria de atualizar minhas informações de conta",
    "Vocês trabalham no sábado"
]

for mensagem in mensagens_cliente:
    resposta = classificar_mensagem(mensagem)
    print(f"Cliente: {mensagem}")
    print(f"Resposta: {resposta}\n")
