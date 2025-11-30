# Gestor de Reportes — Microservicio Híbrido (FastAPI + PostgreSQL + MongoDB)

API de inteligencia de negocio encargada de consolidar información. Implementa el patrón de **Persistencia Políglota**, cruzando datos relacionales de empleados (`PostgreSQL`) con datos transaccionales de pedidos (`MongoDB`) para generar dashboards en tiempo real.

---

## Tabla de contenidos

- [Características](#características)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación y ejecución (desarrollo)](#instalación-y-ejecución-desarrollo)
- [Configuración](#configuración)
- [Infraestructura de datos (Docker)](#infraestructura-de-datos-docker)
- [Endpoints principales](#endpoints-principales)
- [Documentación de la API](#documentación-de-la-api)
- [Despliegue sugerido](#despliegue-sugerido)
- [Contribuir](#contribuir)
- [Licencia y contacto](#licencia-y-contacto)

---

## Características

- Dashboard operativo con métricas de ventas por empleado.
- Integración asíncrona entre `PostgreSQL` (empleados) y `MongoDB` (pedidos).
- Lectura de datos cruzados entre microservicios (patrón de **persistencia políglota**).
- Endpoints documentados automáticamente con OpenAPI/Swagger.
- Preparado para generar dashboards y métricas en tiempo (casi) real.

---

## Tecnologías

- `FastAPI` — Framework principal de la API.
- `SQLModel` / `SQLAlchemy` — Capa de acceso a datos para `PostgreSQL`.
- `motor` — Driver asíncrono para `MongoDB`.
- `PostgreSQL` — Base de datos relacional (datos de empleados).
- `MongoDB` — Base de datos documental (datos de pedidos).
- `uvicorn` — Servidor ASGI para ejecución de la API.

---

## Estructura del proyecto

Raíz del servicio `microservicio-reportes`:

```text
microservicio-reportes/
├── main.py          # Lógica de negocio y definición de endpoints
├── database.py      # Configuración de conexiones (SQL + Mongo)
├── requirements.txt # Dependencias del proyecto
├── .env.example     # Variables de entorno de ejemplo
└── README.md        # Documentación (este archivo)


Requisitos

Python 3.10+

PostgreSQL con los datos de empleados disponibles

MongoDB con los datos de pedidos disponibles

pip y virtualenv (recomendado)

Opcional: Docker y docker-compose para levantar la infraestructura de datos

Instalación y ejecución (desarrollo)

Clonar el repositorio y entrar en el directorio del servicio:

git clone <URL_DEL_REPO>
cd microservicio-reportes


Crear y activar un entorno virtual:

python -m venv venv
.\venv\Scripts\activate


En Linux/macOS, la activación sería:

source venv/bin/activate


Instalar dependencias:

pip install -r requirements.txt


Crear el archivo de configuración a partir del ejemplo:

copy .env.example .env


Ajustar el archivo .env con las credenciales/hosts de tus bases de datos (ver sección Configuración
).

Ejecutar la aplicación en modo desarrollo:

uvicorn main:app --reload --port 8002


La API estará disponible en:
http://localhost:8002

Configuración

Editar el archivo .env (creado a partir de .env.example) y ajustar las variables de conexión:

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


Asegúrate de que los puertos y hosts coinciden con tus contenedores o instancias de base de datos.

Infraestructura de datos (Docker)

Para levantar rápidamente ambas bases de datos en entorno de desarrollo:

docker run -d --name postgres_db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=password123 \
  -e POSTGRES_DB=empleados_db \
  -p 5433:5432 \
  postgres:15

docker run -d --name mongo_db \
  -p 27017:27017 \
  mongo:7.0


Opcional: se puede añadir un archivo docker-compose.yml para orquestar:

postgres_db

mongo_db

microservicio-reportes (API)

Endpoints principales

GET /reportes/dashboard — Devuelve el dashboard operativo consolidado.

Ejemplo (cURL):

curl -X GET "http://localhost:8002/reportes/dashboard" \
  -H "accept: application/json"


Respuesta de ejemplo:

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


Nota: La estructura exacta de la respuesta puede variar según el modelo de datos y la lógica implementada en main.py.

Documentación de la API

FastAPI expone automáticamente la documentación interactiva:

Swagger UI:
http://localhost:8002/docs

ReDoc:
http://localhost:8002/redoc

Desde estas interfaces puedes probar los endpoints, ver esquemas de entrada/salida y explorar el modelo de datos.

Despliegue sugerido

Para un entorno de producción se recomienda:

Contenerizar la API (por ejemplo, con Docker) y correrla detrás de un proxy inverso (NGINX).

Usar un process manager como gunicorn con workers uvicorn:

gunicorn -k uvicorn.workers.UvicornWorker main:app


Aislar las bases de datos en una red privada y restringir el acceso mediante:

Security Groups (en la nube)

Reglas de firewall

Gestionar secretos (credenciales de DB, tokens, etc.) mediante:

Variables de entorno seguras

Gestores de secretos (AWS Secrets Manager, Vault, etc.)

Configurar logs centralizados y monitoreo (Prometheus, Grafana, ELK, etc.)

Contribuir

Haz un fork del repositorio.

Crea una rama para tu cambio:

git checkout -b feature/mi-nueva-funcionalidad
# o
git checkout -b fix/correccion-bug-x


Realiza tus cambios y confirma los commits con mensajes claros.

Envía un Pull Request describiendo:

El problema que se resuelve

Los cambios realizados

Cómo probarlos

Licencia y contacto

Licencia: MIT (o la que corresponda a tu proyecto).

Mantenedor: [Nombre del mantenedor]

Contacto: [correo@ejemplo.com
]

Actualiza esta sección con la información real de tu proyecto antes de publicarlo.