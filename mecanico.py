"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [completar]
- Nicolás Múnera - ID: [completar]

ADT Mecanico: representa un mecánico del taller, con una especialidad y
como máximo una orden asignada a la vez.
"""

import itertools
from typing import Optional

from enums import TipoServicio


class Mecanico:
    """
    Representa a un mecánico. Invariante central: nunca puede tener más
    de una orden asignada simultáneamente.
    """

    _contador_id = itertools.count(1)

    def __init__(self, nombre: str, especialidad: TipoServicio):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del mecánico no puede estar vacío")
        if not isinstance(especialidad, TipoServicio):
            raise ValueError("La especialidad debe ser un TipoServicio válido")

        self._id = next(Mecanico._contador_id)
        self._nombre = nombre.strip()
        self._especialidad = especialidad
        self._orden_asignada = None
        self._disponible = True

    def asignarOrden(self, orden) -> None:
        if orden is None:
            raise ValueError("La orden no puede ser None")
        if not self.estaDisponible():
            raise ValueError(f"El mecánico {self._nombre} ya tiene una orden asignada")
        self._orden_asignada = orden
        self._disponible = False

    def completarOrden(self) -> None:
        if self._orden_asignada is None:
            raise ValueError(f"El mecánico {self._nombre} no tiene ninguna orden asignada")
        self._orden_asignada = None
        self._disponible = True

    def estaDisponible(self) -> bool:
        return self._disponible and self._orden_asignada is None

    def marcarDisponibilidad(self, disponible: bool) -> None:
        self._disponible = disponible

    def getOrdenAsignada(self):
        return self._orden_asignada

    # ---------- Getters ----------
    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def get_especialidad(self) -> TipoServicio:
        return self._especialidad

    def __str__(self) -> str:
        estado = "disponible" if self.estaDisponible() else "ocupado"
        return f"Mecánico[{self._id}] {self._nombre} ({self._especialidad.value}) - {estado}"


if __name__ == "__main__":
    # --- Caso típico ---
    m1 = Mecanico("Pedro Gómez", TipoServicio.MOTOR)
    assert m1.estaDisponible() is True

    m1.asignarOrden("orden_dummy_1")
    assert m1.estaDisponible() is False
    assert m1.getOrdenAsignada() == "orden_dummy_1"

    # --- Caso de error: asignar segunda orden sin liberar la primera ---
    try:
        m1.asignarOrden("orden_dummy_2")
        assert False, "Debió lanzar excepción: mecánico ya ocupado"
    except ValueError:
        pass

    # --- Liberar y volver a asignar ---
    m1.completarOrden()
    assert m1.estaDisponible() is True
    assert m1.getOrdenAsignada() is None

    # --- Caso de error: completar sin tener orden asignada ---
    try:
        m1.completarOrden()
        assert False, "Debió lanzar excepción: no tiene orden asignada"
    except ValueError:
        pass

    # --- Caso de error: nombre vacío / especialidad inválida ---
    try:
        Mecanico("", TipoServicio.FRENOS)
        assert False, "Debió lanzar excepción por nombre vacío"
    except ValueError:
        pass

    try:
        Mecanico("Nombre válido", "Motor")  # string, no TipoServicio
        assert False, "Debió lanzar excepción por especialidad inválida"
    except ValueError:
        pass

    print("Todas las pruebas de Mecanico pasaron correctamente.")
