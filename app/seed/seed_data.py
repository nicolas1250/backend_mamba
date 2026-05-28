from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from datetime import datetime

from app.models.models import (
    Rol,
    Permiso,
    RolPermiso,
    Usuario,
    GrupoMinciencias,
    TipoProducto,
    Proyecto,
    ProyectoUsuario,
    Producto,
    ProductoAutor
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


async def seed_database(db: AsyncSession):
    result = await db.execute(select(Rol))
    if result.scalars().first():
        print("Base ya sembrada")
        return

    # ======================
    # ROLES
    # ======================
    admin = Rol(nombre="Administrador")
    profesor = Rol(nombre="Profesor")
    estudiante = Rol(nombre="Estudiante")
    usuario = Rol(nombre="Usuario")

    db.add_all([admin, profesor, estudiante, usuario])
    await db.flush()

    # ======================
    # PERMISOS
    # ======================
    permisos = [
        Permiso(nombre="Crear Usuario", modulo="usuarios", accion="crear"),
        Permiso(nombre="Leer Usuario", modulo="usuarios", accion="leer"),
        Permiso(nombre="Actualizar Usuario", modulo="usuarios", accion="actualizar"),
        Permiso(nombre="Eliminar Usuario", modulo="usuarios", accion="eliminar"),

        Permiso(nombre="Crear Proyecto", modulo="proyectos", accion="crear"),
        Permiso(nombre="Leer Proyecto", modulo="proyectos", accion="leer"),
        Permiso(nombre="Actualizar Proyecto", modulo="proyectos", accion="actualizar"),
        Permiso(nombre="Eliminar Proyecto", modulo="proyectos", accion="eliminar"),

        Permiso(nombre="Crear Producto", modulo="productos", accion="crear"),
        Permiso(nombre="Leer Producto", modulo="productos", accion="leer"),
        Permiso(nombre="Actualizar Producto", modulo="productos", accion="actualizar"),
        Permiso(nombre="Eliminar Producto", modulo="productos", accion="eliminar"),

        Permiso(nombre="Crear Rol", modulo="roles", accion="crear"),
        Permiso(nombre="Leer Rol", modulo="roles", accion="leer"),
        Permiso(nombre="Actualizar Rol", modulo="roles", accion="actualizar"),
        Permiso(nombre="Eliminar Rol", modulo="roles", accion="eliminar"),

    ]


    db.add_all(permisos)
    await db.flush()

    perm_map = {p.nombre: p for p in permisos}

    # ======================
    # ADMIN
    # ======================
    for p in permisos:
        db.add(RolPermiso(rol_id=admin.id, permiso_id=p.id))

    # ======================
    # PROFESOR
    # ======================
    permisos_profesor = [
        "Leer Usuario",

        "Crear Proyecto",
        "Leer Proyecto",
        "Actualizar Proyecto",
        "Eliminar Proyecto",

        "Crear Producto",
        "Eliminar Producto",
        "Actualizar Producto",
        "Leer Producto",

    ]

    for nombre in permisos_profesor:
        db.add(RolPermiso(
            rol_id=profesor.id,
            permiso_id=perm_map[nombre].id
        ))

    # ======================
    # ESTUDIANTE
    # ======================
    permisos_estudiante = [
        "Leer Proyecto",
        "Actualizar Proyecto",
        "Eliminar Proyecto",

        "Leer Producto",
        
    ]

    for nombre in permisos_estudiante:
        db.add(RolPermiso(
            rol_id=estudiante.id,
            permiso_id=perm_map[nombre].id
        ))
    # ======================
    # Usuario
    # ======================
    permisos_usuario = [
        "Leer Proyecto",
        "actualizar Proyecto",
        "Eliminar Proyecto",

        "Leer Producto",
    ]
    
    for nombre in permisos_usuario:
        db.add(RolPermiso(
            rol_id=usuario.id,
            permiso_id=perm_map[nombre].id
        ))

    # ======================
    # GRUPOS
    # ======================
    grupo_ing = GrupoMinciencias(nombre="Ingeniería")
    grupo_social = GrupoMinciencias(nombre="Ciencias Sociales")

    db.add_all([grupo_ing, grupo_social])
    await db.flush()

    # ======================
    # TIPOS PRODUCTO
    # ======================
    articulo = TipoProducto(grupo_id=grupo_ing.id, nombre="Artículo Científico")
    ponencia = TipoProducto(grupo_id=grupo_social.id, nombre="Ponencia")

    db.add_all([articulo, ponencia])
    await db.flush()

    # ======================
    # USUARIOS
    # ======================
    user_admin = Usuario(
        nombre="Julian",
        email="julian@mamba.com",
        password_hash=hash_password("123456"),
        rol_id=admin.id
    )

    user_prof = Usuario(
        nombre="Jose",
        email="jose@mamba.com",
        password_hash=hash_password("123456"),
        rol_id=profesor.id
    )

    user_est = Usuario(
        nombre="Maria",
        email="maria@mamba.com",
        password_hash=hash_password("123456"),
        rol_id=estudiante.id
    )

    db.add_all([user_admin, user_prof, user_est])
    await db.flush()

    # ======================
    # PROYECTO
    # ======================
    proyecto = Proyecto(
        nombre="Sistema sexonacional de gestión investigativa",
        descripcion="Plataforma para gestión investigativa",
        imagen_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRu3-_TbUInL975rAfMjR83kQAjePhVRRJFfw&s",
        link_proyecto="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRu3-_TbUInL975rAfMjR83kQAjePhVRRJFfw&s",
        estado="activo",
        fecha_inicio=datetime.utcnow(),
        fecha_fin=None,
        creado_por=user_admin.id
    )

    db.add(proyecto)
    await db.flush()

    

    # ======================
    # PROYECTO USUARIOS
    # ======================
    db.add_all([
        ProyectoUsuario(
            proyecto_id=proyecto.id,
            usuario_id=user_prof.id,
            rol_en_proyecto="Director"
        ),
        ProyectoUsuario(
            proyecto_id=proyecto.id,
            usuario_id=user_est.id,
            rol_en_proyecto="Investigador"
        )
    ])

    await db.flush()

    # ======================
    # PRODUCTO
    # ======================
    producto = Producto(
        tipo_producto_id=articulo.id,
        proyecto_id=proyecto.id,
        titulo="Modelo Predictivo con IA",
        descripcion="Investigación aplicada con machine learning",
        estado="finalizado",
        anio_produccion=2026
    )

    db.add(producto)
    await db.flush()

    # ======================
    # AUTORES
    # ======================
    db.add_all([
        ProductoAutor(
            producto_id=producto.id,
            usuario_id=user_prof.id,
            rol_autor="Autor Principal",
            es_autor_principal=True
        ),
        ProductoAutor(
            producto_id=producto.id,
            usuario_id=user_est.id,
            rol_autor="Coautor"
        )
    ])

    await db.commit()

    print("Seed ejecutado correctamente")