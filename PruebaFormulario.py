# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import mysql.connector

app = FastAPI()

class Objetivo(BaseModel):
    anio: int
    mes: int
    clientes_brutos: Optional[int] = None
    clientes_netos: Optional[int] = None
    rgus_netas: Optional[int] = None

def get_conn():
    return mysql.connector.connect(
        host="10.118.33.11",
        user="replication",
        password="Inc0nc3rt!2025",
        database="BI_VODAFONE_E2E"
    )
@app.post("/upsert_objetivos")
def upsert(obj: Objetivo):
    try:
        conn = get_conn()
        cur = conn.cursor()
        # ¿Existe?
        cur.execute(
            "SELECT COUNT(*) FROM Objetivos_Edealer WHERE Anio=%s AND Mes=%s",
            (obj.anio, obj.mes)
        )
        exists = cur.fetchone()[0] > 0

        if exists:
            parts = []
            vals = []
            if obj.clientes_brutos is not None:
                parts.append("clientes_brutos=%s"); vals.append(obj.clientes_brutos)
            if obj.clientes_netos is not None:
                parts.append("clientes_netos=%s"); vals.append(obj.clientes_netos)
            if obj.rgus_netas is not None:
                parts.append("rgus_netas=%s"); vals.append(obj.rgus_netas)

            if parts:
                sql = "UPDATE Objetivos_Edealer SET " + ", ".join(parts) + " WHERE Anio=%s AND Mes=%s"
                vals.extend([obj.anio, obj.mes])
                cur.execute(sql, tuple(vals))
                conn.commit()
        else:
            cur.execute(
                "INSERT INTO Objetivos_Edealer (Anio, Mes, clientes_brutos, clientes_netos, rgus_netas) VALUES (%s,%s,%s,%s,%s)",
                (obj.anio, obj.mes, obj.clientes_brutos, obj.clientes_netos, obj.rgus_netas)
            )
            conn.commit()
        return {"status": "ok"}

    except mysql.connector.Error as e:
        return {"status": "error", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        try:
            cur.close()
            conn.close()
        except:
            pass

        
@app.get("/upsert_objetivos_simple")
def upsert_simple(anio: int, mes: int, clientes_brutos: int = None, clientes_netos: int = None, rgus_netas: int = None):
    conn = get_conn()
    cur = conn.cursor()

    # Revisar si existe
    cur.execute("SELECT COUNT(*) FROM Objetivos_Edealer WHERE Anio=%s AND Mes=%s", (anio, mes))
    exists = cur.fetchone()[0] > 0

    if exists:
        parts = []
        vals = []
        if clientes_brutos is not None:
            parts.append("clientes_brutos=%s"); vals.append(clientes_brutos)
        if clientes_netos is not None:
            parts.append("clientes_netos=%s"); vals.append(clientes_netos)
        if rgus_netas is not None:
            parts.append("rgus_netas=%s"); vals.append(rgus_netas)

        if parts:
            sql = "UPDATE Objetivos_Edealer SET " + ", ".join(parts) + " WHERE Anio=%s AND Mes=%s"
            vals.extend([anio, mes])
            cur.execute(sql, tuple(vals))
            conn.commit()
    else:
        cur.execute(
            "INSERT INTO Objetivos_Edealer (Anio, Mes, clientes_brutos, clientes_netos, rgus_netas) VALUES (%s,%s,%s,%s,%s)",
            (anio, mes, clientes_brutos, clientes_netos, rgus_netas)
        )
        conn.commit()

    cur.close()
    conn.close()
    return {"status": "ok"}
