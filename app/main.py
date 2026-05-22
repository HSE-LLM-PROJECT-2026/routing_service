from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.config import Settings, get_settings


class GenericPayload(BaseModel):
    id: str | None = None
    name: str | None = None
    cluster_id: str | None = None
    deployment_id: str | None = None
    alias: str | None = None
    status: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def service_payload(settings: Settings) -> dict[str, Any]:
    return {
        "service": settings.service_name,
        "role": settings.service_role,
        "title": settings.service_title,
        "description": settings.service_description,
        "split_enabled": settings.service_split_enabled,
        "updated_at": now_iso(),
    }


def payload_id(payload: GenericPayload | None) -> str:
    if payload and payload.id:
        return payload.id
    if payload and payload.name:
        return payload.name
    return str(uuid4())


settings = get_settings()
app = FastAPI(title=settings.service_title, version="0.1.0")
store: dict[str, dict[str, Any]] = {}


@app.get("/livez")
async def livez() -> dict[str, Any]:
    return {"status": "ok", **service_payload(settings)}


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"status": "ok", **service_payload(settings)}


@app.get("/service-info")
async def service_info() -> dict[str, Any]:
    return {
        **service_payload(settings),
        "service_to_service_urls": settings.service_to_service_urls,
    }


def row(resource: str, item_id: str, payload: GenericPayload | None = None, **extra: Any) -> dict[str, Any]:
    data = payload.model_dump(mode="json") if payload else {}
    status_value = data.get("status") or extra.pop("status", "accepted")
    item = {
        "id": item_id,
        "resource": resource,
        "service": settings.service_name,
        "role": settings.service_role,
        "status": status_value,
        "updated_at": now_iso(),
        **extra,
    }
    for key, value in data.items():
        if key != "status" and value is not None:
            item[key] = value
    store[f"{resource}:{item_id}"] = item
    return item


def list_rows(resource: str) -> list[dict[str, Any]]:
    return [value for key, value in sorted(store.items()) if key.startswith(f"{resource}:")]


def get_row(resource: str, item_id: str) -> dict[str, Any]:
    return store.get(f"{resource}:{item_id}") or {
        "id": item_id,
        "resource": resource,
        "service": settings.service_name,
        "role": settings.service_role,
        "status": "not_found",
        "updated_at": now_iso(),
    }


@app.get("/traffic-routes")
async def list_traffic_routes() -> Any:
    return list_rows("traffic_routes")


@app.post("/traffic-routes")
async def create_traffic_route(payload: GenericPayload | None = None) -> Any:
    return row("traffic_routes", payload_id(payload), payload, operation="create_traffic_route")


@app.get("/traffic-routes/{alias}")
async def get_traffic_route(alias: str) -> Any:
    return get_row("traffic_routes", alias)


@app.put("/traffic-routes/{alias}")
async def update_traffic_route(alias: str, payload: GenericPayload | None = None) -> Any:
    return row("traffic_routes", alias, payload, operation="update_traffic_route")


@app.delete("/traffic-routes/{alias}")
async def delete_traffic_route(alias: str) -> Any:
    key = f"traffic_routes:{alias}"
    deleted = store.pop(key, None)
    if deleted:
        return deleted
    return {
        "id": alias,
        "resource": "traffic_routes",
        "service": settings.service_name,
        "role": settings.service_role,
        "status": "deleted",
        "updated_at": now_iso(),
    }


@app.post("/traffic-routes/{alias}/weights")
async def update_traffic_weights(alias: str, payload: GenericPayload | None = None) -> Any:
    return row("traffic_routes", alias, payload, operation="update_traffic_weights")


@app.post("/traffic-routes/{alias}/test")
async def test_traffic_route(alias: str, payload: GenericPayload | None = None) -> Any:
    return row("traffic_routes", alias, payload, operation="test_traffic_route")
