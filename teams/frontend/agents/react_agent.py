from pathlib import Path
from agno.agent import Agent
from agno.skills import Skills, LocalSkills

from core.agent_loader import get_model_for_simple_frontend

# Chemin relatif vers le SKILL (ne casse pas si le projet est deplace)
_SKILL_PATH = Path(__file__).resolve().parent.parent.parent.parent / "skills" / "react18-batching-patterns" / "SKILL.md"


def _build_skills() -> Skills | None:
    """Charge le SKILL React18 si le fichier existe, sinon retourne None (pas de crash)."""
    if _SKILL_PATH.exists():
        return Skills(loaders=[LocalSkills(str(_SKILL_PATH))])
    return None


def build_react_agent(skip_tools: bool = True) -> Agent:
    """
    Cree un agent Agno specialise dans le developpement frontend React.

    Args:
        skip_tools: Si True (defaut), aucun outil MCP n'est charge. Gain de 5-15s
                    de latence sur les pages simples. Mettre a False uniquement pour
                    les projets fullstack qui ont besoin du filesystem MCP.
    """
    instructions = [
        # --- Format de sortie STRICT ---
        "Repondre UNIQUEMENT avec deux blocs markdown: ```html``` (index.html complet) et ```javascript``` (main.js). AUCUNE prose, AUCUNE explication, AUCUN autre bloc.",

        # --- INTERDICTION ABSOLUE des imports ES modules ---
        "INTERDIT ABSOLU: NE JAMAIS ecrire `import` ou `export` dans le bloc javascript. Ces mots-clefs CASSENT la page.",
        "INTERDIT ABSOLU: NE PAS ecrire `import React from 'react'`, ni `import { useState } from 'react'`, ni aucune forme d'import.",
        "React, ReactDOM, useState, useEffect etc. sont DEJA DISPONIBLES comme variables globales via les scripts UMD charges dans le HTML. Il SUFFIT d'ecrire: `const { useState, useEffect, useRef, useMemo, useCallback } = React;` en haut du fichier javascript.",
        "Exemple CORRECT debut de main.js: `const { useState, useEffect } = React;` puis directement le composant.",
        "Exemple INCORRECT a NE JAMAIS faire: `import React, { useState } from 'react';`",

        # --- HTML structure ---
        (
            "index.html doit avoir dans <head>: "
            "(1) <script src=\"https://unpkg.com/react@18/umd/react.development.js\"></script> "
            "(2) <script src=\"https://unpkg.com/react-dom@18/umd/react-dom.development.js\"></script> "
            "(3) <script src=\"https://cdn.tailwindcss.com\"></script> "
            "Et juste avant </body>: "
            "(4) <script src=\"https://unpkg.com/@babel/standalone@7.23.9/babel.min.js\"></script> "
            "(5) <script type=\"text/babel\" data-presets=\"react\" src=\"main.js\"></script>"
        ),

        # --- React 18 montage ---
        "Montage React 18 UNIQUEMENT: `const root = ReactDOM.createRoot(document.getElementById('root')); root.render(<App />);` — jamais ReactDOM.render (deprecie).",

        # --- Conventions React ---
        "Utiliser className (jamais class), htmlFor (jamais for), onClick (jamais onclick).",
        "NE PAS inclure de balise <meta http-equiv=\"Content-Security-Policy\">.",

        # --- Design premium ---
        "Creer une page professionnelle et visuellement riche avec Tailwind CSS: hero avec gradient, sections distincts, cartes avec ombres, boutons stylises, typographie claire, 100% responsive mobile-first.",
        "Utiliser des images reelles Unsplash (https://images.unsplash.com/photo-XXXXX?w=800) avec loading=lazy et alt text. Jamais via.placeholder.com.",
        "Ajouter des transitions CSS smooth sur les hover (transition-all duration-300).",
        "Assurer a11y: attributs aria-label, role, titres h1->h6 hierarchises, contrastes WCAG AA.",
    ]

    skills = _build_skills()
    skill_kwargs = {"skills": skills} if skills else {}

    return Agent(
        name="ReactAgent",
        model=get_model_for_simple_frontend(),
        instructions=instructions,
        markdown=True,
        debug_mode=True,
        **skill_kwargs,
    )