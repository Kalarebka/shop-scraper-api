from enum import Enum
from typing import List, Optional, Union

from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from app.db_handler import DBHandler
from app.models import Query, UpdateQuery

router = APIRouter(prefix="/query")
db = DBHandler()


class Mode(dict, Enum):
    get_all: dict = {}
    active: dict = {"active": True}
    inactive: dict = {"active": False}


@router.get("/{mode}", response_model=List[Query])
async def get_queries(mode: str, max_results: Union[int, None] = None) -> List[dict]:
    mode_filter: dict = Mode[mode].value
    queries: List[dict] = await db.get_queries(
        find_filter=mode_filter, max_results=max_results
    )
    return queries


@router.post("/", response_model=Query)
async def add_query(query: Query = Body(...)) -> JSONResponse:
    query = jsonable_encoder(query)
    added_query_id = await db.create_query(query)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=added_query_id)


@router.put("/{id}", response_model=Query)
async def update_query(id: str, query: UpdateQuery = Body(...)) -> Optional[str]:
    query_update = {k: v for k, v in query.dict().items() if v is not None}

    if len(query_update) >= 1:
        updated_query_id: Optional[str] = await db.update_query(id, query_update)
        if updated_query_id is not None:
            return updated_query_id

    existing_query: Union[dict, None] = await db.get_query_by_id(id)
    if existing_query is not None:
        return id

    raise HTTPException(status_code=404, detail=f"Query {id} not found")


@router.delete("/{id}")
async def delete_query(id: str) -> Response:
    result = await db.delete_query(id)

    if result == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Query {id} not found")
