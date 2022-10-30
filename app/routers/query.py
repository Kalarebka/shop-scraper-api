from enum import Enum
from typing import List, Union

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from app.models import Query, UpdateQuery
from app.db_handler import DBHandler


router = APIRouter(prefix="/query")
db = DBHandler()


class Mode(str, Enum):
    get_all = "all"
    active = "active"
    inactive = "inactive"


@router.get("/{mode}", response_model=List[Query])
async def get_queries(mode: Mode, max_results: Union[int, None] = None) -> List[dict]:
    filter = {}
    if mode == Mode.inactive:
        filter = {"active": False}
    elif mode == Mode.active:
        filter = {"active": True}
    queries: List[dict] = await db.get_queries(filter=filter, max_results=max_results)
    return queries


@router.post("/", response_model=Query)
async def add_query(query: Query = Body(...)) -> JSONResponse:
    query = jsonable_encoder(query)
    added_query = await db.create_query(query)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=added_query)


@router.put("/{id}", response_model=Query)
async def update_query(id: str, query: UpdateQuery = Body(...)) -> Union[dict, None]:
    query_update = {k: v for k, v in query.dict().items() if v is not None}

    if len(query_update) >= 1:
        updated_query: Union[dict, None] = await db.update_query(id, query_update)
        if updated_query is not None:
            return updated_query

    existing_query: Union[dict, None] = await db.get_query_by_id(id)
    if existing_query is not None:
        return existing_query

    raise HTTPException(status_code=404, detail=f"Query {id} not found")


@router.delete("/{id}")
async def delete_query(id: str) -> Response:
    result = await db.delete_query(id)

    if result == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Query {id} not found")
