from fastapi import APIRouter, HTTPException, Depends
from service.query import query_db_sql

query = APIRouter()


@query.post("/query")
async def query_db():
    return await query_db_sql()
