"""
Schemas Pydantic — Semillero Mamba (INT version)
"""
from datetime import  datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ══════════════════════════════════════════════════════════════
# AUTH
# ══════════════════════════════════════════════════════════════
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: int   # 🔥 cambiado a int
    


# ══════════════════════════════════════════════════════════════
# ROLES
# ══════════════════════════════════════════════════════════════
class RolBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    activo: bool = True


class RolCreate(RolBase):
    pass


class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class RolOut(RolBase):
    model_config = ConfigDict(from_attributes=True)
    id: int   # 🔥 cambiado
    created_at: datetime
    updated_at: datetime


# ══════════════════════════════════════════════════════════════
# PERMISOS
# ══════════════════════════════════════════════════════════════
class PermisoBase(BaseModel):
    nombre: str
    modulo: str
    accion: str


class PermisoCreate(PermisoBase):
    pass


class PermisoUpdate(BaseModel):
    nombre: Optional[str] = None
    modulo: Optional[str] = None
    accion: Optional[str] = None


class PermisoOut(PermisoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int   # 🔥
    created_at: datetime
    updated_at: datetime


# ══════════════════════════════════════════════════════════════
# USUARIOS
# ══════════════════════════════════════════════════════════════
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    activo: bool = True


class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str = Field(..., min_length=8)
    # ❌ eliminamos rol_id del request (mejor práctica)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    rol_id: Optional[int] = None   # 🔥 ahora sí int
    activo: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nombre: str
    email: EmailStr
    rol_id: Optional[int]
    activo: bool
    ultimo_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


# ══════════════════════════════════════════════════════════════
# GRUPOS
# ══════════════════════════════════════════════════════════════
class GrupoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


class GrupoCreate(GrupoBase):
    pass


class GrupoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class GrupoOut(GrupoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


# ══════════════════════════════════════════════════════════════
# TIPOS PRODUCTO
# ══════════════════════════════════════════════════════════════
class TipoProductoBase(BaseModel):
    grupo_id: int   # 🔥
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True


class TipoProductoCreate(TipoProductoBase):
    pass


class TipoProductoUpdate(BaseModel):
    grupo_id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class TipoProductoOut(TipoProductoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


# ══════════════════════════════════════════════════════════════
# PROYECTOS
# ══════════════════════════════════════════════════════════════
class ProyectoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    link_proyecto: Optional[str] = None
    estado: str = "activo"
    fecha_inicio:Optional[datetime] = None
    fecha_fin:Optional[datetime] = None
    creado_por: Optional[int] = None
    activo: bool = True


class ProyectoCreate(ProyectoBase):
    pass


class ProyectoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class ProyectoOut(ProyectoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    creado_por: Optional[int]   # 🔥
    created_at: datetime
    updated_at: datetime


# ══════════════════════════════════════════════════════════════
# PROYECTO_USUARIOS
# ══════════════════════════════════════════════
class ProyectoUsuarioBase(BaseModel):
    proyecto_id: int
    usuario_id: int
    rol_en_proyecto: Optional[str] = None
    fecha_ingreso: Optional[datetime] = None
    fecha_salida: Optional[datetime] = None
    activo: bool = True


class ProyectoUsuarioCreate(ProyectoUsuarioBase):
    pass


class ProyectoUsuarioUpdate(BaseModel):
    rol_en_proyecto: Optional[str] = None
    activo: Optional[bool] = None


class ProyectoUsuarioOut(ProyectoUsuarioBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


# ══════════════════════════════════════════════════════════════
# PRODUCTOS
# ══════════════════════════════════════════════════════════════
class ProductoBase(BaseModel):
    tipo_producto_id: int
    proyecto_id: int
    titulo: str
    descripcion: Optional[str] = None
    estado: str = "en_proceso"
    anio_produccion: Optional[int] = None
    url_evidencia: Optional[str] = None
    doi: Optional[str] = None
    activo: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    tipo_producto_id: Optional[int] = None
    titulo: Optional[str] = None
    activo: Optional[bool] = None


class ProductoOut(ProductoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


# ══════════════════════════════════════════════════════════════
# PRODUCTO_AUTORES
# ══════════════════════════════════════════════════════════════
class ProductoAutorBase(BaseModel):
    producto_id: int
    usuario_id: int
    rol_autor: Optional[str] = None
    es_autor_principal: bool = False


class ProductoAutorCreate(ProductoAutorBase):
    pass


class ProductoAutorUpdate(BaseModel):
    rol_autor: Optional[str] = None
    es_autor_principal: Optional[bool] = None


class ProductoAutorOut(ProductoAutorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime