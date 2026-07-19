from core.agent_loader import create_agent


def build_readme_agent():
    """Crée un agent Agno spécialisé dans la génération de documentation README."""
    return create_agent(
        name="ReadmeAgent",
        instructions=[
            "Générer un README.md complet, clair et attrayant pour le projet.",
            "Inclure les sections essentielles : description, badges, installation, configuration, usage, contribution.",
            "Ajouter des exemples de code clairs et des captures d'écran si disponibles.",
            "Documenter les variables d'environnement requises avec des exemples.",
            "Inclure une section FAQ et Troubleshooting pour les problèmes courants.",
            "Proposer des badges GitHub (CI status, coverage, version, license) pour le README.",
            "Rédiger dans un style accessible, avec des liens vers la documentation complète.",
        ],
        team="doc",
    )
