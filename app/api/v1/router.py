from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.roles import router as roles_router
from app.api.v1.endpoints.usuarios import router as usuarios_router
from app.api.v1.endpoints.proyectos import router as proyectos_router
from app.api.v1.endpoints.productos import router as productos_router
from app.api.v1.endpoints.catalogos import grupos_router, tipos_router
from app.api.v1.endpoints.relaciones import pu_router, pa_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(roles_router)
api_router.include_router(usuarios_router)
api_router.include_router(proyectos_router)
api_router.include_router(productos_router)
api_router.include_router(grupos_router)
api_router.include_router(tipos_router)
api_router.include_router(pu_router)
api_router.include_router(pa_router)
