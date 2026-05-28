from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.permissions import require_permission
from app.core.security import get_current_active_user
from app.db.session import get_db
from app.schemas.schemas import UsuarioCreate, UsuarioUpdate, UsuarioOut
from app.services.usuario_service import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("/", response_model=list[UsuarioOut])
async def listar(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("usuarios", "leer"))):
    return await UsuarioService.get_multi(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=UsuarioOut)
async def obtener(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("usuarios", "leer"))):
    obj = await UsuarioService.get_by_id(db, id)
    if not obj:
        raise HTTPException(404, "Usuario no encontrado")
    return obj

@router.post("/", response_model=UsuarioOut, status_code=201)
async def crear(payload: UsuarioCreate, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("usuarios", "crear"))):
    return await UsuarioService.create(db, obj_in=payload, rol_id=payload.rol_id)


@router.patch("/{id}", response_model=UsuarioOut)
async def actualizar(id: int, payload: UsuarioUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("usuarios", "actualizar"))):
    obj = await UsuarioService.get_by_id(db, id)
    if not obj:
        raise HTTPException(404, "Usuario no encontrado")
    return await UsuarioService.update(db, db_obj=obj, obj_in=payload)


@router.delete("/{id}", status_code=204)
async def eliminar(id: int, db: AsyncSession = Depends(get_db), current_user=Depends(require_permission("usuarios", "eliminar"))):
    obj = await UsuarioService.remove(db, id=id)
    if not obj:
        raise HTTPException(404, "Usuario no encontrado")
