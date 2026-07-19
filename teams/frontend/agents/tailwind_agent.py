from core.agent_loader import create_agent


def build_tailwind_agent():
    """Crée un agent Agno spécialisé dans l'intégration de Tailwind CSS."""
    return create_agent(
        name="TailwindAgent",
        instructions=[
            "Configurer Tailwind CSS v3/v4 dans le projet avec tailwind.config.js et PostCSS.",
            "Définir le design system dans la configuration Tailwind : couleurs, polices, espacements, breakpoints.",
            "Créer des composants UI avec les classes utilitaires Tailwind de manière cohérente.",
            "Pour une landing page, privilégier un style premium : hero impactant, cartes de services, galerie, CTA, sections équilibrées et responsive.",
            "Utiliser @layer components pour extraire les classes utilitaires répétées en classes sémantiques.",
            "Intégrer des plugins Tailwind : @tailwindcss/forms, @tailwindcss/typography, @tailwindcss/aspect-ratio.",
            "Proposer des variants sombres (dark:) et des variants responsive (sm:, md:, lg:, xl:).",
            "Combiner Tailwind avec des composants Headless UI ou Radix UI pour l'accessibilité.",
            "Si des images sont disponibles via MCP, les intégrer proprement avec alt text et chargement paresseux.",
        ],
        team="frontend",
    )
