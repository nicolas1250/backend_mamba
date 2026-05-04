from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.schemas.schemas import (
    GrupoCreate, GrupoUpdate, GrupoOut,
    TipoProductoCreate, TipoProductoUpdate, TipoProductoOut,
)
from app.services.services import GrupoService, TipoProductoService

# ── Grupos Minciencias ─────────────────────────────────────────
grupos_router = APIRouter(prefix="/grupos-minciencias", tags=["Grupos Minciencias"])


@grupos_router.get("/", response_model=list[GrupoOut])
async def listar_grupos(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    return await GrupoService.get_multi(db, skip=skip, limit=limit)


@grupos_router.get("/{id}", response_model=GrupoOut)
async def obtener_grupo(id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await GrupoService.get(db, id)
    if not obj:
        raise HTTPException(404, "Grupo no encontrado")
    return obj


@grupos_router.post("/", response_model=GrupoOut, status_code=201)
async def crear_grupo(payload: GrupoCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    return await GrupoService.create(db, obj_in=payload)


@grupos_router.patch("/{id}", response_model=GrupoOut)
async def actualizar_grupo(id: int, payload: GrupoUpdate, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await GrupoService.get(db, id)
    if not obj:
        raise HTTPException(404, "Grupo no encontrado")
    return await GrupoService.update(db, db_obj=obj, obj_in=payload)


@grupos_router.delete("/{id}", status_code=204)
async def eliminar_grupo(id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await GrupoService.remove(db, id=id)
    if not obj:
        raise HTTPException(404, "Grupo no encontrado")


# ── Tipos Producto ─────────────────────────────────────────────
tipos_router = APIRouter(prefix="/tipos-producto", tags=["Tipos de Producto"])


@tipos_router.get("/", response_model=list[TipoProductoOut])
async def listar_tipos(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    return await TipoProductoService.get_multi(db, skip=skip, limit=limit)


@tipos_router.get("/{id}", response_model=TipoProductoOut)
async def obtener_tipo(id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await TipoProductoService.get(db, id)
    if not obj:
        raise HTTPException(404, "Tipo de producto no encontrado")
    return obj


@tipos_router.post("/", response_model=TipoProductoOut, status_code=201)
async def crear_tipo(payload: TipoProductoCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    return await TipoProductoService.create(db, obj_in=payload)


@tipos_router.patch("/{id}", response_model=TipoProductoOut)
async def actualizar_tipo(id: int, payload: TipoProductoUpdate, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await TipoProductoService.get(db, id)
    if not obj:
        raise HTTPException(404, "Tipo de producto no encontrado")
    return await TipoProductoService.update(db, db_obj=obj, obj_in=payload)


@tipos_router.delete("/{id}", status_code=204)
async def eliminar_tipo(id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await TipoProductoService.remove(db, id=id)
    if not obj:
        raise HTTPException(404, "Tipo de producto no encontrado")
