from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# --- Permitir CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelo de datos esperado ---
class Dato(BaseModel):
    nombre: str
    valor: float

# --- Conexión MySQL ---
def get_db_connection():
    return mysql.connector.connect(
        host="34.247.119.184",
        user="maria.moran",
        password="FpGa27Ura3",
        database="BI_FEEDBACK"
    )

# --- Endpoint de prueba ---
@app.get("/")
def root():
    return {"status": "ok", "message": "API corriendo correctamente"}

# --- Endpoint para insertar datos ---
@app.post("/insertar_dato")
async def insertar_dato(dato: Dato):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO tabla_pruebas (nombre, valor) VALUES (%s, %s)"
    cursor.execute(sql, (dato.nombre, dato.valor))
    conn.commit()

    cursor.close()
    conn.close()

    return {"status": "ok", "mensaje": f"Dato insertado correctamente: {dato.nombre}"}
