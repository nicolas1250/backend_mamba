from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import require_permission
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.schemas.schemas import ProyectoCreate, ProyectoUpdate, ProyectoOut
from app.services.services import ProyectoService
from app.models.models import Proyecto


router = APIRouter(prefix="/proyectos", tags=["Proyectos"])


@router.get("/", response_model=list[ProyectoOut])
async def listar(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("proyectos", "leer"))):
    return await ProyectoService.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=ProyectoOut)
async def obtener(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("proyectos", "leer"))):
    obj = await ProyectoService.get(db, id)
    if not obj:
        raise HTTPException(404, "Proyecto no encontrado")
    return obj


@router.post("/", response_model=ProyectoOut, status_code=201)
async def crear(payload: ProyectoCreate, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("proyectos", "crear"))):
    data = payload.model_dump(exclude_unset=True)
    data["creado_por"] = current_user.id
    obj = Proyecto(**data)
    db.add(obj)
    await db.flush()
    await db.refresh(obj)
    return obj


@router.patch("/{id}", response_model=ProyectoOut)
async def actualizar(id: int, payload: ProyectoUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("proyectos", "actualizar"))):
    obj = await ProyectoService.get(db, id)
    if not obj:
        raise HTTPException(404, "Proyecto no encontrado")
    return await ProyectoService.update(db, db_obj=obj, obj_in=payload)


@router.delete("/{id}", status_code=204)
async def eliminar(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("proyectos", "eliminar"))):
    obj = await ProyectoService.remove(db, id=id)
    if not obj:
        raise HTTPException(404, "Proyecto no encontrado")
