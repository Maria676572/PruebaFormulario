from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

# --- 1️⃣ Permitir CORS (para que Power Apps/BI puedan acceder) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puedes restringir luego
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2️⃣ Conexión con MySQL ---
def get_db_connection():
    return mysql.connector.connect(
        host="34.247.119.184",
        user="maria.moran",
        password="FpGa27Ura3",
        database="BI_FEEDBACK"
    )

# --- 3️⃣ Endpoint de prueba ---
@app.get("/")
def root():
    return {"status": "ok", "message": "API corriendo correctamente"}

# --- 4️⃣ Endpoint para recibir datos de Power Apps ---
@app.post("/insertar_dato")
async def insertar_dato(request: Request):
    data = await request.json()
    nombre = data.get("nombre")
    valor = data.get("valor")

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO tabla_pruebas (nombre, valor) VALUES (%s, %s)"
    cursor.execute(sql, (nombre, valor))
    conn.commit()

    cursor.close()
    conn.close()

    return {"status": "ok", "mensaje": f"Dato insertado correctamente: {nombre}"}
