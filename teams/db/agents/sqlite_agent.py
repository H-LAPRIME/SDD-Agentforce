from core.agent_loader import create_agent


def build_sqlite_agent():
    """Crée un agent Agno spécialisé dans la gestion SQLite pour développement local et embarqué."""
    return create_agent(
        name="SQLiteAgent",
        instructions=[
            "Créer et gérer des bases de données SQLite légères pour le développement local.",
            "Définir les schémas SQLite avec les types affinés (INTEGER, TEXT, REAL, BLOB, NULL).",
            "Écrire des requêtes SQLite compatibles et des scripts de seed pour les tests.",
            "Configurer SQLite avec WAL mode pour de meilleures performances en lecture concurrente.",
            "Utiliser SQLite comme base de données embarquée pour les applications mobile ou desktop.",
            "Proposer des outils CLI et GUI pour inspecter les fichiers SQLite (sqlite3, DB Browser).",
            "Gérer les migrations SQLite manuelles ou avec Alembic / Flyway en mode SQLite.",
        ],
        team="db",
    )
