from fastapi import Request

from app.store import Store


def get_store(request: Request) -> Store:
    return request.app.state.store
