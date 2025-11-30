from fastapi import FastAPI, Depends
from sqlmodel import Session, text
from database import get_sql_session, pedidos_collection

app = FastAPI(title="Microservicio de Reportes (Híbrido)", version="1.0.0")

@app.get("/reportes/dashboard")
async def dashboard_general(session: Session = Depends(get_sql_session)):
    """
    Reporte Híbrido:
    1. Obtiene empleados desde PostgreSQL (Puerto 5433).
    2. Cruza datos con MongoDB (Puerto 27017).
    """
    
    # --- PASO 1: Leer SQL (Usuarios) ---
    try:
        # Traemos username y rol de la tabla usuario
        query = text("SELECT username, rol FROM usuario")
        resultado_sql = session.exec(query).all()
    except Exception as e:
        return {
            "error": "Fallo conectando a SQL (5433). ¿Creaste usuarios en el puerto 8001?", 
            "detalle": str(e)
        }

    reporte_consolidado = []
    total_ventas_empresa = 0

    # --- PASO 2: Cruzar con Mongo (Pedidos) ---
    for row in resultado_sql:
        username = row[0]
        rol = row[1]
        
        # Consultamos a Mongo: "¿Cuántos pedidos tienen 'vendedor_id' == username?"
        cantidad_pedidos = await pedidos_collection.count_documents({"vendedor_id": username})
        
        total_ventas_empresa += cantidad_pedidos
        
        reporte_consolidado.append({
            "empleado": username,
            "rol": rol,
            "pedidos_realizados": cantidad_pedidos,
            "estado": "Activo" if cantidad_pedidos > 0 else "Sin ventas"
        })

    return {
        "titulo": "Dashboard Operativo - Sprint 4",
        "metricas_globales": {
            "total_empleados": len(resultado_sql),
            "total_pedidos_procesados": total_ventas_empresa
        },
        "detalle_por_vendedor": reporte_consolidado
    }

@app.get("/")
def home():
    return {"status": "Microservicio de Reportes Online (Puerto 8002)"}

@app.get("/debug/collections")
async def ver_colecciones():
    from database import mongo_db
    nombres = await mongo_db.list_collection_names()
    return {"colecciones_en_mongo": nombres}