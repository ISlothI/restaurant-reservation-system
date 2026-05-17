from fastapi import APIRouter, Depends

from app.middleware.auth import require_role
from app.models.table import TableCreate, TableResponse, TableUpdate
from app.services.table_service import TableService

router = APIRouter()


@router.get("/{restaurant_id}/tables", response_model=list[TableResponse])
async def list_tables(restaurant_id: str):
    return await TableService.list_by_restaurant(restaurant_id)


@router.get("/{restaurant_id}/tables/{table_id}", response_model=TableResponse)
async def get_table(restaurant_id: str, table_id: str):
    return await TableService.get_by_id(table_id)


@router.post(
    "/{restaurant_id}/tables", response_model=TableResponse, status_code=201
)
async def create_table(
    restaurant_id: str,
    data: TableCreate,
    admin: dict = Depends(require_role("admin")),
):
    return await TableService.create(restaurant_id, data, admin["_id"])


@router.put(
    "/{restaurant_id}/tables/{table_id}", response_model=TableResponse
)
async def update_table(
    restaurant_id: str,
    table_id: str,
    data: TableUpdate,
    admin: dict = Depends(require_role("admin")),
):
    return await TableService.update(restaurant_id, table_id, data, admin["_id"])


@router.delete("/{restaurant_id}/tables/{table_id}", status_code=204)
async def delete_table(
    restaurant_id: str,
    table_id: str,
    admin: dict = Depends(require_role("admin")),
):
    await TableService.delete(restaurant_id, table_id, admin["_id"])
