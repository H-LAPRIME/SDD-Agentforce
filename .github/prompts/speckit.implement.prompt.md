---
agent: speckit.implement
---

When plan.md and tasks.md already exist, do not re-plan or re-decompose anything in Copilot.
Call the `agentforge_implement` MCP tool with `spec_path`, `plan_path`, `tasks_path`, and `feature_dir`.
Use the tool output as the implementation result and keep `tasks.md` as the source of truth for execution order.
