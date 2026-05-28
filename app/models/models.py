"""
Modelos SQLAlchemy — Semillero Mamba (VERSIÓN INT)
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Integer, String, Text,
    UniqueConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from sqlalchemy import text

# ═════════════════════════════════════════════════════════════
# ROLES
# ═════════════════════════════════════════════════════════════
class Rol(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255))
    activo: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="rol")
    roles_permisos: Mapped[list["RolPermiso"]] = relationship(back_populates="rol", cascade="all, delete-orphan")


# ═════════════════════════════════════════════════════════════
# PERMISOS
# ═════════════════════════════════════════════════════════════
class Permiso(Base):
    __tablename__ = "permisos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    modulo: Mapped[str] = mapped_column(String(100), nullable=False)
    accion: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    roles_permisos: Mapped[list["RolPermiso"]] = relationship(
        back_populates="permiso", cascade="all, delete-orphan")


# ═════════════════════════════════════════════════════════════
# ROLES_PERMISOS
# ═════════════════════════════════════════════════════════════
class RolPermiso(Base):
    __tablename__ = "roles_permisos"
    rol_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permiso_id: Mapped[int] = mapped_column(Integer, ForeignKey("permisos.id", ondelete="CASCADE"), primary_key=True)

    rol: Mapped["Rol"] = relationship(back_populates="roles_permisos")
    permiso: Mapped["Permiso"] = relationship(back_populates="roles_permisos")


# ═════════════════════════════════════════════════════════════
# USUARIOS
# ═════════════════════════════════════════════════════════════
class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    rol_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id", ondelete="SET NULL"))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    ultimo_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    rol: Mapped["Rol"] = relationship(back_populates="usuarios")
    proyectos_creados: Mapped[list["Proyecto"]] = relationship(back_populates="creador", foreign_keys="Proyecto.creado_por")
    proyecto_usuarios: Mapped[list["ProyectoUsuario"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    producto_autores: Mapped[list["ProductoAutor"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")


# ═════════════════════════════════════════════════════════════
# GRUPOS MINCIENCIAS
# ═════════════════════════════════════════════════════════════
class GrupoMinciencias(Base):
    __tablename__ = "grupos_minciencias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tipos_producto: Mapped[list["TipoProducto"]] = relationship(back_populates="grupo")


# ═════════════════════════════════════════════════════════════
# TIPOS PRODUCTO
# ═════════════════════════════════════════════════════════════
class TipoProducto(Base):
    __tablename__ = "tipos_producto"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    grupo_id: Mapped[int] = mapped_column(Integer, ForeignKey("grupos_minciencias.id", ondelete="RESTRICT"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    grupo: Mapped["GrupoMinciencias"] = relationship(back_populates="tipos_producto")
    productos: Mapped[list["Producto"]] = relationship(back_populates="tipo_producto")


# ═════════════════════════════════════════════════════════════
# PROYECTOS
# ═════════════════════════════════════════════════════════════
class Proyecto(Base):
    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    imagen_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    link_proyecto: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estado: Mapped[str] = mapped_column(String(50), default="activo")
    fecha_inicio: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    fecha_fin: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    creado_por: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    creador: Mapped[Optional["Usuario"]] = relationship(back_populates="proyectos_creados", foreign_keys=[creado_por])
    proyecto_usuarios: Mapped[list["ProyectoUsuario"]] = relationship(back_populates="proyecto", cascade="all, delete-orphan")
    productos: Mapped[list["Producto"]] = relationship(back_populates="proyecto")


# ═════════════════════════════════════════════════════════════
# PROYECTO_USUARIOS
# ═════════════════════════════════════════════════════════════
class ProyectoUsuario(Base):
    __tablename__ = "proyecto_usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    proyecto_id: Mapped[int] = mapped_column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    rol_en_proyecto: Mapped[Optional[str]] = mapped_column(String(50))
    fecha_ingreso: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    fecha_salida: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (UniqueConstraint("proyecto_id", "usuario_id", name="uq_proyecto_usuario"),)

    proyecto: Mapped["Proyecto"] = relationship(back_populates="proyecto_usuarios")
    usuario: Mapped["Usuario"] = relationship(back_populates="proyecto_usuarios")


# ═════════════════════════════════════════════════════════════
# PRODUCTOS
# ═════════════════════════════════════════════════════════════
class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tipo_producto_id: Mapped[int] = mapped_column(Integer, ForeignKey("tipos_producto.id", ondelete="RESTRICT"), nullable=False)
    proyecto_id: Mapped[int] = mapped_column(Integer, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(300), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(Text)
    estado: Mapped[str] = mapped_column(String(50), default="en_proceso")
    anio_produccion: Mapped[Optional[int]] = mapped_column(Integer)
    url_evidencia: Mapped[Optional[str]] = mapped_column(Text)
    doi: Mapped[Optional[str]] = mapped_column(String(100))
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    tipo_producto: Mapped["TipoProducto"] = relationship(back_populates="productos")
    proyecto: Mapped["Proyecto"] = relationship(back_populates="productos")
    producto_autores: Mapped[list["ProductoAutor"]] = relationship(back_populates="producto", cascade="all, delete-orphan")


# ═════════════════════════════════════════════════════════════
# PRODUCTO_AUTORES
# ═════════════════════════════════════════════════════════════
class ProductoAutor(Base):
    __tablename__ = "producto_autores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey("productos.id", ondelete="CASCADE"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    rol_autor: Mapped[Optional[str]] = mapped_column(String(50))
    es_autor_principal: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("producto_id", "usuario_id", name="uq_producto_autor"),)

    producto: Mapped["Producto"] = relationship(back_populates="producto_autores")
    usuario: Mapped["Usuario"] = relationship(back_populates="producto_autores")