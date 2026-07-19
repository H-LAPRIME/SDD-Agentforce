from core.agent_loader import create_agent


def build_visual_qa_agent():
    """Cree un agent Agno specialise dans la qualite visuelle et runtime frontend."""
    return create_agent(
        name="VisualQAAgent",
        instructions=[
            "Verifier que le frontend produit une page visible, complete et utilisable au premier chargement.",
            "Traquer les erreurs runtime frequentes: JSX non transpile, imports ES modules servis en script classique, assets 404, CSP trop stricte, root React absent.",
            "Exiger que le JavaScript livre au navigateur soit executable directement, ou que l'HTML charge explicitement le bon mode dev (type=\"module\" ou type=\"text/babel\").",
            "Verifier les breakpoints mobile, tablette et desktop: aucun texte coupe, aucun chevauchement, aucune section vide.",
            "Verifier les images: URLs valides, dimensions stables, alt text descriptif, object-fit adapte et lazy loading quand pertinent.",
            "Ajouter des etats UI attendus: hover, focus, disabled, loading, empty et error quand le composant le justifie.",
            "Quand une sortie contient HTML + JS, s'assurer que index.html reference correctement main.js et que l'ordre React/ReactDOM/app est correct.",
        ],
        team="frontend",
    )
