# Microservicio de Reportes

Servicio FastAPI que consolida empleados en PostgreSQL y pedidos en MongoDB para construir un dashboard operativo por vendedor, siguiendo el patrón de persistencia poliglota.

## Arquitectura y flujo
- FastAPI + Uvicorn.
- SQLModel/SQLAlchemy sobre PostgreSQL para leer la tabla `usuario` (campos `username`, `rol`).
- Motor (driver async) sobre MongoDB para contar pedidos por `vendedor_id` en la colección configurada.
- `GET /reportes/dashboard` agrega métricas globales y detalle por empleado.

## Requisitos previos
- Python 3.10+
- PostgreSQL accesible (`SQL_*`) con tabla `usuario` y datos de empleados.
- MongoDB accesible (`MONGO_*`) con pedidos asociados a `vendedor_id`.
- pip/venv recomendados. Opcional: Docker para bases de datos.

## Configuración (.env)
Variables soportadas (ver `.env.example`):

| Variable          | Descripción                          | Ejemplo      |
| ----------------- | ------------------------------------ | ------------ |
| SQL_USER          | Usuario de PostgreSQL                | postgres     |
| SQL_PASSWORD      | Contraseña de PostgreSQL             | secret       |
| SQL_HOST          | Host de PostgreSQL                   | localhost    |
| SQL_PORT          | Puerto de PostgreSQL                 | 5432 (o 5433)|
| SQL_DB            | Base de datos de empleados           | empleados_db |
| MONGO_HOST        | Host de MongoDB                      | localhost    |
| MONGO_PORT        | Puerto de MongoDB                    | 27017        |
| MONGO_DB          | Base/DB de MongoDB                   | inventory_db |
| MONGO_COLLECTION  | Colección con pedidos                | orders       |

## Instalación y ejecución (desarrollo)
1) Crear y activar entorno:
   - Windows: `python -m venv venv && .\venv\Scripts\activate`
   - Linux/macOS: `python -m venv venv && source venv/bin/activate`
2) Instalar dependencias: `pip install -r requirements.txt`
3) Copiar y editar variables: `cp .env.example .env` (Windows: `copy`)
4) Arrancar la API: `uvicorn main:app --reload --host 0.0.0.0 --port 8002`
5) Probar salud: `curl http://localhost:8002/`

## Bases de datos rápidas con Docker (opcional)
```bash
# PostgreSQL (ajusta SQL_PORT si usas 5433)
docker run -d --name postgres_reportes \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=empleados_db \
  -p 5433:5432 \
  postgres:15

# MongoDB
docker run -d --name mongo_reportes -p 27017:27017 mongo:7.0
Esquema de datos mínimo
PostgreSQL:

sql

CREATE TABLE IF NOT EXISTS usuario (
  username VARCHAR(50) PRIMARY KEY,
  rol VARCHAR(30) NOT NULL
);

INSERT INTO usuario (username, rol) VALUES ('S-01', 'operario');
MongoDB (colección orders):

json

{ "vendedor_id": "S-01", "pedido_id": "P-1001", "total": 125.50 }
Endpoints
GET / → estado del servicio.
GET /reportes/dashboard → dashboard consolidado (empleados vs pedidos).
GET /debug/collections → nombres de colecciones visibles en MongoDB.
Ejemplo de respuesta GET /reportes/dashboard:

json

{
  "titulo": "Dashboard Operativo - Sprint 4",
  "metricas_globales": { "total_empleados": 1, "total_pedidos_procesados": 2 },
  "detalle_por_vendedor": [
    { "empleado": "S-01", "rol": "operario", "pedidos_realizados": 2, "estado": "Activo" }
  ]
}
Estructura del proyecto
text

microservicio-reportes/
├─ main.py             # Endpoints y lógica del dashboard
├─ database.py         # Conexiones a PostgreSQL y MongoDB
├─ requirements.txt    # Dependencias de la API
├─ .env.example        # Variables de entorno de referencia
└─ README.md           # Documentación
Documentación automática
Swagger UI: http://localhost:8002/docs
ReDoc: http://localhost:8002/redoc
Notas
El DSN SQL se forma como postgresql://{user}:{pass}@{host}:{port}/{db}.
Alinea SQL_PORT con el puerto publicado por el microservicio de usuarios si usas el ecosistema completo.
/debug/collections ayuda a validar la conexión a MongoDB en desarrollo.