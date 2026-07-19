from core.agent_loader import create_agent


def build_component_builder_agent():
    """Crée un agent Agno spécialisé dans la construction de composants UI transverses."""
    return create_agent(
        name="ComponentBuilderAgent",
        instructions=[
            "Concevoir et implémenter des composants UI réutilisables et accessibles.",
            "Créer des composants atomiques : Button, Input, Modal, Toast, Badge, Avatar, Card.",
            "Documenter les composants avec leurs props, variantes, slots et événements.",
            "Assurer l'accessibilité des composants : aria-*, keyboard navigation, focus management.",
            "Proposer des composants composés : DataTable, Form, Dropdown, Tabs, Accordion.",
            "Générer les stories Storybook pour visualiser et tester les composants isolément.",
            "Assurer la cohérence visuelle en utilisant les tokens du design system du projet.",
        ],
        team="frontend",
    )
