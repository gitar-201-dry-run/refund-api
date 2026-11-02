import os

from fastapi import FastAPI

from app.routes import charges, refunds
from app.store import MemoryStore, Store
from app.store_pg import PostgresStore


def default_store() -> Store:
    """Use Postgres when DATABASE_URL is set, otherwise keep data in memory."""
    url = os.environ.get("DATABASE_URL")
    return PostgresStore(url) if url else MemoryStore()


def create_app(store: Store | None = None) -> FastAPI:
    app = FastAPI(title="Refund API")
    app.state.store = store or default_store()
    app.include_router(charges.router)
    app.include_router(refunds.router)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
