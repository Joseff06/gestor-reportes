# Gestor de Reportes — Microservicio Híbrido (FastAPI + SQL + NoSQL)

Servicio de inteligencia de negocio encargado de consolidar información. Implementa el patrón de **Persistencia Políglota**, cruzando datos relacionales de empleados (`PostgreSQL`) con datos transaccionales de pedidos (`MongoDB`) para generar dashboards en tiempo real.

-----

## 📋 Tabla de contenidos

- [Características](#características)
- [🎯 ASRs Atacados](#-asrs-atacados-requisitos-de-arquitectura)
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

- Dashboard operativo con métricas de ventas por empleado.
- Conexión dual asíncrona (SQL y NoSQL simultáneos).
- Alto rendimiento mediante el uso de drivers no bloqueantes.
- Documentación automática con OpenAPI/Swagger.

## 🎯 ASRs Atacados (Requisitos de Arquitectura)

Este microservicio fue diseñado para cumplir con:

* **ASR - Mantenibilidad y Modificabilidad:** Al estar desacoplado de la lógica de usuarios y pedidos, este módulo puede ser actualizado, apagado o modificado sin interrumpir la operación de venta ni el acceso a datos de empleados.
* **ASR - Disponibilidad:** Implementa el patrón de **Persistencia Políglota**. Incluso si el servicio de creación de pedidos (Django) tiene alta latencia, este servicio de lectura puede consultar directamente la base de datos MongoDB sin pasar por la API del compañero, garantizando respuestas rápidas.

## Tecnologías

- `FastAPI` (API Framework)
- `SQLModel` (Conexión a PostgreSQL)
- `Motor` (Driver asíncrono para MongoDB)
- `PostgreSQL` (Datos maestros de empleados)
- `MongoDB` (Datos transaccionales de pedidos)
- `uvicorn` (Servidor ASGI)

## Estructura del proyecto

Raíz del servicio `microservicio-reportes`:

```text
main.py            # Lógica de negocio y endpoints
database.py        # Configuración de conexiones híbridas
requirements.txt   # Dependencias del proyecto
.env.example       # Variables de entorno de ejemplo
README.md          # Documentación (este archivo)
```

## Requisitos
Python 3.10+

PostgreSQL activo (con datos de usuarios creados)

MongoDB activo (con pedidos registrados)

pip y virtualenv (recomendado)

## Instalación y ejecución (desarrollo)
1. Clonar el repositorio y entrar en el directorio del servicio:

PowerShell

git clone <URL_DEL_REPO>
cd microservicio-reportes

2. Crear y activar un entorno virtual:

PowerShell

python -m venv venv
.\venv\Scripts\activate

3. Instalar dependencias:

PowerShell

pip install -r requirements.txt

4. Crear el archivo de configuración a partir del ejemplo:

PowerShell

copy .env.example .env
Editar .env y ajustar las variables para tu entorno (ver sección "Configuración").

5. Iniciar el servidor en modo desarrollo:

PowerShell

uvicorn main:app --reload --port 8002

### El servidor quedará disponible en http://localhost:8002.

Configuración
Usar el archivo .env para configurar ambas conexiones. Asegúrate de que los puertos coincidan con tu Docker.

Ini, TOML

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
Infraestructura de Datos (Docker)
Para que este microservicio funcione, necesita que la infraestructura de datos esté activa. Puedes levantar ambas bases de datos con Docker:

Bash

# PostgreSQL (Puerto 5433)
docker run -d --name postgres_db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=password123 -e POSTGRES_DB=empleados_db -p 5433:5432 postgres:15

# MongoDB (Puerto 27017)
docker run -d --name mongo_db -p 27017:27017 mongo:7.0
Documentación de la API
FastAPI expone documentación interactiva OpenAPI en:

Swagger UI: http://localhost:8002/docs

ReDoc: http://localhost:8002/redoc

## Ejemplo de uso (Dashboard)
Bash

curl -X GET "http://localhost:8002/reportes/dashboard" \
  -H "accept: application/json"
Respuesta esperada:

JSON

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
Despliegue sugerido
Para producción:

Ejecutar en contenedores orquestados (ECS/Kubernetes).

Aislar las bases de datos en subredes privadas.

Usar un API Gateway para unificar los endpoints.