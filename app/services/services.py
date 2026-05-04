from app.models.models import (
    Rol, Permiso, RolPermiso,
    GrupoMinciencias, TipoProducto,
    Proyecto, ProyectoUsuario,
    Producto, ProductoAutor,
)
from app.schemas.schemas import (
    RolCreate, RolUpdate,
    PermisoCreate, PermisoUpdate,
    GrupoCreate, GrupoUpdate,
    TipoProductoCreate, TipoProductoUpdate,
    ProyectoCreate, ProyectoUpdate,
    ProyectoUsuarioCreate, ProyectoUsuarioUpdate,
    ProductoCreate, ProductoUpdate,
    ProductoAutorCreate, ProductoAutorUpdate,
)
from app.services.base import CRUDBase

RolService            = CRUDBase(Rol)
PermisoService        = CRUDBase(Permiso)
GrupoService          = CRUDBase(GrupoMinciencias)
TipoProductoService   = CRUDBase(TipoProducto)
ProyectoService       = CRUDBase(Proyecto)
ProyectoUsuarioService= CRUDBase(ProyectoUsuario)
ProductoService       = CRUDBase(Producto)
ProductoAutorService  = CRUDBase(ProductoAutor)
