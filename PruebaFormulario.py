from fastapi import FastAPI, Form
from pydantic import BaseModel
import mysql.connector
import os

app = FastAPI()

MYSQL_HOST = os.getenv("34.247.119.184")
MYSQL_USER = os.getenv("maria.moran")
MYSQL_PASS = os.getenv("FpGa27Ura3")
MYSQL_DB = os.getenv("BI_FEEDBACK")

@app.post("/insertar")
async def insertar(usuario: str = Form(...), comentario: str = Form(...), origen: str = Form("PowerApps")):
    conn = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASS, database=MYSQL_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO BI_FEEDBACK.feedback_usuarios (usuario, comentario, origen) VALUES (%s, %s, %s)", (usuario, comentario, origen))
    conn.commit()
    cursor.close()
    conn.close()
    return {"status": "ok"}
