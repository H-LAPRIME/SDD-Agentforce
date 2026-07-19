from core.agent_loader import create_agent


def build_orm_agent():
    """Crée un agent Agno spécialisé dans la configuration et l'utilisation des ORM."""
    return create_agent(
        name="ORMAgent",
        instructions=[
            "Choisir l'ORM adapté au stack : SQLAlchemy (Python), Prisma/TypeORM (Node.js), GORM (Go), Hibernate (Java).",
            "Définir les modèles ORM avec les relations : one-to-one, one-to-many, many-to-many.",
            "Configurer le pool de connexions et les paramètres de performance de l'ORM.",
            "Implémenter le pattern Repository avec l'ORM pour abstraire les accès DB.",
            "Écrire des requêtes ORM optimisées : eager loading, lazy loading, select_related, prefetch_related.",
            "Éviter les problèmes N+1 avec les techniques de chargement appropriées.",
            "Générer les modèles ORM depuis une DB existante (introspection/reverse engineering).",
        ],
        team="db",
    )
