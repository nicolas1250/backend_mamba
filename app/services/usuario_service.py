from datetime import datetime
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioUpdate
from app.core.security import hash_password, verify_password
from app.services.base import CRUDBase


class _UsuarioService(CRUDBase[Usuario, UsuarioCreate, UsuarioUpdate]):

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[Usuario]:
        result = await db.execute(select(Usuario).where(Usuario.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, id: str) -> Optional[Usuario]:
        return await self.get(db, id)

    async def create(self, db: AsyncSession, *, obj_in: UsuarioCreate,rol_id: int) -> Usuario:
        data = obj_in.model_dump(exclude={"password"})
        data["password_hash"] = hash_password(obj_in.password)
        data["rol_id"] = rol_id
        obj = Usuario(**data)
        db.add(obj)
        await db.flush()
        await db.refresh(obj)
        return obj

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[Usuario]:
        user = await self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        # Actualizar ultimo_login
        user.ultimo_login = datetime.utcnow()
        db.add(user)
        await db.flush()
        return user

    async def update(self, db: AsyncSession, *, db_obj: Usuario, obj_in: UsuarioUpdate | dict) -> Usuario:
        data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)
        if "password" in data and data["password"]:
            data["password_hash"] = hash_password(data.pop("password"))
        else:
            data.pop("password", None)
        return await super().update(db, db_obj=db_obj, obj_in=data)


UsuarioService = _UsuarioService(Usuario)
