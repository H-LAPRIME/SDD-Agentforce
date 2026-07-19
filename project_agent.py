import sys
import ssl
import os
import re
import io
import time
import json
import yaml
import threading
import webbrowser
import http.server
import socketserver
import concurrent.futures
from functools import partial
from pathlib import Path

from agno.team.mode import TeamMode

# ── Fix encodage Windows ─────────────────────────────────────────────────────
# Windows utilise cp1252 par defaut : les caracteres non-latins (chinois, emoji...)
# generes par certains modeles (Qwen, etc.) crashent le logger Rich et les print().
# On force UTF-8 avant tout import de librairie.
os.environ.setdefault("PYTHONUTF8", "1")  # affecte aussi les sous-processus
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass  # lecture seule ou non-TTY : on continue sans crash

# Desactive la verification SSL pour les appels de telemetrie Agno (session saver)
# Necessaire dans les reseaux avec proxy corporate (Capgemini)
ssl._create_default_https_context = ssl._create_unverified_context
os.environ.setdefault("AGNO_TELEMETRY", "false")


def _safe_print(text: str) -> None:
    """Affiche du texte en remplacant les caracteres non-encodables (evite UnicodeEncodeError)."""
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8", errors="replace"))

from agno.agent import Agent
from agno.run.team import RunStatus

from core.config import MODEL_CONFIG, RUN_PROFILE
from core.agent_loader import get_model
from teams.backend.backend_team import build_backend_team
from teams.frontend.frontend_team import build_frontend_team
from teams.frontend.agents.react_agent import build_react_agent
from teams.db.db_team import build_db_team
from teams.test.test_team import build_test_team
from teams.doc.doc_team import build_doc_team
from teams.devops.devops_team import build_devops_team
from teams.security.security_team import build_security_team
from core.spec_bridge import build_team_brief, group_tasks_by_team, mark_tasks_completed, parse_tasks, tasks_summary


# ---------------------------------------------------------------------------
# Regex precompiles (evite la recompilation a chaque appel de fonction)
# ---------------------------------------------------------------------------

_CODE_BLOCK_RE = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)

_JSX_PATTERNS = [
    re.compile(r"ReactDOM\.render\s*\(\s*<"),
    re.compile(r"return\s*\(\s*<"),
    re.compile(r"=>\s*\(\s*<"),
    re.compile(r"<[A-Z][A-Za-z0-9]*(\s|>|/|\.)"),
    re.compile(r"<[a-z][a-z0-9-]*(\s[^>]*(className|onClick|onChange)=|/>)"),
    re.compile(r"createElement\s*\(\s*['\"][A-Z]"),
]
_REACT_ATTRS_RE = re.compile(
    r'\b(className|htmlFor|onClick|onChange|onSubmit|onFocus|onBlur|'
    r'dangerouslySetInnerHTML|onMouseEnter|onMouseLeave)\s*='
)
_REACT_FRAGMENT_RE = re.compile(r'<React\.\w+')
_REACT_REF_RE = re.compile(r'\bReact\b')
_ANGLE_TAG_RE = re.compile(r'<[a-zA-Z][a-zA-Z0-9]*(\s|>|/>)')

_IMPORT_LINE_RE = re.compile(r'^\s*import\s[^;]*;\s*$', re.MULTILINE)
_EXPORT_LINE_RE = re.compile(r'^\s*export\s+', re.MULTILINE)
_HAS_IMPORT_RE = re.compile(r'^\s*import\s+', re.MULTILINE)
_HAS_EXPORT_RE = re.compile(r'^\s*export\s+', re.MULTILINE)
# Patterns pour stripper specifiquement les imports React (souvent generes meme avec les consignes)
_REACT_IMPORT_RE = re.compile(
    r'^\s*import\s+.*?[Rr]eact.*?;?\s*$',
    re.MULTILINE
)
# Import generique sur plusieurs styles (avec ou sans point-virgule)
_ANY_IMPORT_RE = re.compile(
    r'^[ \t]*import\b[^\n]*(?:\n|$)',
    re.MULTILINE
)
_ANY_EXPORT_DEFAULT_RE = re.compile(
    r'^[ \t]*export\s+default\s+',
    re.MULTILINE
)

_REACT17_RE = re.compile(r'react@17(\.[^/]*)?/umd/')
_REACT_DOM17_RE = re.compile(r'react-dom@17(\.[^/]*)?/umd/')

_MAIN_SCRIPT_TAG_RE = re.compile(
    r'\s*<script[^>]+src=["\']main\.js["\'][^>]*>\s*</script>', re.IGNORECASE
)
_SCRIPT_SRC_ATTR_RE = re.compile(r'(script-src\s+)([^;]+)')

_SIMPLE_FRONTEND_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in (
        r"landing[\s\-]?page",
        r"home[\s\-]?page",
        r"homepage",
        r"simple[\s\-]*site",
        r"frontend[\s\-]*only",
        r"page[\s\-]d.accueil",
        r"site[\s\-]*vitrine",
        r"portfolio",
        r"page[\s\-]*web",
        r"site[\s\-]*statique",
        r"static[\s\-]*site",
        r"page[\s\-]*principale",
        r"one[\s\-]?page",
        r"single[\s\-]?page",
        r"page[\s\-]*d.?entreprise",
        r"corporate[\s\-]*page",
        r"vitrine",
        r"showcase",
    )
]


# ---------------------------------------------------------------------------
# Extraction stack / env
# ---------------------------------------------------------------------------

def get_extractor_model():
    """Modele LLM dedie a l'extraction."""
    return get_model(role="router")


def _extract_first_json_object(text: str):
    """
    Isole le premier objet JSON valide dans une chaine, meme si le modele
    ajoute du texte avant/apres malgre la consigne stricte. Gere les
    accolades imbriquees et les accolades a l'interieur de chaines.
    """
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None  # objet jamais ferme -> reponse tronquee


def extract_stack_and_env(prompt: str) -> dict:
    """Analyse le prompt de l'utilisateur pour extraire les technos et les credentials."""
    transverse_default = "false" if RUN_PROFILE == "fast" else "true"
    extraction_agent = Agent(
        name="ExtractionAgent",
        model=get_extractor_model(),
        instructions=[
            "Tu es un expert DevOps et un architecte logiciel.",
            "Ta seule tache est d'analyser le texte de l'utilisateur et d'en extraire un JSON strict avec deux cles: 'stack' et 'env'.",
            "La cle 'stack' doit contenir un objet avec: 'frontend' (ex: react, angular), 'backend' (ex: fastapi, express), 'database' (ex: postgresql, mongodb).",
            f"Ajoute aussi dans 'stack' les booleens: 'test' ({transverse_default} par defaut), 'devops' ({transverse_default} par defaut), 'doc' ({transverse_default} par defaut), 'security' ({transverse_default} par defaut).",
            "Si l'utilisateur demande explicitement de NE PAS faire de tests, mets 'test': false. Meme chose pour devops, doc ou securite.",
            "Si l'utilisateur demande explicitement des tests, du devops, de la doc ou de la securite, mets la valeur a true.",
            "CRITIQUE : Si le projet ne necessite manifestement pas de backend ou de base de donnees (ex: 'simple landing page'), laisse les valeurs de 'backend' et 'database' a vide (''). Ne devine pas les technos non demandees !",
            "La cle 'env' doit contenir les identifiants ou URLs fournis par l'utilisateur: 'github_token', 'database_url', 'brave_api_key', 'supabase_url', 'supabase_service_key', 'stripe_api_key', 'figma_access_token', 'resend_api_key', 'cloudflare_api_token', 'cloudflare_account_id', 'mongodb_uri', 'redis_url', etc.",
            "Ne retourne QUE le JSON pur, sans markdown, sans explication, sans bloc de code.",
        ]
    )

    print("--- [1/3] Extraction de la stack et des credentials ---")
    try:
        response = extraction_agent.run(prompt)
    except Exception as e:
        print(f"    [ERREUR] Appel au modele '{MODEL_CONFIG['model']}' echoue : {e}")
        print("    -> Verifie que le modele existe encore sur NVIDIA NIM (build.nvidia.com)")
        print("    -> Verifie ta cle API et le rate limit (429 / 40 RPM sur le free tier)")
        return {}

    if response is None or getattr(response, "content", None) is None:
        print(f"    [ERREUR] Reponse vide du modele '{MODEL_CONFIG['model']}'.")
        print("    Causes possibles : modele deprecie (410), rate limit (429), timeout, ou reponse non-textuelle.")
        return {}

    raw_json = response.content.strip()

    # Nettoyage si le LLM ajoute du markdown
    if raw_json.startswith("```json"):
        raw_json = raw_json[7:]
    if raw_json.startswith("```"):
        raw_json = raw_json[3:]
    if raw_json.endswith("```"):
        raw_json = raw_json[:-3]
    raw_json = raw_json.strip()

    json_candidate = _extract_first_json_object(raw_json)
    if json_candidate is None:
        print("    Erreur parsing JSON: aucun objet JSON trouve dans la reponse")
        print(f"    Reponse brute (200 premiers car.): {raw_json[:200]!r}")
        return {}

    try:
        data = json.loads(json_candidate)
        Path("specs").mkdir(exist_ok=True)
        if "stack" in data:
            with open("specs/detected_stack.yaml", "w", encoding="utf-8") as f:
                yaml.dump(data["stack"], f, default_flow_style=False)
        if "env" in data:
            with open("specs/extracted_env.yaml", "w", encoding="utf-8") as f:
                yaml.dump(data["env"], f, default_flow_style=False)
        print("    Specs : specs/detected_stack.yaml + specs/extracted_env.yaml")
        return data.get("stack", {})
    except json.JSONDecodeError as e:
        print(f"    Erreur parsing JSON: {e}")
        print(f"    Extrait tente (200 premiers car.): {json_candidate[:200]!r}")
        return {}


# ---------------------------------------------------------------------------
# Execution teams / agents
# ---------------------------------------------------------------------------

def _extract_team_content(response):
    """
    Extrait le contenu textuel d'une reponse Agent/Team Agno.
    Retourne None si aucun contenu reel n'a ete produit (permet a l'appelant
    de decider s'il faut retry), au lieu d'un texte de remplacement qui
    masquerait l'echec.
    """
    if getattr(response, "content", None):
        return str(response.content)

    member_responses = getattr(response, "member_responses", None)
    if member_responses:
        parts = []
        for mr in member_responses:
            if getattr(mr, "content", None):
                parts.append(str(mr.content))
                continue
            member_name = getattr(mr, "agent_name", None) or getattr(mr, "agent_id", "unknown")
            if str(getattr(mr, "status", "")) == "error":
                parts.append(f"[{member_name}] Erreur lors de l'execution")
            elif getattr(mr, "messages", None):
                for m in reversed(mr.messages):
                    if getattr(m, "role", None) == "assistant" and getattr(m, "content", None):
                        parts.append(str(m.content))
                        break
                else:
                    parts.append(f"[{member_name}] Aucun contenu genere")
            else:
                parts.append(f"[{member_name}] Aucun contenu genere")
        if parts:
            return "\n\n".join(parts)

    messages = getattr(response, "messages", None)
    if messages:
        for m in reversed(messages):
            if getattr(m, "role", None) == "tool" and getattr(m, "content", None):
                return str(m.content)

    events = getattr(response, "events", None)
    if events:
        errs = [
            str(getattr(e, "content", ""))
            for e in events
            if "error" in str(getattr(e, "event", "")).lower()
        ]
        if errs:
            return "\n".join(errs)

    return None


def _extract_error_details(response) -> str:
    """Extrait les details d'erreur depuis une reponse de team en echec."""
    details = []
    events = getattr(response, "events", None)
    if events:
        for e in events:
            if getattr(e, "content", None):
                details.append(str(e.content))
            elif hasattr(e, "event"):
                details.append(f"Event: {e.event}")

    messages = getattr(response, "messages", None)
    if messages:
        for m in messages:
            if getattr(m, "role", None) in ("tool", "assistant") and getattr(m, "content", None):
                content_str = str(m.content)
                if any(kw in content_str.lower() for kw in ("error", "exception", "traceback", "failed")):
                    details.append(content_str[:500])

    member_responses = getattr(response, "member_responses", None)
    if member_responses:
        for mr in member_responses:
            if str(getattr(mr, "status", "")) == "error":
                member_name = getattr(mr, "agent_name", None) or getattr(mr, "agent_id", "unknown")
                details.append(f"Membre {member_name} en erreur")
            if getattr(mr, "content", None):
                details.append(str(mr.content)[:300])

    return " | ".join(details) if details else "Aucun detail d'erreur disponible"


def _run_team(team, prompt: str) -> str:
    """Execute un team/agent Agno avec retry sur erreur 429 et contenu vide."""
    max_retries = 3
    wait = 5  # Reduit de 10 -> 5s pour une meilleure UX
    max_wait = 30  # Plafond du backoff exponentiel

    entity_name = getattr(team, "name", None) or type(team).__name__

    for attempt in range(1, max_retries + 1):
        try:
            response = team.run(prompt)

            status = getattr(response, "status", None)
            if status == RunStatus.error or (hasattr(status, "value") and status.value == "error"):
                error_details = _extract_error_details(response)
                if attempt < max_retries:
                    print(f"    [RETRY] {entity_name} - echec silencieux (attempt {attempt}/{max_retries}): {error_details[:100]}")
                    time.sleep(wait)
                    wait *= 2
                    continue
                return f"\n{'='*60}\n[{entity_name}]\n{'='*60}\n[ERREUR] Team run echoue apres {max_retries} tentatives.\nDetails: {error_details}\n"

            content = _extract_team_content(response)
            if not content or not content.strip():
                if attempt < max_retries:
                    print(f"    [RETRY] {entity_name} - contenu vide / 0 token de sortie (attempt {attempt}/{max_retries})")
                    time.sleep(wait)
                    wait = min(wait * 2, max_wait)
                    continue
                return f"\n{'='*60}\n[{entity_name}]\n{'='*60}\n[ATTENTION] Contenu vide apres {max_retries} tentatives (le modele a repondu avec 0 token de sortie).\n"

            return f"\n{'='*60}\n[{entity_name}]\n{'='*60}\n{content}\n"

        except Exception as e:
            err_msg = str(e).lower()
            if "429" in str(e) or "rate limit" in err_msg or "too many requests" in err_msg:
                if attempt < max_retries:
                    print(f"    [WAIT]  {entity_name} - rate limit, retry {attempt}/{max_retries} dans {wait}s...")
                    time.sleep(wait)
                    wait = min(wait * 2, max_wait)
                else:
                    return f"\n[{entity_name}] Rate limit atteint apres {max_retries} tentatives.\n"
            else:
                if attempt < max_retries:
                    print(f"    [RETRY] {entity_name} - exception: {e} (attempt {attempt}/{max_retries})")
                    time.sleep(wait)
                    wait = min(wait * 2, max_wait)
                    continue
                return f"\n[{entity_name}] Erreur: {e}\n"
    return f"\n[{entity_name}] Echec apres {max_retries} tentatives.\n"


# ---------------------------------------------------------------------------
# Extraction / sauvegarde des blocs de code
# ---------------------------------------------------------------------------

def _extract_code_blocks(text: str) -> dict:
    """Extrait les blocs de code d'une reponse markdown. Retourne {langage: code}."""
    blocks = {}
    for match in _CODE_BLOCK_RE.finditer(text):
        lang = (match.group(1) or "text").lower()
        code = match.group(2).strip()
        blocks.setdefault(lang, []).append(code)
    return {lang: "\n\n".join(parts) for lang, parts in blocks.items()}


def _looks_like_jsx(code: str) -> bool:
    """Best-effort guard for generated React code that was not transpiled."""
    if not code:
        return False

    if any(p.search(code) for p in _JSX_PATTERNS):
        return True
    if _REACT_ATTRS_RE.search(code):
        return True
    if _REACT_FRAGMENT_RE.search(code):
        return True
    if _REACT_REF_RE.search(code) and _ANGLE_TAG_RE.search(code):
        return True
    return False


def _save_frontend_output(response_text: str, output_dir: Path):
    """
    Analyse la reponse de la Frontend Team et ecrit les fichiers dans output/.
    Priorite : html > jsx > tsx > js > css
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    blocks = _extract_code_blocks(response_text)

    saved = []

    if "html" in blocks:
        path = output_dir / "index.html"
        path.write_text(blocks["html"], encoding="utf-8")
        saved.append(str(path))

    if "css" in blocks:
        path = output_dir / "styles.css"
        path.write_text(blocks["css"], encoding="utf-8")
        saved.append(str(path))

    js_code_raw = blocks.get("javascript") or blocks.get("js", "")
    if js_code_raw:
        path = output_dir / "main.js"
        path.write_text(js_code_raw, encoding="utf-8")
        saved.append(str(path))

    # Si HTML + JS presents, patcher index.html pour charger main.js correctement
    # (React/Babel/module selon le contenu detecte), sans relire les fichiers
    # depuis le disque (tout est deja en memoire).
    try:
        if any(Path(p).name == 'index.html' for p in saved) and js_code_raw:
            index_path = output_dir / 'index.html'
            html_text = blocks["html"]
            js_code = js_code_raw

            has_imports = bool(_HAS_IMPORT_RE.search(js_code))
            has_exports = bool(_HAS_EXPORT_RE.search(js_code))
            is_jsx = _looks_like_jsx(js_code)

            # --- Nettoyage agressif des imports ES modules ---
            # Le modele genere souvent des `import React from 'react'` malgre les consignes.
            # Ces imports cassent le mode script classique et le mode text/babel de Babel.
            # On les supprime TOUJOURS si Babel est utilise OU si des imports React sont detectes.
            react_import_detected = bool(_REACT_IMPORT_RE.search(js_code))

            if is_jsx or react_import_detected:
                # Supprimer toutes les lignes import/export pour le mode Babel/UMD
                js_code = _ANY_IMPORT_RE.sub('', js_code)
                js_code = _ANY_EXPORT_DEFAULT_RE.sub('', js_code)
                js_code = _EXPORT_LINE_RE.sub('', js_code)
                js_code = js_code.strip()
                # Re-detecter JSX apres nettoyage (les imports masquaient parfois le JSX)
                is_jsx = _looks_like_jsx(js_code) or react_import_detected
                has_imports = False
                has_exports = False
            elif has_imports:
                # JS pur avec imports mais sans JSX : charger en module ES
                js_code = js_code  # on garde les imports, type="module"

            if is_jsx:
                script_tag = '<script type="text/babel" data-presets="react" src="main.js"></script>'
            elif has_imports or has_exports:
                script_tag = '<script type="module" src="main.js"></script>'
            else:
                script_tag = '<script src="main.js"></script>'

            react_needed = is_jsx or ('React.createElement' in js_code) or ('ReactDOM' in js_code) or ('React.' in js_code)
            react_tags = ''
            if react_needed and ('react.development.js' not in html_text) and ('react.production.min.js' not in html_text):
                react_tags = ('<script src="https://unpkg.com/react@18/umd/react.development.js"></script>\n'
                              '    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>\n')

            if react_needed and 'ReactDOM.createRoot' in js_code:
                html_text = _REACT17_RE.sub('react@18/umd/', html_text)
                html_text = _REACT_DOM17_RE.sub('react-dom@18/umd/', html_text)

            babel_tag = ''
            if is_jsx and '@babel/standalone' not in html_text:
                babel_tag = '<script src="https://unpkg.com/@babel/standalone@7.23.9/babel.min.js"></script>\n    '

            if _MAIN_SCRIPT_TAG_RE.search(html_text):
                new_html = _MAIN_SCRIPT_TAG_RE.sub(f'\n    {babel_tag}{script_tag}', html_text)
            elif '</body>' in html_text:
                new_html = html_text.replace('</body>', f'    {react_tags}{babel_tag}{script_tag}\n</body>')
            else:
                new_html = html_text + f'\n{react_tags}{babel_tag}{script_tag}\n'

            js_path = output_dir / 'main.js'
            js_path.write_text(js_code, encoding='utf-8')

            print(f"    [PATCH] JSX={is_jsx}, react_needed={react_needed}, script_tag={script_tag}")

            if 'Content-Security-Policy' in new_html:
                csp_fixes = ["'unsafe-inline'"]
                if is_jsx:
                    csp_fixes.append("'unsafe-eval'")
                if 'cdn.tailwindcss.com' in new_html or 'tailwindcss' in new_html:
                    csp_fixes.append("https://cdn.tailwindcss.com")

                def add_to_script_src(m, fixes=csp_fixes):
                    current = m.group(2)
                    for fix in fixes:
                        if fix not in current:
                            current = current.strip() + " " + fix
                    return m.group(1) + current

                new_html = _SCRIPT_SRC_ATTR_RE.sub(add_to_script_src, new_html)

                if "default-src 'self'" in new_html and "connect-src" not in new_html:
                    new_html = new_html.replace("default-src 'self'", "default-src 'self' https://unpkg.com")
                elif "connect-src" in new_html and "https://unpkg.com" not in new_html:
                    new_html = new_html.replace("connect-src", "connect-src https://unpkg.com")

            index_path.write_text(new_html, encoding='utf-8')
    except Exception:
        pass  # best-effort patching; ne casse pas la sauvegarde globale

    if "tailwind.config.js" in response_text and "javascript" in blocks:
        path = output_dir / "tailwind.config.js"
        path.write_text(blocks["javascript"], encoding="utf-8")
        saved.append(str(path))

    if "index.html" not in [Path(p).name for p in saved]:
        fallback = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AgentForge Output</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 font-sans">
  <div class="max-w-4xl mx-auto p-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-4">AgentForge — Generated Output</h1>
    <pre class="bg-white border rounded-lg p-6 text-sm text-gray-700 whitespace-pre-wrap overflow-auto">{response_text[:3000]}</pre>
  </div>
</body>
</html>"""
        path = output_dir / "index.html"
        path.write_text(fallback, encoding="utf-8")
        saved.append(str(path))

    return saved


_BACKEND_FNAME_MAP = {
    "python": "main.py", "py": "app.py",
    "requirements": "requirements.txt",
    "dockerfile": "Dockerfile",
    "yaml": "docker-compose.yml", "yml": "docker-compose.yml",
    "conf": "nginx.conf", "ini": "config.ini",
    "env": ".env.example",
    "shell": "setup.sh", "bash": "setup.sh",
}


def _save_backend_output(response_text: str, target_dir: Path) -> list:
    """Sauvegarde les fichiers backend generes dans target_dir/."""
    target_dir.mkdir(parents=True, exist_ok=True)
    blocks = _extract_code_blocks(response_text)
    saved = []
    for lang in ("python", "py", "requirements", "dockerfile", "yaml", "yml", "conf", "ini", "env", "shell", "bash"):
        if lang not in blocks:
            continue
        path = target_dir / _BACKEND_FNAME_MAP.get(lang, f"file.{lang}")
        path.write_text(blocks[lang], encoding="utf-8")
        saved.append(path)
    return saved


_DB_FNAME_MAP = {
    "sql": "schema.sql",
    "python": "seed.py", "py": "models.py",
    "yaml": "database.yml", "yml": "database.yml",
    "env": ".env.db",
}


def _save_db_output(response_text: str, target_dir: Path) -> list:
    """Sauvegarde les fichiers base de donnees generes dans target_dir/."""
    target_dir.mkdir(parents=True, exist_ok=True)
    blocks = _extract_code_blocks(response_text)
    saved = []
    for lang in ("sql", "python", "py", "yaml", "yml", "env"):
        if lang not in blocks:
            continue
        path = target_dir / _DB_FNAME_MAP.get(lang, f"file.{lang}")
        path.write_text(blocks[lang], encoding="utf-8")
        saved.append(path)
    return saved


_DOC_FNAME_MAP = {
    "markdown": "architecture.md",
    "md": "api.md",
    "text": "notes.txt",
    "html": "report.html",
}


def _save_doc_output(response_text: str, target_dir: Path) -> list:
    """Sauvegarde la documentation generee dans target_dir/."""
    target_dir.mkdir(parents=True, exist_ok=True)
    blocks = _extract_code_blocks(response_text)
    saved = []
    for lang in ("markdown", "md", "text", "html"):
        if lang not in blocks:
            continue
        fname = _DOC_FNAME_MAP.get(lang, f"doc.{lang}")
        path = target_dir / fname
        path.write_text(blocks[lang], encoding="utf-8")
        saved.append(path)
    return saved


def _generate_readme(results: dict, stack: dict, output_dir: Path) -> Path:
    """Genere un README.md synthetique a partir des resultats des equipes."""
    project_name = stack.get("project_name", "AgentForge Project")
    frontend_tech = stack.get("frontend", "N/A")
    backend_tech = stack.get("backend", "N/A")
    database_tech = stack.get("database", "N/A")

    lines = [
        f"# {project_name}",
        "",
        "Projet genere automatiquement par **AgentForge**.",
        "",
        "## Stack Technique",
        "",
        f"- **Frontend** : {frontend_tech}",
        f"- **Backend** : {backend_tech}" if backend_tech else "",
        f"- **Base de donnees** : {database_tech}" if database_tech else "",
        "",
        "## Structure du Projet",
        "",
        "```",
    ]

    tree_lines = []
    for root, dirs, files in os.walk(output_dir):
        rel = Path(root).relative_to(output_dir)
        prefix = "" if str(rel) == "." else f"{rel}/"
        for f in files:
            if f == "README.md" and str(rel) == ".":
                continue
            tree_lines.append(f"{prefix}{f}")
    lines.extend(sorted(tree_lines))
    lines.extend(["```", ""])

    for team_name in ("frontend", "backend", "db", "doc", "test", "devops", "security"):
        if team_name not in results:
            continue
        text = results[team_name]
        lines.append(f"## {team_name.capitalize()}")
        lines.append("")
        for paragraph in text.split("\n\n"):
            stripped = paragraph.strip()
            if stripped and not stripped.startswith("```") and not stripped.startswith("="):
                lines.append(stripped[:300])
                lines.append("")
                break

    lines.extend(["---", "", "## Instructions de Lancement", ""])

    if frontend_tech:
        lines.append(f"### Frontend ({frontend_tech})")
        lines.append("```bash")
        if frontend_tech in ("react", "next"):
            lines.append("cd frontend")
            lines.append("npm install")
            lines.append("npm run dev")
        else:
            lines.append("Ouvrir frontend/index.html dans un navigateur")
        lines.append("```")
        lines.append("")

    if backend_tech:
        lines.append(f"### Backend ({backend_tech})")
        lines.append("```bash")
        lines.append("cd backend")
        lines.append("pip install -r requirements.txt")
        lines.append("python main.py")
        lines.append("```")
        lines.append("")

    lines.append("---")
    lines.append("*Generé par AgentForge*")

    readme = output_dir / "README.md"
    readme.write_text("\n".join(lines), encoding="utf-8")
    return readme


_TEAM_DIR_MAP = {
    "frontend": "frontend",
    "backend": "backend",
    "db": "database",
    "doc": "docs",
    "test": "tests",
    "devops": "devops",
    "security": "security",
}


def _save_project_structure(results: dict, stack: dict, output_dir: Path) -> list:
    """Cree une structure de projet organisee a partir des resultats des equipes."""
    output_dir.mkdir(parents=True, exist_ok=True)
    all_saved = []

    for team_name, response_text in results.items():
        target_name = _TEAM_DIR_MAP.get(team_name)
        if not target_name:
            continue
        target_dir = output_dir / target_name

        if team_name == "frontend":
            saved = _save_frontend_output(response_text, target_dir)
        elif team_name == "backend":
            saved = _save_backend_output(response_text, target_dir)
        elif team_name == "db":
            saved = _save_db_output(response_text, target_dir)
        elif team_name == "doc":
            saved = _save_doc_output(response_text, target_dir)
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            blocks = _extract_code_blocks(response_text)
            saved = []
            for lang, code in blocks.items():
                path = target_dir / f"output.{lang}"
                path.write_text(code, encoding="utf-8")
                saved.append(path)

        for p in saved:
            print(f"    Ecrit : {p}")
        all_saved.extend(saved)

    readme = _generate_readme(results, stack, output_dir)
    print(f"    Ecrit : {readme}")
    all_saved.append(readme)

    return all_saved


# ---------------------------------------------------------------------------
# Serveur de preview
# ---------------------------------------------------------------------------

class _NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    """Desactive completement le cache navigateur (evite les 304 qui servent
    d'anciennes versions de main.js/index.html apres une regeneration)."""

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        pass


class _ReusableThreadingHTTPServer(http.server.ThreadingHTTPServer):
    # allow_reuse_address evite un OSError si un serveur precedent tient encore
    # le port en TIME_WAIT (frequent apres des redemarrages rapproches).
    allow_reuse_address = True
    daemon_threads = True


def _serve_output(output_dir: Path, port: int = 8080):
    """
    Lance un serveur HTTP local (multi-thread) sur le dossier output/, sans
    cache et sans changer le cwd du processus (utilise directory= au lieu de
    os.chdir, plus sur si d'autres threads font de l'I/O fichier en parallele).
    """
    handler_cls = partial(_NoCacheHandler, directory=str(output_dir))

    httpd = None
    chosen_port = port
    for candidate_port in range(port, port + 10):
        try:
            httpd = _ReusableThreadingHTTPServer(("", candidate_port), handler_cls)
            chosen_port = candidate_port
            break
        except OSError as e:
            print(f"    [WARN] Port {candidate_port} indisponible ({e}), tentative suivante...")
            continue

    if httpd is None:
        print(f"    [ERREUR] Aucun port libre trouve entre {port} et {port + 9}.")
        return None

    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()

    url = f"http://localhost:{chosen_port}"
    print(f"\n    Serveur local lance : {url}")
    print(f"    Dossier servi : {output_dir}")
    if chosen_port != port:
        print(f"    [INFO] Port {port} etait occupe, utilisation du port {chosen_port} a la place.")
    webbrowser.open(url)
    return url


def _is_simple_frontend(stack: dict, prompt: str) -> bool:
    """Detecte si le projet est un simple frontend (landing page, site simple)."""
    if stack.get("backend") or stack.get("database"):
        return False
    prompt_lower = prompt.lower()
    return any(p.search(prompt_lower) for p in _SIMPLE_FRONTEND_PATTERNS)


def _load_speckit_implementation_context() -> str:
    """Charge les artefacts Spec Kit existants pour verrouiller la phase d'implementation."""
    feature_file = Path(".specify/feature.json")
    if not feature_file.exists():
        return ""

    try:
        feature_data = json.loads(feature_file.read_text(encoding="utf-8"))
    except Exception:
        return ""

    feature_dir_value = feature_data.get("feature_directory")
    if not feature_dir_value:
        return ""

    feature_dir = Path(feature_dir_value)
    plan_path = feature_dir / "plan.md"
    tasks_path = feature_dir / "tasks.md"

    if not plan_path.exists() or not tasks_path.exists():
        return ""

    return (
        "Contexte Spec Kit verrouille:\n"
        f"- Source de verite: {plan_path.as_posix()} et {tasks_path.as_posix()}\n"
        "- Ne cree jamais un nouveau plan d'execution a cette etape.\n"
        "- Ne regenere jamais une nouvelle decomposition des taches.\n"
        "- Execute uniquement le plan et les taches deja fournis.\n"
        "- Si la demande depasse le contenu existant, signale le manque de couverture au lieu de replanifier.\n"
    )


def _build_team_for_bridge(team_hint: str):
    if team_hint == "frontend":
        return build_frontend_team(mode=TeamMode.coordinate)
    if team_hint == "backend":
        return build_backend_team(mode=TeamMode.coordinate)
    if team_hint == "db":
        return build_db_team(mode=TeamMode.coordinate)
    if team_hint == "test":
        return build_test_team()
    if team_hint == "doc":
        return build_doc_team()
    if team_hint == "devops":
        return build_devops_team()
    if team_hint == "security":
        return build_security_team()
    return build_backend_team(mode=TeamMode.coordinate)


def _save_team_output(team_hint: str, response_text: str, target_dir: Path) -> list[str]:
    if team_hint == "frontend":
        return _save_frontend_output(response_text, target_dir)
    if team_hint == "backend":
        return _save_backend_output(response_text, target_dir)
    if team_hint == "db":
        return _save_db_output(response_text, target_dir)
    if team_hint == "doc":
        return _save_doc_output(response_text, target_dir)

    target_dir.mkdir(parents=True, exist_ok=True)
    blocks = _extract_code_blocks(response_text)
    saved: list[str] = []
    for lang, code in blocks.items():
        path = target_dir / f"file.{lang}"
        path.write_text(code, encoding="utf-8")
        saved.append(str(path))
    return saved


def run_implementation(
    spec_path: str,
    plan_path: str,
    tasks_path: str,
    feature_dir: str,
    mode: str = "bridge",
):
    """Execute a Spec Kit implementation bridge from existing artifacts."""
    spec_file = Path(spec_path)
    plan_file = Path(plan_path)
    tasks_file = Path(tasks_path)
    feature_dir_path = Path(feature_dir)

    if not spec_file.exists() or not plan_file.exists() or not tasks_file.exists():
        return {
            "status": "error",
            "message": "Missing spec, plan, or tasks artifact.",
            "spec_path": str(spec_file),
            "plan_path": str(plan_file),
            "tasks_path": str(tasks_file),
        }

    spec_text = spec_file.read_text(encoding="utf-8")
    plan_text = plan_file.read_text(encoding="utf-8")
    tasks_text = tasks_file.read_text(encoding="utf-8")
    tasks = parse_tasks(tasks_file)

    if not tasks:
        return {
            "status": "error",
            "message": "No executable tasks found in tasks.md.",
            "feature_dir": str(feature_dir_path),
        }

    bridge_output_dir = Path("output") / "bridge" / feature_dir_path.name
    grouped = group_tasks_by_team(tasks)
    completed_task_ids: set[str] = set()
    saved_artifacts: dict[str, list[str]] = {}
    task_results: list[dict[str, str]] = []

    for team_hint, grouped_tasks in grouped.items():
        team = _build_team_for_bridge(team_hint)
        task_prompt = build_team_brief(
            tasks=grouped_tasks,
            spec_text=spec_text,
            plan_text=plan_text,
            tasks_text=tasks_text,
            feature_dir=str(feature_dir_path),
        )
        response = _run_team(team, task_prompt)
        team_ok = bool(response and "[ERREUR]" not in response and "[ATTENTION]" not in response)

        for task in grouped_tasks:
            task_results.append(
                {
                    "task_id": task.task_id,
                    "team": team_hint,
                    "status": "completed" if team_ok else "blocked",
                }
            )

        if team_ok:
            completed_task_ids.update(task.task_id for task in grouped_tasks)
            saved_artifacts[team_hint] = _save_team_output(team_hint, response, bridge_output_dir / team_hint)

    changed_tasks = mark_tasks_completed(tasks_file, completed_task_ids)

    return {
        "status": "ok",
        "mode": mode,
        "feature_dir": str(feature_dir_path),
        "bridge_output_dir": str(bridge_output_dir),
        "task_summary": tasks_summary(tasks),
        "tasks_total": len(tasks),
        "tasks_completed": len(completed_task_ids),
        "changed_tasks": changed_tasks,
        "task_results": task_results,
        "saved_artifacts": saved_artifacts,
    }


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def run_agentforge(user_prompt: str):
    """
    Point d'entree principal.

    Pipeline :
        1. ExtractionAgent  -> detecte stack + credentials depuis le prompt
        2. Build teams      -> construit les equipes selon le profil
        3. ThreadPoolExecutor -> lance toutes les equipes en parallele

    Profils :
        - fast   : equipes minimales, pas de transverses par defaut
        - quality: equipes completes avec transverses (comportement actuel)
        - full   : tous les outils disponibles
    """
    stack = extract_stack_and_env(user_prompt)
    print(f"    Stack detecte : {stack}")
    print(f"    RUN_PROFILE   : {RUN_PROFILE}")

    print("\n--- [2/3] Construction des equipes ---")
    teams = {}

    if RUN_PROFILE == "fast" and _is_simple_frontend(stack, user_prompt):
        print("    [FAST] Projet frontend simple detecte -> generation directe (ReactAgent)")
        react_agent = build_react_agent(skip_tools=True)
        task_prompt = f"Realise cette page en HTML/React/Tailwind: {user_prompt}"
        result = _run_team(react_agent, task_prompt)
        print(result)
        output_dir = Path("output")
        saved = _save_frontend_output(result, output_dir)
        for f in saved:
            print(f"    Ecrit : {f}")
        _serve_output(output_dir, port=8080)
        return

    # Fast-path etendu : en mode fast, si c'est uniquement du frontend (pas de backend,
    # pas de db, pas d'equipes transverses activees) -> ReactAgent direct egalement.
    _only_frontend = (
        RUN_PROFILE == "fast"
        and stack.get("frontend")
        and not stack.get("backend")
        and not stack.get("database")
        and stack.get("test") is not True
        and stack.get("devops") is not True
        and stack.get("doc") is not True
        and stack.get("security") is not True
    )
    if _only_frontend:
        print("    [FAST] Frontend-only detecte -> ReactAgent direct (bypass heavy team)")
        react_agent = build_react_agent(skip_tools=True)
        task_prompt = (
            f"Stack: {stack.get('frontend', 'react')}. "
            f"Realise cette page: {user_prompt}"
        )
        result = _run_team(react_agent, task_prompt)
        print(result)
        output_dir = Path("output")
        saved = _save_frontend_output(result, output_dir)
        for f in saved:
            print(f"    Ecrit : {f}")
        _serve_output(output_dir, port=8080)
        return

    if stack.get("frontend"):
        teams["frontend"] = build_frontend_team()
    if stack.get("backend"):
        teams["backend"] = build_backend_team()
    if stack.get("database"):
        teams["db"] = build_db_team()

    if not teams:
        print("    Aucune equipe construite. Verifiez votre prompt.")
        return

    if RUN_PROFILE == "fast":
        if stack.get("test") is True:
            teams["test"] = build_test_team()
        if stack.get("doc") is True:
            teams["doc"] = build_doc_team()
        if stack.get("devops") is True:
            teams["devops"] = build_devops_team()
        if stack.get("security") is True:
            teams["security"] = build_security_team()
    else:
        if stack.get("test", True):
            teams["test"] = build_test_team()
        if stack.get("doc", True):
            teams["doc"] = build_doc_team()
        if stack.get("devops", True):
            teams["devops"] = build_devops_team()
        if stack.get("security", True):
            teams["security"] = build_security_team()

    for name, team in teams.items():
        print(f"    Team prete : {team.name} [mode={team.mode}]")

    # Taille du pool adaptee au nombre reel d'equipes (evite de sur- ou
    # sous-dimensionner par rapport a une constante fixe).
    profile_cap = 4 if RUN_PROFILE == "fast" else 2
    max_workers = max(1, min(len(teams), profile_cap))
    print(f"\n--- [3/3] Execution des {len(teams)} equipes ({max_workers} en parallele) ---")

    implementation_lock = _load_speckit_implementation_context()
    task_prompt = (
        f"Stack technique imposee : {json.dumps(stack)}\n\n"
        f"Consigne projet : {user_prompt}\n\n"
        "Tu es en phase finale d'implementation. Tu ne dois pas creer de plan d'execution,"
        " ni rediviser le travail. Si des artefacts Spec Kit existent, ils sont prioritaires.\n\n"
        f"{implementation_lock}"
        "Realise ta partie en respectant strictement cette stack et en te referant au plan/taches existants si presentes."
    )

    results = {}
    # Timeout par equipe : 90s en mode fast, 180s sinon
    # Evite qu'un modele gele bloque indefiniment le pipeline.
    per_team_timeout = 90 if RUN_PROFILE == "fast" else 180

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_run_team, team, task_prompt): name
            for name, team in teams.items()
        }
        done, not_done = concurrent.futures.wait(
            futures, timeout=per_team_timeout * max(1, len(teams))
        )
        # Annuler les futures encore en attente apres timeout global
        for f in not_done:
            f.cancel()
            team_name = futures[f]
            print(f"    [TIMEOUT] {team_name} depasse le timeout de {per_team_timeout}s — ignore.")
            results[team_name] = f"\n[{team_name}] Timeout: generation annulee apres {per_team_timeout}s.\n"
        for future in done:
            team_name = futures[future]
            try:
                results[team_name] = future.result(timeout=5)
            except Exception as e:
                results[team_name] = f"\n[{team_name}] Erreur: {e}\n"
            print(f"    [DONE] {team_name}")

    output_dir = Path("output")

    for name in ("frontend", "backend", "db", "devops", "security", "test", "doc"):
        if name in results:
            print(results[name])

    is_fullstack = bool(
        stack.get("backend") or stack.get("database") or stack.get("test")
        or stack.get("devops") or stack.get("doc") or stack.get("security")
    )

    if is_fullstack:
        print("\n--- Sauvegarde de la structure du projet ---")
        _save_project_structure(results, stack, output_dir)
        frontend_dir = output_dir / "frontend"
        if frontend_dir.exists() and any(frontend_dir.iterdir()):
            _serve_output(frontend_dir, port=8080)
        else:
            _serve_output(output_dir, port=8080)
    elif "frontend" in results:
        print("\n--- Sauvegarde des fichiers frontend ---")
        saved = _save_frontend_output(results["frontend"], output_dir)
        for f in saved:
            print(f"    Ecrit : {f}")
        _serve_output(output_dir, port=8080)


if __name__ == "__main__":
    print("=== AgentForge --- Generateur de projets fullstack ===")
    user_prompt = input("Que voulez-vous construire ? > ")
    if user_prompt.strip():
        run_agentforge(user_prompt)
        input("\nAppuyez sur Entree pour arreter le serveur et quitter...")
    else:
        print("Aucun prompt fourni.")