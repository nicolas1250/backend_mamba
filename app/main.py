from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.db.session import engine, Base
from app.seed.seed_data import seed_database
from app.db.session import AsyncSessionLocal

# Importar todos los modelos para que Alembic / create_all los detecte
import app.models.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Sembrar datos
    async with AsyncSessionLocal() as db:
        await seed_database(db)

    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""

    
## Semillero Mamba — API Backend

Sistema de Gestión de Proyectos y Productos de Investigación  
**Semillero Mamba · Marco Minciencias · CORHUILA**

### Módulos disponibles
- 🔐 **Autenticación** — JWT (login / registro / perfil)
- 👥 **Usuarios** — CRUD con roles y permisos
- 📂 **Proyectos** — Gestión de proyectos de investigación
- 📦 **Productos** — Artículos, ponencias, libros y más
- 🏷️ **Catálogos** — Grupos Minciencias y tipos de producto
- 🔗 **Relaciones** — Miembros de proyecto y autores de productos
""",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Rutas ─────────────────────────────────────────────────────
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
        "status": "ok",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}
