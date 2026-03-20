"""
A2A Store — JSON-Dateispeicher für Agents und Tasks.

Speichert Agent-Cards und Task-Daten in ~/.a2a-agents/
"""

import json
from pathlib import Path
from typing import Any


# Speicherort: ~/.a2a-agents/
STORE_DIR = Path.home() / ".a2a-agents"
AGENTS_FILE = STORE_DIR / "agents.json"
TASKS_FILE = STORE_DIR / "tasks.json"


def _ensure_store():
    """Stellt sicher, dass der Speicherordner und Dateien existieren."""
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    if not AGENTS_FILE.exists():
        AGENTS_FILE.write_text("[]", encoding="utf-8")
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")


def load_agents() -> list[dict[str, Any]]:
    """Lädt alle registrierten Agents."""
    _ensure_store()
    try:
        data = json.loads(AGENTS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_agents(agents: list[dict[str, Any]]) -> None:
    """Speichert die Agent-Liste."""
    _ensure_store()
    AGENTS_FILE.write_text(
        json.dumps(agents, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def load_tasks() -> list[dict[str, Any]]:
    """Lädt alle Tasks."""
    _ensure_store()
    try:
        data = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks: list[dict[str, Any]]) -> None:
    """Speichert die Task-Liste."""
    _ensure_store()
    TASKS_FILE.write_text(
        json.dumps(tasks, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def find_agent_by_name(name: str) -> dict[str, Any] | None:
    """Findet einen Agent anhand seines Namens."""
    agents = load_agents()
    for agent in agents:
        if agent.get("name", "").lower() == name.lower():
            return agent
    return None


def find_task_by_id(task_id: str) -> dict[str, Any] | None:
    """Findet einen Task anhand seiner ID."""
    tasks = load_tasks()
    for task in tasks:
        if task.get("id") == task_id:
            return task
    return None


def update_task(task_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
    """Aktualisiert einen bestehenden Task."""
    tasks = load_tasks()
    for task in tasks:
        if task.get("id") == task_id:
            task.update(updates)
            save_tasks(tasks)
            return task
    return None
