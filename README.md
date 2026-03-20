# A2A Protocol MCP Server

Bridge between MCP (Model Context Protocol) and Google's **Agent2Agent (A2A) Protocol** — enabling agent discovery, task delegation, and inter-agent communication.

## What is A2A?

The [Agent2Agent Protocol](https://github.com/google/A2A) was introduced by Google in April 2025 as an open standard for AI agents to communicate with each other. It is now being standardized under the **Linux Foundation** to ensure vendor-neutral governance.

**Key concepts:**
- **Agent Cards** — JSON descriptors that advertise an agent's capabilities, skills, and endpoint
- **Task lifecycle** — Structured task delegation with states (submitted, working, completed, failed)
- **Discovery** — Agents can find each other by capability

## How This Server Bridges MCP and A2A

MCP provides the interface between AI models and tools. A2A provides the interface between agents. This server combines both:

- **MCP tools** expose A2A operations to any MCP-compatible AI agent
- Agents can **register themselves**, **discover other agents**, and **delegate tasks**
- Local registry at `~/.a2a-agents/` stores Agent Cards and tasks

## Tools

| Tool | Description |
|------|-------------|
| `create_agent_card` | Create an A2A-compatible Agent Card with skills and endpoint |
| `register_agent` | Register an agent in the local A2A directory |
| `discover_agents` | Search for agents by capability |
| `send_task` | Create a task request following A2A protocol format |
| `get_task_status` | Check status of a delegated task |
| `list_registered_agents` | List all registered agents with capabilities |

## Installation

```bash
pip install a2a-protocol-mcp-server
```

Or with [uvx](https://docs.astral.sh/uv/):

```bash
uvx a2a-protocol-mcp-server
```

## Configuration

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "a2a-protocol": {
      "command": "uvx",
      "args": ["a2a-protocol-mcp-server"]
    }
  }
}
```

### Cursor / Windsurf

```json
{
  "mcpServers": {
    "a2a-protocol": {
      "command": "uvx",
      "args": ["a2a-protocol-mcp-server"]
    }
  }
}
```

## Usage Example

```
1. Create an Agent Card for your agent:
   create_agent_card("MyBot", "Translates text", ["translation", "german", "english"], "http://localhost:8000")

2. Register it:
   register_agent(<agent_card>)

3. Discover agents:
   discover_agents("translation")

4. Send a task:
   send_task("MyBot", "Translate 'Hello World' to German")

5. Check status:
   get_task_status("<task-id>")
```

## Data Storage

Agent Cards and tasks are stored locally in `~/.a2a-agents/`:
- `agents.json` — Registered Agent Cards
- `tasks.json` — Task history and status

## Why A2A + MCP?

| | MCP | A2A |
|---|---|---|
| **Purpose** | Model ↔ Tool interface | Agent ↔ Agent interface |
| **Focus** | Tool access, context | Discovery, delegation |
| **Standard** | Anthropic | Google → Linux Foundation |

Together they create a complete agent communication stack: MCP handles the vertical (model-to-tools), A2A handles the horizontal (agent-to-agent).


---

## More MCP Servers by AiAgentKarl

| Category | Servers |
|----------|---------|
| 🔗 Blockchain | [Solana](https://github.com/AiAgentKarl/solana-mcp-server) |
| 🌍 Data | [Weather](https://github.com/AiAgentKarl/weather-mcp-server) · [Germany](https://github.com/AiAgentKarl/germany-mcp-server) · [Agriculture](https://github.com/AiAgentKarl/agriculture-mcp-server) · [Space](https://github.com/AiAgentKarl/space-mcp-server) · [Aviation](https://github.com/AiAgentKarl/aviation-mcp-server) · [EU Companies](https://github.com/AiAgentKarl/eu-company-mcp-server) |
| 🔒 Security | [Cybersecurity](https://github.com/AiAgentKarl/cybersecurity-mcp-server) · [Policy Gateway](https://github.com/AiAgentKarl/agent-policy-gateway-mcp) · [Audit Trail](https://github.com/AiAgentKarl/agent-audit-trail-mcp) |
| 🤖 Agent Infra | [Memory](https://github.com/AiAgentKarl/agent-memory-mcp-server) · [Directory](https://github.com/AiAgentKarl/agent-directory-mcp-server) · [Hub](https://github.com/AiAgentKarl/mcp-appstore-server) · [Reputation](https://github.com/AiAgentKarl/agent-reputation-mcp-server) |
| 🔬 Research | [Academic](https://github.com/AiAgentKarl/crossref-academic-mcp-server) · [LLM Benchmark](https://github.com/AiAgentKarl/llm-benchmark-mcp-server) · [Legal](https://github.com/AiAgentKarl/legal-court-mcp-server) |

[→ Full catalog (40+ servers)](https://github.com/AiAgentKarl)

## License

MIT
