from core.skill_registry import build_skill_instructions, discover_skills, get_skill_refs_for


def test_discovers_local_markdown_skills():
    skills = discover_skills()

    assert skills
    assert all(skill.path.startswith("skills/") for skill in skills)
    assert all(skill.path.endswith("/SKILL.md") for skill in skills)


def test_links_relevant_skills_to_agent_and_team():
    skill_refs = get_skill_refs_for("ReactAgent", "frontend")
    names = {skill.name for skill in skill_refs}
    instructions = build_skill_instructions("ReactAgent", "frontend")

    assert any("react" in name.lower() for name in names)
    assert instructions
    assert "skills/" in instructions[0]
