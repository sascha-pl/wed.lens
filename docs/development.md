# Development

## Configuration

Each deployment uses one root-level environment file. Docker Compose passes only the relevant
settings from that file to each service; the backend does not load a separate `.env` file.
`POSTGRES_*` values are the single source for both the database container and the backend's
database connection.

For local development, run:

```bash
docker compose --env-file .env.development up --build
```

The frontend is available at `http://localhost:5173`, and the API documentation is at
`http://localhost:8000/docs`. Both backend and database ports are bound to loopback only.

For a production Compose deployment, create the ignored `.env.production` from its committed
template, replace the example values, and select it explicitly:

```bash
cp .env.production.example .env.production
docker compose --env-file .env.production up --build -d
```

`.env.production` must remain uncommitted. In a real deployment, a secret manager can provide the
same variable names instead of storing the database password in that file. Put the frontend behind
a TLS reverse proxy before exposing it publicly.

## Database migrations

The development Compose stack runs `alembic upgrade head` before starting the API, so a fresh
`docker compose --env-file .env.development up --build` creates the `users` table automatically.

To run a migration manually in the running backend container:

```bash
docker compose --env-file .env.development exec backend alembic upgrade head
```

Migrations are the source of truth for the database schema. Do not create or alter application
tables manually through a database GUI.

The initial `users` table stores a UUID, display name, unique email address, password hash, and
creation timestamp. Authentication endpoints and password-hashing logic will be added with the
authentication feature; plain-text passwords are never stored.
