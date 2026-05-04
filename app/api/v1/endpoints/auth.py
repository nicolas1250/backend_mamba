from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_current_active_user
from app.db.session import get_db
from app.schemas.schemas import Token, UsuarioOut, UsuarioCreate
from app.services.usuario_service import UsuarioService
from app.services.services import RolService

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token, summary="Obtener token JWT")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await UsuarioService.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    if not user.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo")
    token = create_access_token(
        data={
            "sub":  str(user.id),
            "rol": user.rol_id
            })
    return Token(access_token=token)


@router.post("/registro", response_model=UsuarioOut, status_code=201)
async def registro(payload: UsuarioCreate, db: AsyncSession = Depends(get_db)):

    existing = await UsuarioService.get_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # 🔥 buscar rol por defecto
    rol = await RolService.get_by_nombre(db, "usuario")  # o "admin"
    if not rol:
        raise HTTPException(status_code=500, detail="Rol por defecto no existe")

    # 🔥 crear usuario con rol
    return await UsuarioService.create(
        db,
        obj_in=payload,
        rol_id=rol.id
    )


@router.get("/me", response_model=UsuarioOut, summary="Perfil del usuario autenticado")
async def me(current_user=Depends(get_current_active_user)):
    return current_user
