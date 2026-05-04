from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.security import get_current_active_user
from app.db.session import get_db
from app.models.models import Usuario, Rol, RolPermiso


def require_permission(modulo: str, accion: str):

    async def permission_checker(
        current_user=Depends(get_current_active_user),
        db: AsyncSession = Depends(get_db)
    ):
        result = await db.execute(
            select(Usuario)
            .options(
                selectinload(Usuario.rol)
                .selectinload(Rol.roles_permisos)
                .selectinload(RolPermiso.permiso)
            )
            .where(Usuario.id == current_user.id)
        )

        usuario = result.scalar_one_or_none()

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        rol = usuario.rol

        if not rol:
            raise HTTPException(
                status_code=403,
                detail="Usuario sin rol"
            )

        permisos = [rp.permiso for rp in rol.roles_permisos]

        for permiso in permisos:
            if permiso.modulo == modulo and permiso.accion == accion:
                return usuario

        raise HTTPException(
            status_code=403,
            detail="No tienes permisos"
        )

    return permission_checker