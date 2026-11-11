# Smart Event

This project deploys the React app and its FastAPI API as one Vercel project. The API runs in Vercel Functions and connects server-side to the existing Neon PostgreSQL database. The browser never receives `DATABASE_URL` or `OPENROUTER_API_KEY`.

## Local development

1. The private `.env` in this working copy has the backend settings. For a fresh checkout, copy `.env.example` to `.env` and set the existing Neon `DATABASE_URL`, a secure `SECRET_KEY`, and the actual OpenRouter settings. The local `.env` is ignored by Git.
2. In one terminal, from this directory, run `npm run api`.
3. In a second terminal, run `npm ci` once, then `npm run dev`.

The Vite development server proxies `/api` requests to the local FastAPI process.

## Vercel deployment

1. Import the `smart-event` directory as the Vercel project root.
2. Add the values from the private local `.env` in Vercel's server-side environment-variable settings (the `.env.example` file is only a key list). Use the existing Neon connection URL for `DATABASE_URL`, set `APP_ENV=production` and `ENABLE_API_DOCS=false`, and do not name database or provider secrets with a `VITE_` prefix.
3. Run the Alembic migrations against that Neon database before the first deployment: `uv run --project server alembic -c server/alembic.ini upgrade head` (from this directory). This includes an additive column for storing uploaded RAG source documents in Neon; existing rows are retained.
4. Deploy. Vercel builds `dist` and routes `/api/*` to the FastAPI function; the remaining routes use the SPA entry point.

Knowledge uploads are limited to 4 MB to fit within serverless request payload limits. Use the Vercel plan/function duration available to the project for long AI and document-ingestion requests. Vercel's filesystem is temporary; event, registration, account, chat, indexed knowledge, and uploaded RAG source data persist in Neon. Documents bundled under `server/documents` remain read-only defaults in deployments.
