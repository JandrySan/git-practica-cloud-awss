from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import datetime

app = FastAPI(
    title="API Restaurante Familia Sánchez",
    description="Backend para gestión de reservas",
    version="1.0.0"
)

# ✅ CORS: permite que el frontend en Cloud Run llame al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cuando tengas la URL de Cloud Run, ponla aquí
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos temporal en memoria (luego puedes conectar una DB real)
reservas_db: List[dict] = []


# ---------- MODELOS ----------

class Reserva(BaseModel):
    nombre: str
    fecha: str
    personas: str
    telefono: str


# ---------- ENDPOINTS ----------

@app.get("/")
def root():
    return {
        "mensaje": "API Restaurante Modelado y frontend prueba funcionando  ✅",
        "version": "1.0.0",
        "fecha": str(datetime.datetime.now())
    }


@app.get("/health")
def health_check():
    """Endpoint de salud para AWS Elastic Beanstalk"""
    return {"status": "healthy"}


@app.post("/reserva")
def crear_reserva(reserva: Reserva):
    """Recibe una reserva desde el formulario del frontend"""
    nueva = {
        "id": len(reservas_db) + 1,
        "nombre": reserva.nombre,
        "fecha": reserva.fecha,
        "personas": reserva.personas,
        "telefono": reserva.telefono,
        "creado_en": str(datetime.datetime.now())
    }
    reservas_db.append(nueva)
    print(f"📋 Nueva reserva recibida: {nueva}")
    return {
        "status": "ok",
        "mensaje": f"¡Reserva confirmada para {reserva.nombre} el {reserva.fecha}!",
        "reserva": nueva
    }


@app.get("/reservas")
def listar_reservas():
    """Lista todas las reservas recibidas"""
    return {
        "total": len(reservas_db),
        "reservas": reservas_db
    }
