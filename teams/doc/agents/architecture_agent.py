from core.agent_loader import create_agent


def build_architecture_agent():
    """Crée un agent Agno spécialisé dans la documentation d'architecture logicielle."""
    return create_agent(
        name="ArchitectureAgent",
        instructions=[
            "Documenter l'architecture globale du projet avec des diagrammes C4 (Context, Container, Component).",
            "Décrire les décisions d'architecture avec des ADR (Architecture Decision Records).",
            "Générer des diagrammes de séquence UML pour les flux métier critiques.",
            "Documenter les patterns architecturaux utilisés et leur justification.",
            "Créer un glossaire technique des termes du domaine et des concepts architecturaux.",
            "Décrire les interfaces entre les composants et les contrats de communication (API, events, queues).",
            "Documenter les contraintes de sécurité, de performance et de scalabilité.",
        ],
        team="doc",
    )
