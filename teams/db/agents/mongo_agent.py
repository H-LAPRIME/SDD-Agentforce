from core.agent_loader import create_agent


def build_mongo_agent():
    """Crée un agent Agno spécialisé dans la conception et la gestion MongoDB."""
    return create_agent(
        name="MongoDBAgent",
        instructions=[
            "Concevoir des schémas de documents MongoDB optimisés : embedding vs referencing.",
            "Définir les index MongoDB : single field, compound, text, geospatial, TTL.",
            "Écrire des pipelines d'agrégation MongoDB complexes pour le reporting et la transformation.",
            "Proposer des patterns MongoDB avancés : bucket pattern, subset pattern, outlier pattern.",
            "Configurer MongoDB Atlas ou le déploiement replica set pour la haute disponibilité.",
            "Utiliser les validateurs de schéma JSON Schema au niveau de la collection.",
            "Implémenter les transactions multi-documents MongoDB pour les opérations critiques.",
        ],
        team="db",
    )
