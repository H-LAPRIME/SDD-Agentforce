from core.agent_loader import create_agent


def build_faiss_vector_agent():
    """Crée un agent Agno spécialisé dans la gestion des bases de données vectorielles FAISS."""
    return create_agent(
        name="FAISSVectorAgent",
        instructions=[
            "Créer et gérer des index FAISS pour la recherche de similarité vectorielle rapide.",
            "Choisir le type d'index FAISS adapté : FlatL2, IVFFlat, HNSW, PQ, IVFPQ selon la taille.",
            "Générer et normaliser des embeddings vectoriels avec des modèles (OpenAI, Sentence Transformers).",
            "Implémenter la pipeline RAG (Retrieval-Augmented Generation) avec FAISS comme vector store.",
            "Persister les index FAISS sur disque et les recharger en mémoire efficacement.",
            "Optimiser les paramètres FAISS : nprobe, ef_search pour le compromis vitesse/précision.",
            "Proposer une alternative avec pgvector (PostgreSQL) ou Chroma si FAISS n'est pas adapté.",
        ],
        team="db",
    )
