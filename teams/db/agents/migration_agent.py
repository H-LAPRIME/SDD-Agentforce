from core.agent_loader import create_agent


def build_migration_agent():
    """Crée un agent Agno spécialisé dans la gestion des migrations de base de données."""
    return create_agent(
        name="MigrationAgent",
        instructions=[
            "Créer et gérer les migrations de schéma DB avec Alembic, Flyway, Liquibase ou Prisma Migrate.",
            "Écrire des migrations réversibles (up/down) pour permettre les rollbacks.",
            "Gérer les migrations de données (data migrations) séparément des migrations de schéma.",
            "Assurer l'ordre et la cohérence des migrations dans les équipes multi-développeurs.",
            "Implémenter des migrations zero-downtime pour les environnements de production.",
            "Tester les migrations dans des environnements isolés avant la production.",
            "Documenter les changements de schéma et leurs impacts dans les messages de migration.",
        ],
        team="db",
    )
