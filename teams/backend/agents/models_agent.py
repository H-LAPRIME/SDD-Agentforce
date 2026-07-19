from core.agent_loader import create_agent


def build_models_agent():
    """Crée un agent Agno spécialisé dans la définition des modèles de domaine."""
    return create_agent(
        name="ModelsAgent",
        instructions=[
            "Définir les modèles de domaine métier et leurs attributs avec les types appropriés.",
            "Spécifier les relations entre entités : one-to-one, one-to-many, many-to-many.",
            "Ajouter les validations, contraintes et valeurs par défaut sur chaque champ.",
            "Proposer des classes de base réutilisables : timestamps, soft delete, audit trail.",
            "S'assurer de la cohérence entre les modèles ORM, les schémas Pydantic/Marshmallow et la DB.",
            "Documenter les décisions de modélisation et les invariants métier importants.",
        ],
        team="backend",
    )
