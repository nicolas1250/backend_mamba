# 🐍 SEMILLERO MAMBA - Backend

Sistema de Gestión de Proyectos y Productos de Investigación desarrollado para **CORHUILA** bajo lineamientos de **Minciencias**.

---

## 📌 Descripción

Semillero Mamba es una API REST desarrollada para gestionar proyectos de investigación, productos académicos, usuarios, roles y permisos dentro de un entorno institucional universitario.

El sistema permite:

- Registrar usuarios y autenticarlos
- Gestionar roles y permisos
- Administrar proyectos de investigación
- Asociar investigadores a proyectos
- Registrar productos académicos
- Gestionar autores de productos
- Clasificar productos según Minciencias

---

# 🚀 Stack Tecnológico

| Tecnología | Versión |
|-----------|---------|
| Python | 3.11.10 |
| FastAPI | 0.111.0 |
| PostgreSQL | 15 |
| SQLAlchemy | 2.0 |
| Alembic | 1.13 |
| Docker | 3.9 |
| JWT | jose 3.3 |
| bcrypt | passlib 1.7.4 |
| Uvicorn | 0.29 |

---

# 🏗 Arquitectura

El proyecto sigue arquitectura en capas:

```bash
semillero-mamba/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │
│   ├── core/
│   │
│   ├── db/
│   │
│   ├── models/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │
│   └── main.py
│
├── alembic/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

# 🏗 Arquitectura por Capas

El backend de Semillero Mamba está diseñado bajo una arquitectura en capas, un enfoque que separa responsabilidades para mejorar mantenibilidad, escalabilidad y organización del código.

Cada capa tiene una función específica y se comunica únicamente con las capas necesarias.

---

## Flujo general

```text
Cliente (Frontend)
      ↓
Endpoints (API)
      ↓
Schemas
      ↓
Services
      ↓
Models
      ↓
Database
```

---

# 1️⃣ Capa de Presentación (API)

📂 **Ruta**

```bash
app/api/v1/
```

Esta capa expone todos los endpoints REST del sistema.

Su responsabilidad principal es recibir solicitudes HTTP, validarlas y delegar la lógica de negocio a los servicios.

## Funciones principales

- Recibir requests
- Validar autenticación
- Enviar respuestas HTTP
- Gestionar códigos de estado
- Manejar errores controlados

## Ejemplo

```python
@router.post("/registro")
async def registro(payload: UsuarioCreate):
```

Aquí FastAPI recibe el request, valida el body y llama al servicio correspondiente.

---

## Archivos importantes

### router.py
Centraliza todas las rutas.

Ejemplo:

```python
api_router.include_router(auth.router)
api_router.include_router(usuarios.router)
```

---

### endpoints/auth.py

Gestiona:

- Registro
- Login
- Perfil autenticado

---

### endpoints/usuarios.py

CRUD de usuarios.

---

### endpoints/proyectos.py

CRUD de proyectos.

---

# 2️⃣ Capa de Validación (Schemas)

📂 **Ruta**

```bash
app/schemas/
```

Esta capa define la estructura de los datos que entran y salen de la API.

Está construida con **Pydantic v2**.

---

## Responsabilidades

### Validar entrada

Ejemplo:

```json
{
  "email": "correo@correo.com"
}
```

Si no cumple formato correcto, FastAPI rechaza automáticamente la solicitud.

---

### Serializar salida

Convierte objetos SQLAlchemy a JSON.

---

## Tipos de schemas

### Base

Campos compartidos.

```python
class UsuarioBase
```

---

### Create

Datos requeridos para crear.

```python
class UsuarioCreate
```

Incluye password.

---

### Update

Campos opcionales.

```python
class UsuarioUpdate
```

---

### Out

Respuesta al cliente.

```python
class UsuarioOut
```

Nunca expone password_hash.

---

## Beneficios

✅ Validación automática  
✅ Menos errores  
✅ Documentación Swagger automática

---

# 3️⃣ Capa de Servicios (Business Logic)

📂 **Ruta**

```bash
app/services/
```

Es la capa donde vive la lógica del negocio.

Aquí se decide **cómo funciona el sistema**, no solo guardar datos.

---

## Responsabilidades

- Aplicar reglas de negocio
- Ejecutar operaciones CRUD
- Coordinar modelos
- Procesar lógica adicional

---

## CRUDBase

Archivo:

```bash
base.py
```

Implementa operaciones genéricas:

### get()

Obtiene un registro.

---

### get_multi()

Lista registros.

---

### create()

Inserta nuevos datos.

---

### update()

Actualiza información.

---

### remove()

Elimina registros.

---

## UsuarioService

Archivo:

```bash
usuario_service.py
```

Extiende CRUDBase.

Funciones especiales:

### get_by_email()

Busca usuario por correo.

---

### authenticate()

Valida login.

---

### create()

Hashea contraseña antes de guardar.

---

### update()

Si cambia password, vuelve a cifrar.

---

## ¿Por qué existe esta capa?

Evita poner lógica compleja dentro de endpoints.

Incorrecto:

```python
@router.post()
# lógica completa aquí
```

Correcto:

```python
return await UsuarioService.create()
```

---

# 4️⃣ Capa de Modelos (ORM)

📂 **Ruta**

```bash
app/models/
```

Representa las tablas de PostgreSQL como clases Python.

Usa **SQLAlchemy ORM**.

---

## Responsabilidades

- Definir tablas
- Definir columnas
- Declarar relaciones
- Aplicar restricciones

---

## Ejemplo conceptual

Tabla SQL:

```sql
usuarios
```

Modelo Python:

```python
class Usuario(Base):
```

---

## Qué define cada modelo

### Nombre tabla

```python
__tablename__
```

---

### Columnas

```python
nombre
email
password_hash
```

---

### Relaciones

```python
relationship()
```

---

## Ventajas

No escribir SQL manual para todo.

En lugar de:

```sql
SELECT * FROM usuarios
```

Puedes usar:

```python
db.query(Usuario)
```

---

# 5️⃣ Capa de Persistencia (DB)

📂 **Ruta**

```bash
app/db/
```

Gestiona la conexión con PostgreSQL.

---

## Componentes principales

### Engine

Crea conexión asíncrona.

```python
create_async_engine()
```

---

### Session

Gestiona transacciones.

```python
AsyncSession
```

---

### Dependency Injection

```python
get_db()
```

FastAPI inyecta automáticamente la sesión.

---

## Qué hace

Abre conexión al iniciar request.

Si todo sale bien:

```text
COMMIT
```

Si falla:

```text
ROLLBACK
```

Esto protege consistencia de datos.

---

# 6️⃣ Capa de Seguridad

📂 **Ruta**

```bash
app/core/security.py
```

Encargada de autenticación y autorización.

---

## Funciones

### Hash de contraseñas

```python
hash_password()
```

---

### Verificación

```python
verify_password()
```

---

### Crear token JWT

```python
create_access_token()
```

---

### Obtener usuario autenticado

```python
get_current_user()
```

---

## Flujo

1. Usuario hace login
2. Se valida password
3. Se genera token
4. Cliente guarda token
5. Token se envía en requests
6. Backend valida acceso

---

# 7️⃣ Capa de Configuración

📂 **Ruta**

```bash
app/core/config.py
```

Centraliza variables de entorno.

---

## Variables importantes

### DATABASE_URL

Conexión a PostgreSQL

---

### SECRET_KEY

Firma JWT

---

### ALGORITHM

HS256

---

### ACCESS_TOKEN_EXPIRE_MINUTES

Tiempo de expiración

---

## Beneficios

Permite cambiar ambiente sin tocar código.

Ejemplo:

Desarrollo:

```env
DEBUG=True
```

Producción:

```env
DEBUG=False
```

---

# 8️⃣ Infraestructura Docker

Archivos:

- Dockerfile
- docker-compose.yml

---

## API Container

Ejecuta FastAPI.

---

## DB Container

Ejecuta PostgreSQL.

---

## Ventajas

- Portabilidad
- Reproducibilidad
- Fácil despliegue

---

# 🎯 Beneficios de esta arquitectura

## Escalabilidad

Agregar módulos sin romper existentes.

---

## Mantenibilidad

Cada capa tiene responsabilidad clara.

---

## Reutilización

CRUDBase evita duplicar código.

---

## Seguridad

JWT + bcrypt.

---

## Testabilidad

Cada capa puede probarse individualmente.

---

# 🔐 Seguridad

El sistema implementa:

## JWT Authentication
Autenticación stateless mediante Bearer Token.

## Hashing de contraseñas
Las contraseñas se almacenan cifradas con bcrypt.

## Control de acceso
Basado en:

- Roles
- Permisos
- Relaciones usuario-sistema

---

# 🗃 Base de Datos

## Tablas principales

### Usuarios
Gestiona credenciales del sistema.

### Roles
Define perfiles como:

- admin
- usuario

### Permisos
Acciones permitidas por módulo.

### Roles_Permisos
Relación muchos a muchos.

### Proyectos
Información de investigación.

### Proyecto_Usuarios
Miembros vinculados a proyectos.

### Productos
Resultados académicos.

### Producto_Autores
Autores de productos.

### Tipos_Producto
Clasificación Minciencias.

---

# 🔄 Relaciones principales

```text
Roles ──────< Usuarios

Roles ──────< Roles_Permisos >────── Permisos

Usuarios ───< Proyecto_Usuarios >─── Proyectos

Proyectos ──< Productos

Productos ──< Producto_Autores >──── Usuarios
```

---

# ⚙ Inicialización del Proyecto

## 1. Clonar repositorio

```bash
git clone <repo>
cd semillero-mamba
```

---

## 2. Configurar variables de entorno

Crear archivo `.env`

```env
DATABASE_URL=postgresql+asyncpg://mamba:123456@db:5432/semillero_mamba

SECRET_KEY=clave_super_secreta_32_caracteres

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## 3. Levantar contenedores

```bash
docker compose up --build
```

---

## 4. Verificar funcionamiento

API:

```bash
http://localhost:8000
```

Swagger:

```bash
http://localhost:8000/api/docs
```

ReDoc:

```bash
http://localhost:8000/api/redoc
```

---

# 🧩 Migraciones

Crear migración:

```bash
docker compose exec api alembic revision --autogenerate -m "descripcion"
```

Aplicar migraciones:

```bash
docker compose exec api alembic upgrade head
```

Revertir:

```bash
docker compose exec api alembic downgrade -1
```

---

# 🔑 Flujo de autenticación

## Registro

```http
POST /api/v1/auth/registro
```

Ejemplo:

```json
{
  "nombre": "Nicolas Gomez",
  "email": "nicolas@example.com",
  "password": "Nicolas1234"
}
```

---

## Login

```http
POST /api/v1/auth/login
```

Devuelve:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

## Perfil autenticado

```http
GET /api/v1/auth/me
```

Header:

```http
Authorization: Bearer <token>
```

---

# 📚 Endpoints principales

## Auth

- POST `/auth/registro`
- POST `/auth/login`
- GET `/auth/me`

## Usuarios

- GET `/usuarios`
- GET `/usuarios/{id}`
- PATCH `/usuarios/{id}`
- DELETE `/usuarios/{id}`

## Roles

- GET `/roles`
- POST `/roles`

## Proyectos

- GET `/proyectos`
- POST `/proyectos`

## Productos

- GET `/productos`
- POST `/productos`

## Relaciones

- Proyecto-Usuarios
- Producto-Autores

---

# 🐳 Comandos útiles Docker

Levantar:

```bash
docker compose up
```

Reconstruir:

```bash
docker compose up --build
```

Detener:

```bash
docker compose down
```

Eliminar incluyendo BD:

```bash
docker compose down -v
```

Logs API:

```bash
docker compose logs -f api
```

Logs PostgreSQL:

```bash
docker compose logs -f db
```

Entrar a PostgreSQL:

```bash
docker compose exec db psql -U mamba semillero_mamba
```

---

# ✅ Buenas prácticas implementadas

- Arquitectura en capas
- Async/await
- UUID como PK
- Soft delete
- JWT stateless
- Validación automática
- Dockerización
- Separación de responsabilidades
- CRUD genérico reutilizable
- Migraciones versionadas

---

# 🎯 Objetivo Académico

Este proyecto fue desarrollado como solución tecnológica para apoyar la gestión investigativa institucional en:

**CORHUILA - Corporación Universitaria del Huila**

Bajo lineamientos de:

**Minciencias**

---

# 👨‍💻 Autor

Proyecto desarrollado para el **Semillero Mamba**

**Ingeniería de Sistemas — CORHUILA**

---