# DevBot

A Discord bot with GitHub notifications and AI chat.

## Overview

TypeScript Discord bot (discord.js) communicates with a Python backend (FastAPI) via REST API. Features multi-server support with per-guild configuration.

## Features

### Bot Commands
| Command | Description |
|---------|-------------|
| `/ping` | Replies with Pong! |
| `/status` | Check bot and backend health |

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Basic status check |
| `/health` | GET | Health check with uptime and version |

## Project Structure

```
devbot/
├── bot/                # TypeScript Discord bot
│   ├── src/
│   │   ├── index.ts    # Entry point + command handlers
│   │   └── deploy-commands.ts  # Slash command registration
│   ├── package.json
│   └── tsconfig.json
│
└── backend/            # Python FastAPI backend
    ├── app/
    │   ├── main.py     # FastAPI app
    │   └── __init__.py
    └── pyproject.toml
```

## Prerequisites

- Node.js 18+
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) - `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Discord bot token ([Developer Portal](https://discord.com/developers/applications))

## Setup

### Backend

```bash
cd backend
uv sync                                # Install dependencies
uv run uvicorn app.main:app --reload   # Start dev server (port 8000)
```

### Bot

```bash
cd bot
npm install                        # Install dependencies
# Create .env with:
#   DISCORD_TOKEN=your_bot_token
#   DISCORD_CLIENT_ID=your_client_id
#   BACKEND_URL=http://localhost:8000
npx tsx src/deploy-commands.ts     # Register slash commands (once)
npm run dev                        # Start bot with hot reload
```

## Development

| Component | Command | Description |
|-----------|---------|-------------|
| Backend | `uv run uvicorn app.main:app --reload` | Start dev server |
| Bot | `npm run dev` | Start with hot reload |
| Bot | `npx tsx src/deploy-commands.ts` | Register commands |

## Author

**Junzhe Wang**
- junzhe.wang2002@gmail.com
- junzhe.hwangfu@gmail.com
