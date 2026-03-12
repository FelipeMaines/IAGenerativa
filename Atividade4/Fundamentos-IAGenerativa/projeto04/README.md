# Projeto 04 - Assistente com Memoria

Este projeto evolui o chatbot base da disciplina com memoria controlada, persona fixa, uso de funcoes Python e persistencia local em JSON.

## Como executar

1. Instale as dependencias:

```bash
pip install -r requirements.txt
```

2. Crie um arquivo `.env` na pasta raiz do repositório ou na pasta do projeto com sua chave:

```env
GROQ_API_KEY=sua_chave_aqui
GROQ_MODEL=llama-3.1-8b-instant
```

3. Execute o chatbot:

```bash
python main.py
```

## Funcionalidades implementadas

- Comando `/limpar` para apagar o historico da conversa.
- Mensagem `Memória da conversa apagada.` exibida ao executar o comando.
- Persona do assistente com tom formal e profissional.
- Limite de memoria com as ultimas 10 mensagens da conversa.
- Persistencia do historico no arquivo `historico.json`.
- Carregamento automatico do historico ao reiniciar o programa.
- Integracao com ferramentas Python por meio de tool calling da OpenAI.
- Funcao para calcular IMC.
- Funcao para gerar senha aleatoria.

## Exemplos de uso

- `Calcule meu IMC com 72 kg e 1.75 m`
- `Gere uma senha segura com 16 caracteres e simbolos`
- `/limpar`

## Estrutura principal

- `main.py`: loop do chat, memoria, persistencia e integracao com o modelo.
- `tools.py`: definicao das ferramentas Python e schemas enviados para o modelo.
- `historico.json`: arquivo criado automaticamente para salvar o historico.

## Reflexoes

### Se o historico crescer muito, quais problemas podem ocorrer no uso de LLMs?

Historicos longos aumentam o consumo de tokens, elevam o custo da aplicacao, deixam as respostas mais lentas e podem reduzir a qualidade do contexto mais recente. Tambem existe o risco de informacoes antigas e pouco relevantes competirem com o que realmente importa na conversa atual.

### Por que algumas tarefas sao melhores resolvidas por funcoes Python do que pelo proprio LLM?

Funcoes Python sao mais adequadas para calculos, regras deterministicas e geracao controlada de resultados, porque entregam respostas reproduziveis e precisas. O LLM e melhor para linguagem natural e decisao contextual, mas nao deve substituir processamento estruturado quando a exatidao e importante.

### Quais riscos existem ao deixar que o LLM tome decisoes sobre quando usar uma funcao?

O modelo pode deixar de usar uma funcao quando deveria, usar a funcao errada ou interpretar parametros de forma incorreta. Por isso, e importante limitar as ferramentas disponiveis, validar argumentos, tratar erros e manter a resposta final supervisionada pelo fluxo da aplicacao.

## Dificuldades encontradas

O principal desafio foi integrar memoria persistente e tool calling sem complicar demais a estrutura original. Tambem foi necessario tomar cuidado para manter o historico enxuto, salvar apenas mensagens relevantes e tratar falhas de execucao sem interromper a conversa.