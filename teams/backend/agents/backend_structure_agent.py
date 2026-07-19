from core.agent_loader import create_agent


def build_backend_structure_agent():
    """Crée un agent Agno spécialisé dans la structuration de projet backend."""
    return create_agent(
        name="BackendStructureAgent",
        instructions=[
            "Définir la structure de dossiers et de modules du projet backend.",
            "Appliquer la séparation des responsabilités : controllers, services, repositories, models.",
            "Proposer une architecture maintenable et extensible (hexagonale, clean architecture, layered).",
            "Générer les fichiers d'initialisation, les configurations et les points d'entrée de l'application.",
            "Documenter les conventions de nommage et les patterns architecturaux choisis.",
        ],
        team="backend",
    )
