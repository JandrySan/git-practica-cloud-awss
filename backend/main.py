from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Restaurante Familia Sanchez",
    description="Backend para gestion de reservas",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

reservas_db: List[dict] = []


class Reserva(BaseModel):
    nombre: str = Field(min_length=1)
    fecha: str = Field(min_length=1)
    personas: str = Field(min_length=1)
    telefono: str = Field(min_length=1)


@app.get("/")
def root():
    return {
        "mensaje": "API Restaurante Familia Sanchez funcionando 2205",
        "version": "1.0.0",
        "fecha": datetime.now().isoformat(),
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/reserva")
def crear_reserva(reserva: Reserva):
    try:
        total_personas = int(reserva.personas)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail="El numero de personas debe ser valido.",
        ) from exc

    if total_personas < 1:
        raise HTTPException(
            status_code=422,
            detail="La reserva debe ser para al menos una persona.",
        )

    nueva = {
        "id": len(reservas_db) + 1,
        "nombre": reserva.nombre,
        "fecha": reserva.fecha,
        "personas": str(total_personas),
        "telefono": reserva.telefono,
        "creado_en": datetime.now().isoformat(),
    }
    reservas_db.append(nueva)

    return {
        "status": "ok",
        "mensaje": f"Reserva confirmada para {reserva.nombre} el {reserva.fecha}.",
        "reserva": nueva,
    }


@app.get("/reservas")
def listar_reservas():
    return {
        "total": len(reservas_db),
        "reservas": reservas_db,
    }
