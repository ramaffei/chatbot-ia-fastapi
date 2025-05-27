import secrets
from datetime import date, datetime

import pytz  # type: ignore


def es_dia_habil(fecha: date, feriados: list[str] | None = None) -> bool:
    if fecha.weekday() >= 5:
        return False

    if feriados is None:
        feriados = []

    if fecha in feriados:
        return False

    return True


def cambio_zona_horaria(fecha: str) -> str:
    return (
        datetime.fromisoformat(fecha + "+00:00")
        .astimezone(pytz.timezone("America/Argentina/Buenos_Aires"))
        .isoformat()
    )


def negativos_a_positivos(solicitud: dict) -> dict:
    for key, value in solicitud.items():
        if type(value) is int or type(value) is float:
            solicitud[key] = round(value, 4) if value >= 0 else round(value * -1, 4)
    return solicitud


def generar_codigo() -> str:
    return f"{secrets.randbelow(10**9):09d}"  # Genera un número aleatorio de 6 dígitos


def generar_headers_attach_file(nombre_archivo: str) -> dict:
    return {"Content-Disposition": f"attachment; filename={nombre_archivo}"}
