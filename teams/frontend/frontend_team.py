from agno.team import Team
from agno.team.mode import TeamMode

from core.agent_loader import get_model
from core.config import RUN_PROFILE
from teams.frontend.agents.react_agent import build_react_agent
from teams.frontend.agents.tailwind_agent import build_tailwind_agent
from teams.frontend.agents.ui_architect_agent import build_ui_architect_agent
from teams.frontend.agents.next_agent import build_next_agent
from teams.frontend.agents.angular_agent import build_angular_agent
from teams.frontend.agents.component_builder_agent import build_component_builder_agent
from teams.frontend.agents.state_management_agent import build_state_management_agent
from teams.frontend.agents.form_handling_agent import build_form_handling_agent
from teams.frontend.agents.seo_agent import build_seo_agent
from teams.frontend.agents.i18n_agent import build_i18n_agent
from teams.frontend.agents.accessibility_agent import build_accessibility_agent
from teams.frontend.agents.visual_qa_agent import build_visual_qa_agent
from teams.frontend.agents.api_integration_agent import build_frontend_api_integration_agent
from teams.frontend.agents.nodejs_agent import build_nodejs_agent
from teams.frontend.agents.bootstrap_agent import build_bootstrap_agent
from teams.frontend.agents.django_agent import build_django_frontend_agent
from teams.frontend.agents.express_agent import build_express_frontend_agent


def build_frontend_team() -> Team:
    """
    Build the Agno team focused on frontend delivery.

    En mode 'fast', seuls les agents essentiels sont charges (3 agents)
    pour reduire considerablement la latence de demarrage.
    En mode 'quality' ou 'full', tous les agents specialises sont inclus.
    """
    if RUN_PROFILE == "fast":
        # Mode rapide : 3 agents core suffisants pour la majorite des projets frontend
        members = [
            build_ui_architect_agent(),
            build_react_agent(skip_tools=True),
            build_tailwind_agent(),
        ]
        instructions_extra = [
            "En mode fast, prioriser la simplicite et la rapidite de livraison.",
        ]
    else:
        # Mode quality/full : equipe complete
        members = [
            build_ui_architect_agent(),
            build_react_agent(),
            build_next_agent(),
            build_angular_agent(),
            build_component_builder_agent(),
            build_state_management_agent(),
            build_form_handling_agent(),
            build_seo_agent(),
            build_i18n_agent(),
            build_accessibility_agent(),
            build_visual_qa_agent(),
            build_frontend_api_integration_agent(),
            build_tailwind_agent(),
            build_nodejs_agent(),
            build_bootstrap_agent(),
            build_django_frontend_agent(),
            build_express_frontend_agent(),
        ]
        instructions_extra = []

    return Team(
        name="Frontend Engineering Team",
        description="Equipe Agno specialisee dans la conception, l'implementation et la verification frontend.",
        mode=TeamMode.route,
        model=get_model(role="team", team="frontend"),
        members=members,
        instructions=[
            "Selectionne l'agent le plus adapte pour produire le frontend final, puis applique les controles VisualQAAgent et AccessibilityAgent avant de repondre." if RUN_PROFILE != "fast" else "Selectionne l'agent le plus adapte et produis le frontend directement.",
            "Pour une landing page simple, retourner preferentiellement deux blocs markdown: ```html``` pour index.html et ```javascript``` pour main.js.",
            "Ne pas gerer toi-meme l'ordre ou le contenu des balises <script> de chargement (React/ReactDOM/Tailwind/Babel).",
            "Verifier le runtime avant sortie: root DOM present, ordre des scripts correct, assets critiques valides, CSP compatible.",
            "Appliquer un niveau UI professionnel: responsive mobile/tablette/desktop, espacements stables, images reelles avec alt text.",
            "Ne pas retourner de plan ni de prose longue; retourner uniquement le code final dans les blocs markdown adaptes.",
            *instructions_extra,
        ],
        markdown=True,
    )
