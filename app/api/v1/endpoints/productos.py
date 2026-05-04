from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import require_permission
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.schemas.schemas import ProductoCreate, ProductoUpdate, ProductoOut
from app.services.services import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=list[ProductoOut])
async def listar(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("productos", "leer"))):
    return await ProductoService.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=ProductoOut)
async def obtener(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("productos", "leer"))):
    obj = await ProductoService.get(db, id)
    if not obj:
        raise HTTPException(404, "Producto no encontrado")
    return obj


@router.post("/", response_model=ProductoOut, status_code=201)
async def crear(payload: ProductoCreate, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("productos", "crear"))):
    return await ProductoService.create(db, obj_in=payload)


@router.patch("/{id}", response_model=ProductoOut)
async def actualizar(id: int, payload: ProductoUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("productos", "actualizar"))):
    obj = await ProductoService.get(db, id)
    if not obj:
        raise HTTPException(404, "Producto no encontrado")
    return await ProductoService.update(db, db_obj=obj, obj_in=payload)


@router.delete("/{id}", status_code=204)
async def eliminar(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("productos", "eliminar"))):
    obj = await ProductoService.remove(db, id=id)
    if not obj:
        raise HTTPException(404, "Producto no encontrado")
