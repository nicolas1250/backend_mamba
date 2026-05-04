from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.schemas.schemas import RolCreate, RolUpdate, RolOut
from app.services.services import RolService
from app.core.permissions import require_permission

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=list[RolOut])
async def listar(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("roles", "leer"))):
    return await RolService.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=RolOut)
async def obtener(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("roles", "leer"))):
    obj = await RolService.get(db, id)
    if not obj:
        raise HTTPException(404, "Rol no encontrado")
    return obj


@router.post("/", response_model=RolOut, status_code=201)
async def crear(payload: RolCreate, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("roles", "crear"))):
    return await RolService.create(db, obj_in=payload)


@router.patch("/{id}", response_model=RolOut)
async def actualizar(id: int, payload: RolUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("roles", "actualizar"))):
    obj = await RolService.get(db, id)
    if not obj:
        raise HTTPException(404, "Rol no encontrado")
    return await RolService.update(db, db_obj=obj, obj_in=payload)


@router.delete("/{id}", status_code=204)
async def eliminar(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("roles", "eliminar"))):
    obj = await RolService.remove(db, id=id)
    if not obj:
        raise HTTPException(404, "Rol no encontrado")
