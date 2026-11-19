# Smart Event

A full-stack event management platform with AI-powered RAG (retrieval-augmented generation).

**Stack:** React 19 + Vite 8 (frontend) + FastAPI + LangGraph (backend) + PostgreSQL with pgvector (database) + OpenRouter (embeddings/chat).

---

## Quick Start (Local Development)

**Prerequisites:** Python 3.12, Node.js, uv package manager

```bash
# 1. Copy environment file
cp .env.example .env    # then edit with your credentials

# 2. Run migrations (creates tables, extensions)
uv run --project server alembic -c server/alembic.ini upgrade head

# 3. Seed knowledge documents (optional)
uv run --project server python -c "
import asyncio
from server.app.rag.ingest import ingest_directory, knowledge_docs_directory
from server.app.db.database import SessionLocal
db = SessionLocal()
asyncio.run(ingest_directory(db, str(knowledge_docs_directory())))
db.close()
"

# 4. Start services (two terminals)
npm run api     # FastAPI on http://localhost:8000
npm run dev     # Vite dev server on http://localhost:5174
```

The Vite dev server proxies `/api/*` to the local FastAPI instance.

---

## Vercel Deployment (Zero-Cost Free Tier)

### One-Time Setup

1. **Database:** Create a Neon Postgres project (Free tier).  
   - pgvector 0.7.0+ is pre-installed.  
   - Connection string includes `?sslmode=require`.

2. **OpenRouter API Key:** Generate at <https://openrouter.ai/keys>.

### Deploy

1. Push the repository to GitHub.
2. In the Vercel Dashboard:  
   **New Project → Import Git Repository → Select the project folder.**
3. In **Settings → Environment Variables**, add:

| Variable | Value | Notes |
|---|---|---|
| `DATABASE_URL` | `postgresql://...` from Neon | |
| `SECRET_KEY` | 64-char random string | `openssl rand -hex 32` |
| `APP_ENV` | `production` | |
| `ENABLE_API_DOCS` | `false` | |
| `CORS_ORIGINS` | `https://your-domain.vercel.app` | |
| `OPENROUTER_API_KEY` | `sk-or-v1-...` | |
| `OPENROUTER_EMBEDDING_MODEL` | `nvidia/llama-nemotron-embed-vl-1b-v2:free` | |
| `OPENROUTER_MODEL` | `openai/gpt-oss-120b` | |
| `ENABLE_REDIS_CACHE` | `false` | optional Redis later via Upstash |
| `KNOWLEDGE_DOCS_DIR` | `documents` | |

4. **Deploy.** Vercel will:
   - Run `npm install` → `npm run build`
   - Serve `dist/` for `/` routes
   - Route `/api/*` to the Python FastAPI Function

---

## How It Works

```
Browser
  │ HTTPS
  ▼
Vercel CDN (static) ───► /api/* ───► Python FastAPI (Serverless Function)
                                                    │
                                                    ├──► Neon PostgreSQL (pgvector)
                                                    └──► OpenRouter Embeddings/Chat
```

---

## Environment Variables

The `.env.example` file contains all configurable options:

* `DATABASE_URL` — PostgreSQL connection string with SSL
* `SECRET_KEY` — JWT signing secret (min 32 chars)
* `OPENROUTER_*` — Embedding and chat model configuration
* `RAG_*` — Chunk size, top-k, and retrieval tuning

---

## API Endpoints

| Route | Description |
|---|---|
| `GET /health` | Health check |
| `GET /api/events` | List events |
| `POST /api/auth/login` | JWT login |
| `POST /api/chat` | AI chat with RAG |
| `POST /api/admin/knowledge/upload` | Upload documents for RAG (max 4 MB) |

---

## Limitations (Vercel Serverless)

* Function timeout: **300 seconds maximum** per invocation.
* Request payload: **4.5 MB** limit.
* Knowledge uploads: 4 MB max; use the admin UI to upload.

For long-running ingestion jobs, consider self-hosting with Docker on Render or Railway.

---

## License

MIT
