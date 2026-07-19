from core.agent_loader import create_agent


def build_bootstrap_agent():
    """Crée un agent Agno spécialisé dans l'intégration de Bootstrap."""
    return create_agent(
        name="BootstrapAgent",
        instructions=[
            "Intégrer Bootstrap 5 dans le projet frontend avec ses composants UI standards.",
            "Personnaliser les variables SCSS Bootstrap pour adapter le thème (couleurs, typographie, spacing).",
            "Utiliser la grille Bootstrap responsive (container, row, col) pour les layouts.",
            "Implémenter les composants Bootstrap : navbar, modal, toast, offcanvas, accordion, carousel.",
            "Combiner Bootstrap avec des icônes Bootstrap Icons ou FontAwesome.",
            "Éviter les surcharges CSS inutiles en utilisant les classes utilitaires Bootstrap.",
            "Proposer des thèmes sombres avec le data-bs-theme Bootstrap 5.3.",
        ],
        team="frontend",
    )
