"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [completar]
- Nicolás Múnera - ID: [000280908]

ADT OrdenReparacion: representa la solicitud de reparación de un vehículo,
con un ciclo de vida controlado por estados (enum EstadoOrden).
"""

import itertools
from datetime import datetime
from typing import Optional

from enums import EstadoOrden, TipoServicio, TRANSICIONES_VALIDAS


class OrdenReparacion:
    """
    Invariantes:
      - El id es único e inmutable.
      - No puede pasar a Reparada sin tener mecanicoAsignado.
      - Solo puede entregarse si está en estado Reparada.
      - fechaFinalizacion (cuando existe) es posterior o igual a fechaIngreso.
    """

    _contador_id = itertools.count(1)

    def __init__(self, descripcion: str, tipo_servicio: TipoServicio, cliente):
        if not descripcion or not descripcion.strip():
            raise ValueError("La descripción de la falla no puede estar vacía")
        if not isinstance(tipo_servicio, TipoServicio):
            raise ValueError("El tipo de servicio debe ser un TipoServicio válido")
        if cliente is None:
            raise ValueError("La orden debe estar asociada a un cliente")

        self._id = next(OrdenReparacion._contador_id)
        self._descripcion = descripcion.strip()
        self._tipo_servicio = tipo_servicio
        self._cliente = cliente
        self._estado = EstadoOrden.RECIBIDA
        self._mecanico_asignado = None
        self._fecha_ingreso = datetime.now()
        self._fecha_finalizacion: Optional[datetime] = None

    def asignarMecanico(self, mecanico) -> None:
        if mecanico is None:
            raise ValueError("El mecánico no puede ser None")
        self._mecanico_asignado = mecanico
        self.cambiarEstado(EstadoOrden.ASIGNADA)

    def cambiarEstado(self, nuevo_estado: EstadoOrden) -> None:
        if not isinstance(nuevo_estado, EstadoOrden):
            raise ValueError("Estado inválido")
        permitidos = TRANSICIONES_VALIDAS[self._estado]
        if nuevo_estado not in permitidos:
            raise ValueError(
                f"Transición inválida: {self._estado.value} -> {nuevo_estado.value}"
            )
        self._estado = nuevo_estado

    def finalizarReparacion(self) -> None:
        if self._mecanico_asignado is None:
            raise ValueError("No se puede finalizar una orden sin mecánico asignado")
        self.cambiarEstado(EstadoOrden.REPARADA)
        self._fecha_finalizacion = datetime.now()

    def entregar(self) -> None:
        if self._estado != EstadoOrden.REPARADA:
            raise ValueError("Solo se puede entregar una orden en estado Reparada")
        self.cambiarEstado(EstadoOrden.ENTREGADA)

    def tiempoEnTaller(self):
        fin = self._fecha_finalizacion or datetime.now()
        return fin - self._fecha_ingreso

    # ---------- Getters ----------
    def get_id(self) -> int:
        return self._id

    def get_descripcion(self) -> str:
        return self._descripcion

    def get_estado(self) -> EstadoOrden:
        return self._estado

    def get_tipo_servicio(self) -> TipoServicio:
        return self._tipo_servicio

    def get_cliente(self):
        return self._cliente

    def get_mecanico_asignado(self):
        return self._mecanico_asignado

    def get_fecha_ingreso(self) -> datetime:
        return self._fecha_ingreso

    def get_fecha_finalizacion(self) -> Optional[datetime]:
        return self._fecha_finalizacion

    def __str__(self) -> str:
        return f"Orden[{self._id}] {self._tipo_servicio.value} - {self._estado.value}"


if __name__ == "__main__":
    from mecanico import Mecanico
    from cliente import Cliente

    cliente = Cliente("Marta Ruiz", "marta@example.com", "3001112233", "JKL456")
    mecanico = Mecanico("Diego Torres", TipoServicio.FRENOS)

    # --- Caso típico: creación ---
    orden = OrdenReparacion("Frenos chillan", TipoServicio.FRENOS, cliente)
    assert orden.get_estado() == EstadoOrden.RECIBIDA

    # --- Caso de error: finalizar sin mecánico asignado ---
    try:
        orden.finalizarReparacion()
        assert False, "Debió lanzar excepción: no se puede finalizar sin mecánico"
    except ValueError:
        pass

    # --- Asignación ---
    orden.asignarMecanico(mecanico)
    assert orden.get_estado() == EstadoOrden.ASIGNADA
    assert orden.get_mecanico_asignado() is mecanico

    # --- Caso de error: transición inválida (saltarse EnReparacion) ---
    try:
        orden.cambiarEstado(EstadoOrden.REPARADA)
        assert False, "Debió lanzar excepción: transición inválida Asignada->Reparada"
    except ValueError:
        pass

    # --- Flujo completo válido ---
    orden.cambiarEstado(EstadoOrden.EN_REPARACION)
    orden.finalizarReparacion()
    assert orden.get_estado() == EstadoOrden.REPARADA
    assert orden.get_fecha_finalizacion() is not None
    assert orden.get_fecha_finalizacion() >= orden.get_fecha_ingreso()

    orden.entregar()
    assert orden.get_estado() == EstadoOrden.ENTREGADA

    # --- Caso de error: entregar dos veces ---
    try:
        orden.entregar()
        assert False, "Debió lanzar excepción: ya está entregada"
    except ValueError:
        pass

    print("Todas las pruebas de OrdenReparacion pasaron correctamente.")
