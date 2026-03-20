"""
A2A Tools — Agent2Agent Protocol Werkzeuge.

Ermöglicht Agent-Entdeckung, Registrierung, Task-Delegation
und Kommunikation nach dem A2A-Protokoll von Google.
"""

import uuid
from datetime import datetime, timezone
from typing import Any

from .a2a_store import (
    find_agent_by_name,
    find_task_by_id,
    load_agents,
    load_tasks,
    save_agents,
    save_tasks,
    update_task,
)


def create_agent_card(
    name: str,
    description: str,
    capabilities: list[str],
    endpoint: str,
) -> dict[str, Any]:
    """
    Erstellt eine A2A-kompatible Agent Card (JSON).

    Eine Agent Card beschreibt einen Agenten nach dem A2A-Protokoll:
    Name, Fähigkeiten, Skills und Kontaktendpunkt.

    Args:
        name: Name des Agenten
        description: Kurzbeschreibung was der Agent kann
        capabilities: Liste von Fähigkeiten (z.B. ["text-generation", "code-review"])
        endpoint: URL oder Adresse unter der der Agent erreichbar ist

    Returns:
        A2A Agent Card als Dictionary
    """
    agent_card = {
        "name": name,
        "description": description,
        "url": endpoint,
        "version": "0.1.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
            "stateTransitionHistory": True,
        },
        "skills": [
            {
                "id": cap.lower().replace(" ", "-"),
                "name": cap,
                "description": f"Agent kann: {cap}",
            }
            for cap in capabilities
        ],
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "provider": {
            "organization": "A2A Protocol MCP",
            "url": endpoint,
        },
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }

    return agent_card


def register_agent(agent_card: dict[str, Any]) -> dict[str, Any]:
    """
    Registriert einen Agenten im lokalen A2A-Verzeichnis.

    Speichert die Agent Card in ~/.a2a-agents/agents.json.
    Falls ein Agent mit gleichem Namen existiert, wird er aktualisiert.

    Args:
        agent_card: A2A Agent Card (von create_agent_card erstellt)

    Returns:
        Bestätigung mit Agent-Daten
    """
    # Pflichtfelder prüfen
    if not agent_card.get("name"):
        return {"error": "Agent Card muss einen 'name' haben"}
    if not agent_card.get("url"):
        return {"error": "Agent Card muss eine 'url' haben"}

    agents = load_agents()

    # Prüfen ob Agent mit gleichem Namen existiert
    existing_idx = None
    for i, agent in enumerate(agents):
        if agent.get("name", "").lower() == agent_card["name"].lower():
            existing_idx = i
            break

    # ID zuweisen
    if existing_idx is not None:
        # Bestehende ID beibehalten, Daten aktualisieren
        agent_card["id"] = agents[existing_idx].get("id", str(uuid.uuid4()))
        agent_card["updatedAt"] = datetime.now(timezone.utc).isoformat()
        agents[existing_idx] = agent_card
        action = "aktualisiert"
    else:
        agent_card["id"] = str(uuid.uuid4())
        agent_card["registeredAt"] = datetime.now(timezone.utc).isoformat()
        agents.append(agent_card)
        action = "registriert"

    save_agents(agents)

    return {
        "status": "success",
        "action": action,
        "agent": {
            "id": agent_card["id"],
            "name": agent_card["name"],
            "url": agent_card["url"],
            "skills": [s["name"] for s in agent_card.get("skills", [])],
        },
        "totalAgents": len(agents),
    }


def discover_agents(capability: str) -> dict[str, Any]:
    """
    Sucht Agenten nach Fähigkeit im lokalen A2A-Verzeichnis.

    Durchsucht alle registrierten Agent Cards nach passenden Skills
    und Capabilities.

    Args:
        capability: Gesuchte Fähigkeit (z.B. "code-review", "translation")

    Returns:
        Liste passender Agenten mit ihren Details
    """
    agents = load_agents()
    capability_lower = capability.lower()
    matches = []

    for agent in agents:
        # Suche in Skills
        skills = agent.get("skills", [])
        matching_skills = [
            s for s in skills
            if capability_lower in s.get("name", "").lower()
            or capability_lower in s.get("id", "").lower()
            or capability_lower in s.get("description", "").lower()
        ]

        # Suche in Description
        desc_match = capability_lower in agent.get("description", "").lower()

        # Suche in Name
        name_match = capability_lower in agent.get("name", "").lower()

        if matching_skills or desc_match or name_match:
            matches.append({
                "name": agent.get("name"),
                "description": agent.get("description"),
                "url": agent.get("url"),
                "matchingSkills": [s["name"] for s in matching_skills],
                "allSkills": [s["name"] for s in skills],
                "id": agent.get("id"),
            })

    return {
        "query": capability,
        "found": len(matches),
        "agents": matches,
        "totalRegistered": len(agents),
    }


def send_task(
    target_agent: str,
    task_description: str,
    input_data: str | None = None,
) -> dict[str, Any]:
    """
    Erstellt einen Task-Request nach dem A2A-Protokoll.

    Erzeugt eine Task-Struktur mit ID, Status und Messages,
    die an einen Ziel-Agenten gesendet werden kann.

    Args:
        target_agent: Name oder ID des Ziel-Agenten
        task_description: Beschreibung der Aufgabe
        input_data: Optionale Eingabedaten für den Task

    Returns:
        A2A Task-Objekt mit taskId, status und messages
    """
    # Ziel-Agent finden
    agent = find_agent_by_name(target_agent)
    if not agent:
        # Auch nach ID suchen
        agents = load_agents()
        agent = next((a for a in agents if a.get("id") == target_agent), None)

    if not agent:
        return {
            "error": f"Agent '{target_agent}' nicht gefunden",
            "hint": "Nutze list_registered_agents() oder discover_agents() um verfügbare Agents zu finden",
        }

    task_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    # A2A Task-Struktur nach Protokoll-Spezifikation
    task = {
        "id": task_id,
        "status": {
            "state": "submitted",
            "timestamp": now,
        },
        "targetAgent": {
            "name": agent.get("name"),
            "id": agent.get("id"),
            "url": agent.get("url"),
        },
        "messages": [
            {
                "role": "user",
                "parts": [
                    {
                        "type": "text",
                        "text": task_description,
                    }
                ],
                "timestamp": now,
            }
        ],
        "metadata": {
            "createdAt": now,
            "protocol": "a2a/0.1",
        },
    }

    # Eingabedaten als zusätzliche Message hinzufügen
    if input_data:
        task["messages"].append({
            "role": "user",
            "parts": [
                {
                    "type": "data",
                    "data": input_data,
                }
            ],
            "timestamp": now,
        })

    # Task speichern
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    return {
        "taskId": task_id,
        "status": "submitted",
        "targetAgent": agent.get("name"),
        "targetUrl": agent.get("url"),
        "description": task_description,
        "message": f"Task erstellt und an '{agent.get('name')}' adressiert",
    }


def get_task_status(task_id: str) -> dict[str, Any]:
    """
    Prüft den Status eines delegierten Tasks.

    Gibt den aktuellen Zustand eines Tasks zurück, inklusive
    aller Status-Übergänge und Messages.

    Args:
        task_id: Die Task-ID (von send_task zurückgegeben)

    Returns:
        Task-Status mit History und Messages
    """
    task = find_task_by_id(task_id)

    if not task:
        return {
            "error": f"Task '{task_id}' nicht gefunden",
            "hint": "Prüfe die Task-ID oder nutze send_task() um einen neuen Task zu erstellen",
        }

    return {
        "taskId": task["id"],
        "status": task.get("status", {}),
        "targetAgent": task.get("targetAgent", {}),
        "messageCount": len(task.get("messages", [])),
        "messages": task.get("messages", []),
        "metadata": task.get("metadata", {}),
    }


def list_registered_agents() -> dict[str, Any]:
    """
    Listet alle registrierten Agenten mit ihren Fähigkeiten auf.

    Gibt eine Übersicht aller Agent Cards im lokalen Verzeichnis zurück.

    Returns:
        Liste aller Agenten mit Name, URL und Skills
    """
    agents = load_agents()

    agent_list = []
    for agent in agents:
        skills = agent.get("skills", [])
        agent_list.append({
            "name": agent.get("name"),
            "description": agent.get("description"),
            "url": agent.get("url"),
            "id": agent.get("id"),
            "skills": [s["name"] for s in skills],
            "registeredAt": agent.get("registeredAt", agent.get("createdAt")),
        })

    return {
        "totalAgents": len(agent_list),
        "agents": agent_list,
    }
