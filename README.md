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
| `/test-db` | GET | Read test data from database |
| `/test-db` | POST | Write test data to database |

## Project Structure

```
devbot/
├── bot/                # TypeScript Discord bot
│   ├── src/
│   │   ├── index.ts            # Entry point + command handlers
│   │   ├── config.ts           # Zod config validation
│   │   └── deploy-commands.ts  # Slash command registration
│   ├── package.json
│   └── tsconfig.json
│
└── backend/            # Python FastAPI backend
    ├── app/
    │   ├── main.py     # FastAPI app
    │   ├── config.py   # Pydantic Settings
    │   ├── database.py # SQLite connection and schema
    │   └── __init__.py
    └── pyproject.toml
```

## Configuration

Both bot and backend validate config at startup (fail-fast pattern).

### Bot (.env)
| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | Yes | Bot token from Developer Portal |
| `DISCORD_CLIENT_ID` | Yes | Application ID |
| `BACKEND_URL` | Yes | Backend API URL |

### Backend (.env)
| Variable | Required | Description |
|----------|----------|-------------|
| `OLLAMA_HOST` | No | Ollama API URL |
| `DATABASE_PATH` | No | SQLite database path |
| `HOST` | No | Server bind address |
| `PORT` | No | Server port |

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
#   BACKEND_URL=your_url
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
