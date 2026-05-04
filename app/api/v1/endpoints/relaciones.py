from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.schemas.schemas import (
    ProyectoUsuarioCreate, ProyectoUsuarioUpdate, ProyectoUsuarioOut,
    ProductoAutorCreate, ProductoAutorUpdate, ProductoAutorOut,
)
from app.services.services import ProyectoUsuarioService, ProductoAutorService

# ── Proyecto Usuarios ──────────────────────────────────────────
pu_router = APIRouter(prefix="/proyecto-usuarios", tags=["Proyecto — Miembros"])


@pu_router.get("/", response_model=list[ProyectoUsuarioOut])
async def listar(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    return await ProyectoUsuarioService.get_multi(db, skip=skip, limit=limit)


@pu_router.get("/{id}", response_model=ProyectoUsuarioOut)
async def obtener(id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await ProyectoUsuarioService.get(db, id)
    if not obj:
        raise HTTPException(404, "Membresía no encontrada")
    return obj


@pu_router.post("/", response_model=ProyectoUsuarioOut, status_code=201)
async def crear(payload: ProyectoUsuarioCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    return await ProyectoUsuarioService.create(db, obj_in=payload)


@pu_router.patch("/{id}", response_model=ProyectoUsuarioOut)
async def actualizar(id: int, payload: ProyectoUsuarioUpdate, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await ProyectoUsuarioService.get(db, id)
    if not obj:
        raise HTTPException(404, "Membresía no encontrada")
    return await ProyectoUsuarioService.update(db, db_obj=obj, obj_in=payload)


@pu_router.delete("/{id}", status_code=204)
async def eliminar(id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await ProyectoUsuarioService.remove(db, id=id)
    if not obj:
        raise HTTPException(404, "Membresía no encontrada")


# ── Producto Autores ───────────────────────────────────────────
pa_router = APIRouter(prefix="/producto-autores", tags=["Producto — Autores"])


@pa_router.get("/", response_model=list[ProductoAutorOut])
async def listar_autores(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    return await ProductoAutorService.get_multi(db, skip=skip, limit=limit)


@pa_router.get("/{id}", response_model=ProductoAutorOut)
async def obtener_autor(id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await ProductoAutorService.get(db, id)
    if not obj:
        raise HTTPException(404, "Autor no encontrado")
    return obj


@pa_router.post("/", response_model=ProductoAutorOut, status_code=201)
async def crear_autor(payload: ProductoAutorCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    return await ProductoAutorService.create(db, obj_in=payload)


@pa_router.patch("/{id}", response_model=ProductoAutorOut)
async def actualizar_autor(id: int, payload: ProductoAutorUpdate, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await ProductoAutorService.get(db, id)
    if not obj:
        raise HTTPException(404, "Autor no encontrado")
    return await ProductoAutorService.update(db, db_obj=obj, obj_in=payload)


@pa_router.delete("/{id}", status_code=204)
async def eliminar_autor(id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_active_user)):
    obj = await ProductoAutorService.remove(db, id=id)
    if not obj:
        raise HTTPException(404, "Autor no encontrado")
