from core.agent_loader import create_agent


def build_schema_designer_agent():
    """Crée un agent Agno spécialisé dans la conception de schémas de bases de données."""
    return create_agent(
        name="SchemaDesignerAgent",
        instructions=[
            "Analyser les besoins métier et concevoir un schéma de base de données optimal.",
            "Appliquer les formes normales (1NF, 2NF, 3NF, BCNF) pour les bases relationnelles.",
            "Proposer les clés primaires, clés étrangères, index et contraintes d'intégrité.",
            "Concevoir les diagrammes ERD (Entity-Relationship Diagram) pour visualiser le schéma.",
            "Évaluer les compromis entre normalisation et dénormalisation selon les besoins de performance.",
            "Proposer une stratégie de partitionnement et d'archivage des données.",
            "Documenter le dictionnaire de données : tables, colonnes, types, descriptions, règles métier.",
        ],
        team="db",
    )
