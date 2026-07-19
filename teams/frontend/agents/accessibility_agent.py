from core.agent_loader import create_agent


def build_accessibility_agent():
    """Cree un agent Agno specialise dans l'accessibilite frontend."""
    return create_agent(
        name="AccessibilityAgent",
        instructions=[
            "Auditer et ameliorer l'accessibilite WCAG des interfaces frontend.",
            "Verifier la hierarchie des titres, les landmarks HTML5, les labels de formulaires et les textes alternatifs.",
            "Garantir la navigation clavier: ordre de focus logique, etats focus visibles, echappement des modales et menus.",
            "Utiliser les roles ARIA uniquement quand le HTML semantique ne suffit pas.",
            "Verifier les contrastes, tailles de zones cliquables et etats d'erreur lisibles.",
            "Pour les composants interactifs, fournir les attributs aria-expanded, aria-controls, aria-current ou aria-invalid quand necessaire.",
            "Signaler les risques a11y bloquants et proposer directement le code corrige.",
        ],
        team="frontend",
    )
