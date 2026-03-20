"""
A2A Protocol MCP Server — Brücke zwischen MCP und Google Agent2Agent Protocol.

Ermöglicht Agent-Entdeckung, Registrierung, Task-Delegation
und Kommunikation nach dem A2A-Standard.
"""

from mcp.server.fastmcp import FastMCP

from .tools.a2a import (
    create_agent_card,
    discover_agents,
    get_task_status,
    list_registered_agents,
    register_agent,
    send_task,
)

# FastMCP Server initialisieren
mcp = FastMCP(
    "A2A Protocol MCP",
    instructions=(
        "Bridges MCP with Google's Agent2Agent (A2A) Protocol. "
        "Enables agent discovery, registration, task delegation, "
        "and inter-agent communication following the A2A standard. "
        "Agents can publish Agent Cards, find other agents by capability, "
        "and delegate tasks using the A2A task lifecycle."
    ),
)


# --- Tools registrieren ---


@mcp.tool()
def tool_create_agent_card(
    name: str,
    description: str,
    capabilities: list[str],
    endpoint: str,
) -> dict:
    """Create an A2A-compatible Agent Card with skills, capabilities and contact endpoint.

    An Agent Card is the standard way for agents to advertise their capabilities
    in the A2A protocol. Other agents can discover and interact with you through it.

    Args:
        name: Agent name (e.g. "CodeReviewBot")
        description: What the agent does (e.g. "Reviews Python code for bugs and style issues")
        capabilities: List of capabilities (e.g. ["code-review", "python", "security-audit"])
        endpoint: URL where the agent is reachable (e.g. "https://myagent.example.com/a2a")
    """
    return create_agent_card(name, description, capabilities, endpoint)


@mcp.tool()
def tool_register_agent(agent_card: dict) -> dict:
    """Register an agent in the local A2A directory.

    Stores the Agent Card in ~/.a2a-agents/ so other agents can discover it.
    If an agent with the same name already exists, it will be updated.

    Args:
        agent_card: A2A Agent Card (created by create_agent_card)
    """
    return register_agent(agent_card)


@mcp.tool()
def tool_discover_agents(capability: str) -> dict:
    """Search for agents by capability in the local A2A registry.

    Finds agents whose skills, description or name match the given capability.
    Useful for finding the right agent to delegate a task to.

    Args:
        capability: Capability to search for (e.g. "translation", "code-review", "data-analysis")
    """
    return discover_agents(capability)


@mcp.tool()
def tool_send_task(
    target_agent: str,
    task_description: str,
    input_data: str | None = None,
) -> dict:
    """Create and send a task request following A2A protocol format.

    Creates a task with taskId, status lifecycle and messages,
    addressed to a specific target agent.

    Args:
        target_agent: Name or ID of the target agent
        task_description: What the agent should do
        input_data: Optional input data for the task
    """
    return send_task(target_agent, task_description, input_data)


@mcp.tool()
def tool_get_task_status(task_id: str) -> dict:
    """Check the status of a delegated task.

    Returns the current state, all status transitions and messages for a task.

    Args:
        task_id: The task ID (returned by send_task)
    """
    return get_task_status(task_id)


@mcp.tool()
def tool_list_registered_agents() -> dict:
    """List all registered agents with their capabilities.

    Returns an overview of all Agent Cards in the local directory,
    including names, endpoints and skills.
    """
    return list_registered_agents()


def main():
    """Startet den A2A Protocol MCP Server."""
    mcp.run()


if __name__ == "__main__":
    main()
