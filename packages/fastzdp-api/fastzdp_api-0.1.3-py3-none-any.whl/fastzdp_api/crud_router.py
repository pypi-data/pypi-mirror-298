from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import Engine
from sqlmodel import SQLModel
import fastzdp_sqlmodel as fasm


def get_crud_router(
        engine: Engine,
        modelSchema: BaseModel,
        model: SQLModel,
):
    """或者增删改查的路由对象"""
    if model is None:
        return

    name = model.__name__
    path = name.lower()

    router = APIRouter(tags=[f"{name} 管理"])

    @router.post(f"/{path}", summary=f"新增 {name}")
    async def add_model_router(req_data: modelSchema):
        fasm.add(engine, model(**req_data.model_dump()))
        return None

    @router.put(f"/{path}" + "/{id}", summary=f"更新 {name}")
    async def update_model_router(id: int, req_data: modelSchema):
        model_router = fasm.get(engine, model, id)
        if not model_router:
            return JSONResponse(status_code=404, content={"error": "数据不存在"})

        fasm.update(engine, model_router, req_data.model_dump())
        return None

    @router.delete(f"/{path}" + "/{id}", summary=f"删除 {name}")
    async def delete_model_router(id: int):
        fasm.delete_id(engine, model, id)
        return None

    @router.get(f"/{path}", summary=f"查询 {name}")
    async def get_model_router(
            page: int = 1,
            size: int = 8,
            key1: str = None,
            value1: str = None,
            key2: str = None,
            value2: str = None,
            key3: str = None,
            value3: str = None,
    ):
        # 等值查询参数
        query_dict = {}
        if key1 and value1:
            query_dict[key1] = value1
        if key2 and value2:
            query_dict[key2] = value2
        if key3 and value3:
            query_dict[key3] = value3

        # 执行查询
        return fasm.get_page(engine, model, page, size, **query_dict)

    return router
