# Gestor de Reportes — Microservicio Híbrido (FastAPI + SQL + NoSQL)

API de inteligencia de negocio encargada de consolidar información. Implementa el patrón de **Persistencia Políglota**, cruzando datos relacionales de empleados (`PostgreSQL`) con datos transaccionales de pedidos (`MongoDB`) para generar dashboards en tiempo real.

## Tabla de contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y ejecución (desarrollo)](#instalación-y-ejecución-desarrollo)
- [Configuración](#configuración)
- [Infraestructura de Datos (Docker)](#infraestructura-de-datos-docker)
- [Documentación de la API](#documentación-de-la-api)
- [Despliegue sugerido](#despliegue-sugerido)
- [Contribuir](#contribuir)
- [Licencia y Contacto](#licencia-y-contacto)

---

## Características

- Dashboard operativo de ventas por empleado.
- Conexión dual asíncrona (SQL y NoSQL simultáneos).
- Lectura de datos cruzada entre microservicios.
- Endpoints documentados con OpenAPI/Swagger.

## Tecnologías

- `FastAPI` (API)
- `SQLModel` (Conexión a PostgreSQL)
- `Motor` (Driver asíncrono para MongoDB)
- `PostgreSQL` (Base de datos relacional - Empleados)
- `MongoDB` (Base de datos documental - Pedidos)
- `uvicorn` (ASGI server)

## Estructura del proyecto

Raíz del servicio `microservicio-reportes`:

```text
main.py            # Lógica de negocio y endpoints
# Gestor de Reportes — Microservicio Híbrido (FastAPI + PostgreSQL + MongoDB)

Servicio responsable de consolidar datos relacionales y documentales (patrón de persistencia políglota) para generar dashboards y métricas operativas en tiempo real.

---

## Tabla de contenidos

- [Características](#caracter%C3%ADsticas)
- [Tecnologías](#tecnolog%C3%ADas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y ejecución (desarrollo)](#instalaci%C3%B3n-y-ejecuci%C3%B3n-desarrollo)
- [Configuración](#configuraci%C3%B3n)
- [Infraestructura de datos (Docker)](#infraestructura-de-datos-docker)
- [Endpoints principales](#endpoints-principales)
- [Documentación de la API](#documentaci%C3%B3n-de-la-api)
- [Despliegue sugerido](#despliegue-sugerido)
- [Contribuir](#contribuir)
- [Licencia y contacto](#licencia-y-contacto)

---

## Características

- Dashboard operativo con métricas por empleado.
- Integración asíncrona entre PostgreSQL y MongoDB.
- Endpoints documentados con OpenAPI/Swagger.

## Tecnologías

- `FastAPI` (API)
- `SQLModel` / `SQLAlchemy` (PostgreSQL)
- `motor` (driver asíncrono para MongoDB)
- `PostgreSQL` (datos de empleados)
- `MongoDB` (datos de pedidos)
- `uvicorn` (ASGI server)

## Estructura del proyecto

Raíz del servicio `microservicio-reportes`:

```
main.py            # Lógica de negocio y endpoints
database.py        # Configuración de conexiones (SQL + Mongo)
requirements.txt   # Dependencias
.env.example       # Variables de entorno de ejemplo
README.md          # Documentación (este archivo)
```

## Requisitos

- `Python 3.10+`
- `PostgreSQL` con los datos de empleados disponibles
- `MongoDB` con los datos de pedidos disponibles
- `pip` y `virtualenv` (recomendado)

## Instalación y ejecución (desarrollo)

1. Clonar el repositorio y entrar en el directorio del servicio:

```powershell
git clone <URL_DEL_REPO>
cd microservicio-reportes
```

2. Crear y activar un entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4. Crear el archivo de configuración a partir del ejemplo:

```powershell
copy .env.example .env
```

5. Ajustar `.
.env` con las credenciales/hosts de tus bases de datos (ver sección "Configuración").

6. Ejecutar la aplicación en modo desarrollo:

```powershell
uvicorn main:app --reload --port 8002
```

La API estará disponible en `http://localhost:8002`.

## Configuración

Editar el archivo `.env` (a partir de `.env.example`) y ajustar las variables de conexión:

```
# --- Base de Datos SQL (Empleados) ---
SQL_USER=admin
SQL_PASSWORD=password123
SQL_HOST=127.0.0.1
SQL_PORT=5433
SQL_DB=empleados_db

# --- Base de Datos NoSQL (Pedidos) ---
MONGO_HOST=127.0.0.1
MONGO_PORT=27017
MONGO_DB=inventory_db
MONGO_COLLECTION=orders
```

Comprueba que los puertos y hosts coinciden con tus contenedores o instancias.

## Infraestructura de datos (Docker)

Puedes levantar rápidamente ambas bases de datos para desarrollo:

```powershell
docker run -d --name postgres_db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password123 -e POSTGRES_DB=empleados_db -p 5433:5432 postgres:15
docker run -d --name mongo_db -p 27017:27017 mongo:7.0
```

Si prefieres, puedo añadir un `docker-compose.yml` que orqueste ambos servicios junto con la API.

## Endpoints principales

- `GET /reportes/dashboard` — Devuelve el dashboard operativo consolidado.

Ejemplo (cURL):

```bash
curl -X GET "http://localhost:8002/reportes/dashboard" \
  -H "accept: application/json"
```

Respuesta de ejemplo:

```json
{
  "titulo": "Dashboard Operativo - Sprint 4",
  "metricas_globales": {
    "total_empleados": 1,
    "total_pedidos_procesados": 2
  },
  "detalle_por_vendedor": [
    {
      "empleado": "S-01",
      "rol": "operario",
      "pedidos_realizados": 2,
      "estado": "Activo"
    }
  ]
}
```

## Documentación de la API

FastAPI ofrece interfaces interactivas:

- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

## Despliegue sugerido

Para producción:

- Ejecutar la API en contenedores o detrás de un proxy (NGINX) y un proceso manager (ej. `gunicorn` con `uvicorn` workers).
- Aislar la base de datos y restringir acceso (Security Groups / reglas de firewall).
- Gestionar secretos mediante un gestor de secretos o variables de entorno seguras.

## Contribuir

1. Fork del repositorio.
2. Crear una rama `feature/...` o `fix/...`.
3. Abrir un Pull Request con una descripción clara.

## Licencia y contacto

Indica aquí la licencia del proyecto (por ejemplo `MIT`) y los datos de contacto del mantenedor.

---