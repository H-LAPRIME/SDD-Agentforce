from core.agent_loader import create_agent


def build_redis_agent():
    """Crée un agent Agno spécialisé dans la gestion Redis pour le cache et les sessions."""
    return create_agent(
        name="RedisAgent",
        instructions=[
            "Implémenter des stratégies de cache Redis : cache-aside, write-through, write-behind.",
            "Utiliser les structures de données Redis : String, Hash, List, Set, Sorted Set, Stream.",
            "Configurer les TTL (Time To Live) et les politiques d'éviction Redis (LRU, LFU).",
            "Implémenter la gestion des sessions utilisateur avec Redis et des tokens de session sécurisés.",
            "Utiliser Redis Pub/Sub ou Redis Streams pour la communication inter-services en temps réel.",
            "Configurer Redis Cluster ou Redis Sentinel pour la haute disponibilité.",
            "Implémenter le rate limiting distribué avec Redis et le pattern sliding window.",
        ],
        team="db",
    )
