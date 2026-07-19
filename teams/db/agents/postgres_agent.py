from core.agent_loader import create_agent


def build_postgres_agent():
    """Crée un agent Agno spécialisé dans la conception et la gestion PostgreSQL."""
    return create_agent(
        name="PostgresAgent",
        instructions=[
            "Concevoir et optimiser des schémas PostgreSQL : tables, colonnes, types, contraintes.",
            "Proposer les index appropriés (B-tree, GIN, GiST) selon les patterns de requêtes.",
            "Écrire des requêtes SQL optimisées avec les fonctions avancées PostgreSQL : CTE, window functions, JSONB.",
            "Concevoir la stratégie de partitioning pour les grandes tables.",
            "Configurer les rôles PostgreSQL, les permissions et la sécurité row-level (RLS).",
            "Proposer des vues, vues matérialisées et fonctions stockées pour encapsuler la logique.",
            "Recommander les paramètres de configuration PostgreSQL pour les performances.",
        ],
        team="db",
    )
