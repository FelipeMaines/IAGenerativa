#RAG com Embeddings

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Inicializar modelo de embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

# Armazenar embeddings em memória
knowledge_embeddings = []
knowledge_chunks = []


def load_conhecimento():
    with open("projeto03/conhecimento/conhecimento.txt", "r", encoding="utf-8") as f:
        return f.read()


def gerar_embeddings(conhecimento):
    """
    Gera embeddings para o conhecimento e armazena em memória.
    Divide o conhecimento em chunks (padrágrafos) para maior granularidade.
    """
    global knowledge_embeddings, knowledge_chunks
    
    # Dividir o conhecimento em chunks (parágrafos)
    chunks = conhecimento.split("\n\n")
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]  # Remove vazios
    
    if not chunks:
        print("Aviso: Nenhum chunk de conhecimento encontrado.")
        return
    
    # Gerar embeddings para cada chunk
    print(f"Gerando embeddings para {len(chunks)} chunks de conhecimento...")
    embeddings = model.encode(chunks, convert_to_numpy=True)
    
    # Armazenar em memória
    knowledge_chunks = chunks
    knowledge_embeddings = embeddings
    
    print(f"✓ {len(chunks)} embeddings gerados e armazenados em memória")


def busca_similaridade(query, top_k=10):
    """
    Busca os trechos mais similares à query usando embeddings e similaridade cosseno.
    """
    # if not knowledge_embeddings or not knowledge_chunks:
    #     return "Desculpe, a base de conhecimento não foi carregada. Tente novamente mais tarde."
    
    # Gerar embedding da query
    query_embedding = model.encode([query], convert_to_numpy=True)
    
    # Calcular similaridade cosseno com todos os chunks
    similarities = cosine_similarity(query_embedding, knowledge_embeddings)[0]
    
    # Obter índices dos top_k resultados mais similares
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    # Montar resposta com trechos relevantes
    relevant_chunks = []
    for idx in top_indices:
        if similarities[idx] > 0.1:  # Threshold mínimo de similaridade
            relevant_chunks.append(knowledge_chunks[idx])
    
    if not relevant_chunks:
        return "Desculpe, não encontrei informações relevantes na base de conhecimento."
    
    return "\n\n".join(relevant_chunks)


def simple_retriever(query, conhecimento):
    """
    Função compatível com interface antiga - usa busca por similaridade.
    """
    return busca_similaridade(query)
