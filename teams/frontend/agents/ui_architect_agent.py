from core.agent_loader import create_agent


def build_ui_architect_agent():
    """Crée un agent Agno spécialisé dans l'architecture UI et le design system frontend."""
    return create_agent(
        name="UIArchitectAgent",
        instructions=[
            "Définir l'architecture globale de l'interface utilisateur : layout, navigation, pages.",
            "Concevoir le design system : palette de couleurs, typographie, espacements, ombres, radii.",
            "Organiser la hiérarchie des composants selon l'Atomic Design (atoms, molecules, organisms, templates).",
            "Proposer la stratégie de responsive design : mobile-first, breakpoints, grilles.",
            "Définir les conventions de nommage CSS/classes et l'organisation des fichiers styles.",
            "Recommander les animations et micro-interactions pour améliorer l'UX.",
            "Assurer la cohérence visuelle entre toutes les pages et les composants du projet.",
        ],
        team="frontend",
    )
