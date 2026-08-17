# WedLens

Private, AI-powered discovery for your wedding memories.

WedLens is currently in Phase 0: a small, local development foundation for the photo-management MVP. It deliberately does not include face recognition, semantic search, or deployment infrastructure yet.

## Run locally with Docker

1. Run `docker compose --env-file .env.development up --build`.
3. Open the frontend at http://localhost:5173 and API documentation at http://localhost:8000/docs.

The stack contains a Vue frontend, FastAPI backend, and PostgreSQL database. The database is persisted in the `postgres_data` Docker volume. Stop it with `docker compose down`; use `docker compose down -v` only when you intentionally want to erase local database data.

## Development

See [development notes](docs/development.md) for the shared development/production configuration and [the initial architecture](docs/TODO.md). The first product slice is authentication, private photo upload/storage, gallery, metadata, deletion, and structured search.
