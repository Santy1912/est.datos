"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [000532192]
- Nicolás Múnera - ID: [000280908]
"""

from enum import Enum


class EstadoOrden(Enum):
    """Estados posibles del ciclo de vida de una OrdenReparacion."""
    RECIBIDA = "Recibida"
    ASIGNADA = "Asignada"
    EN_REPARACION = "EnReparacion"
    REPARADA = "Reparada"
    ENTREGADA = "Entregada"


class TipoServicio(Enum):
    """Tipos de servicio que puede requerir un vehículo."""
    MOTOR = "Motor"
    FRENOS = "Frenos"
    ELECTRICIDAD = "Electricidad"
    CARROCERIA = "Carroceria"
    LLANTAS = "Llantas"
    SUSPENSION = "Suspension"


# Tabla de transiciones válidas: desde qué estado se puede pasar a cuáles otros.
# Se usa para validar cambiarEstado() y evitar saltos ilegales (ej. Recibida -> Reparada).
TRANSICIONES_VALIDAS = {
    EstadoOrden.RECIBIDA: {EstadoOrden.ASIGNADA},
    EstadoOrden.ASIGNADA: {EstadoOrden.EN_REPARACION},
    EstadoOrden.EN_REPARACION: {EstadoOrden.REPARADA},
    EstadoOrden.REPARADA: {EstadoOrden.ENTREGADA},
    EstadoOrden.ENTREGADA: set(),
}


if __name__ == "__main__":
    # Pruebas básicas de los enums y la tabla de transiciones
    assert EstadoOrden.RECIBIDA.value == "Recibida"
    assert TipoServicio.MOTOR.value == "Motor"
    assert EstadoOrden.ASIGNADA in TRANSICIONES_VALIDAS[EstadoOrden.RECIBIDA]
    assert EstadoOrden.REPARADA not in TRANSICIONES_VALIDAS[EstadoOrden.RECIBIDA]
    assert TRANSICIONES_VALIDAS[EstadoOrden.ENTREGADA] == set()

    print("Todas las pruebas de enums pasaron correctamente.")
