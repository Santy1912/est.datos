"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [000532192]
- Nicolás Múnera - ID: [000280908]

ADT TallerSystem: coordina órdenes, mecánicos, tipos de servicio válidos
e historial de reparaciones finalizadas.
"""

from typing import List, Optional

from codigo_fuente.enums import EstadoOrden, TipoServicio
from codigo_fuente.queue_fifo import Queue
from codigo_fuente.bag import Bag
from codigo_fuente.lista_enlazada import ListaEnlazada
from codigo_fuente.orden_reparacion import OrdenReparacion
from codigo_fuente.mecanico import Mecanico
from codigo_fuente.cliente import Cliente
from codigo_fuente.iterador_por_estado import IteradorPorEstado


class TallerSystem:
    """
    Invariantes:
      - Cada orden tiene un id único en todo el sistema.
      - ordenesPendientes siempre refleja el orden real de llegada (FIFO).
      - Solo existen órdenes con tipos de servicio previamente registrados.
    """

    def __init__(self):
        self._ordenes_pendientes: Queue = Queue()
        self._todas_las_ordenes: Bag = Bag()
        self._historial: ListaEnlazada = ListaEnlazada()
        self._mecanicos: Bag = Bag()
        self._tipos_servicio: Bag = Bag()

    # ---------- Configuración inicial ----------
    def agregarMecanico(self, mecanico: Mecanico) -> None:
        if mecanico is None:
            raise ValueError("El mecánico no puede ser None")
        self._mecanicos.add(mecanico)

    def agregarTipoServicio(self, tipo: TipoServicio) -> None:
        if not isinstance(tipo, TipoServicio):
            raise ValueError("Tipo de servicio inválido")
        if not self._tipos_servicio.contains(tipo):
            self._tipos_servicio.add(tipo)

    # ---------- Gestión de órdenes ----------
    def crearOrden(self, descripcion: str, tipo_servicio: TipoServicio, cliente: Cliente) -> OrdenReparacion:
        if not self._tipos_servicio.contains(tipo_servicio):
            raise ValueError(f"Tipo de servicio no habilitado en este taller: {tipo_servicio}")
        orden = OrdenReparacion(descripcion, tipo_servicio, cliente)
        self._todas_las_ordenes.add(orden)
        self._ordenes_pendientes.enqueue(orden)
        return orden

    def asignarOrdenAutomatica(self) -> Optional[OrdenReparacion]:
        """
        Toma la orden más antigua de la cola (FIFO) y la asigna al primer
        mecánico disponible con la especialidad requerida. Si no hay
        mecánico disponible, la orden permanece intacta en la cola.
        """
        if self._ordenes_pendientes.esta_vacia():
            return None

        orden = self._ordenes_pendientes.peek()  # no remover todavía
        mecanico_candidato = self._buscar_mecanico_disponible(orden.get_tipo_servicio())

        if mecanico_candidato is None:
            return None  # la orden queda intacta en la cola

        self._ordenes_pendientes.dequeue()  # ahora sí se remueve
        orden.asignarMecanico(mecanico_candidato)
        mecanico_candidato.asignarOrden(orden)
        return orden

    def _buscar_mecanico_disponible(self, especialidad: TipoServicio) -> Optional[Mecanico]:
        for mecanico in self._mecanicos:
            if mecanico.get_especialidad() == especialidad and mecanico.estaDisponible():
                return mecanico
        return None

    def asignarOrdenManual(self, orden: OrdenReparacion, mecanico: Mecanico) -> None:
        if not mecanico.estaDisponible():
            raise ValueError(f"El mecánico {mecanico.get_nombre()} no está disponible")
        self._remover_de_pendientes(orden)
        orden.asignarMecanico(mecanico)
        mecanico.asignarOrden(orden)

    def _remover_de_pendientes(self, orden: OrdenReparacion) -> None:
        """Reconstruye la cola sin la orden dada (si estaba presente)."""
        temporal = Queue()
        encontrada = False
        while not self._ordenes_pendientes.esta_vacia():
            actual = self._ordenes_pendientes.dequeue()
            if actual is orden and not encontrada:
                encontrada = True
                continue
            temporal.enqueue(actual)
        while not temporal.esta_vacia():
            self._ordenes_pendientes.enqueue(temporal.dequeue())

    def cambiarEstadoOrden(self, orden_id: int, nuevo_estado: EstadoOrden) -> None:
        orden = self._buscar_orden_por_id(orden_id)
        orden.cambiarEstado(nuevo_estado)

    def finalizarOrden(self, orden_id: int) -> None:
        orden = self._buscar_orden_por_id(orden_id)
        mecanico = orden.get_mecanico_asignado()
        orden.finalizarReparacion()
        if mecanico is not None:
            mecanico.completarOrden()
        self._historial.agregar_al_frente(orden)

    def entregarOrden(self, orden_id: int) -> None:
        orden = self._buscar_orden_por_id(orden_id)
        orden.entregar()

    def _buscar_orden_por_id(self, orden_id: int) -> OrdenReparacion:
        for orden in self._todas_las_ordenes:
            if orden.get_id() == orden_id:
                return orden
        raise ValueError(f"No existe una orden con id {orden_id}")

    # ---------- Consultas / Reportes (uso de iteradores) ----------
    def obtenerOrdenesPorEstado(self, estado: EstadoOrden) -> IteradorPorEstado:
        return IteradorPorEstado(self._todas_las_ordenes, estado)

    def obtenerOrdenesPorTipo(self, tipo_servicio: TipoServicio) -> List[OrdenReparacion]:
        return [orden for orden in self._todas_las_ordenes if orden.get_tipo_servicio() == tipo_servicio]

    def obtenerOrdenDeMecanico(self, mecanico: Mecanico):
        return mecanico.getOrdenAsignada()

    def listar_pendientes(self) -> List[OrdenReparacion]:
        """Lista las órdenes pendientes en orden FIFO, sin removerlas de la cola."""
        return list(self._ordenes_pendientes)

    def iterar_historial(self):
        """Recorre el historial de reparaciones finalizadas, más reciente primero."""
        return iter(self._historial)

    def generarEstadisticas(self) -> dict:
        por_estado = {
            estado.value: sum(1 for o in self._todas_las_ordenes if o.get_estado() == estado)
            for estado in EstadoOrden
        }
        return {
            "total_ordenes": self._todas_las_ordenes.size(),
            "pendientes_en_cola": self._ordenes_pendientes.size(),
            "en_historial": self._historial.size(),
            "por_estado": por_estado,
        }


if __name__ == "__main__":
    sistema = TallerSystem()

    # ---------- Configuración inicial ----------
    sistema.agregarTipoServicio(TipoServicio.MOTOR)
    sistema.agregarTipoServicio(TipoServicio.FRENOS)

    mecanico_motor = Mecanico("Carlos Vélez", TipoServicio.MOTOR)
    mecanico_frenos = Mecanico("Julia Ospina", TipoServicio.FRENOS)
    sistema.agregarMecanico(mecanico_motor)
    sistema.agregarMecanico(mecanico_frenos)

    cliente1 = Cliente("Santiago Zuluaga", "santi@gmail.com", "3011112222", "GVN211")

    # ---------- Caso de error: tipo de servicio no habilitado ----------
    try:
        sistema.crearOrden("Falla eléctrica", TipoServicio.ELECTRICIDAD, cliente1)
        assert False, "Debió lanzar excepción: tipo de servicio no registrado"
    except ValueError:
        pass

    # ---------- Crear orden y verificar cola FIFO ----------
    orden1 = sistema.crearOrden("Motor con ruido extraño", TipoServicio.MOTOR, cliente1)
    assert orden1.get_estado() == EstadoOrden.RECIBIDA
    assert sistema.listar_pendientes() == [orden1]

    # ---------- Asignación automática ----------
    asignada = sistema.asignarOrdenAutomatica()
    assert asignada is orden1
    assert orden1.get_estado() == EstadoOrden.ASIGNADA
    assert mecanico_motor.estaDisponible() is False
    assert sistema.listar_pendientes() == []

    # ---------- Caso borde: asignación automática sin pendientes ----------
    assert sistema.asignarOrdenAutomatica() is None

    # ---------- Flujo completo hasta entrega ----------
    sistema.cambiarEstadoOrden(orden1.get_id(), EstadoOrden.EN_REPARACION)
    sistema.finalizarOrden(orden1.get_id())
    assert orden1.get_estado() == EstadoOrden.REPARADA
    assert mecanico_motor.estaDisponible() is True  # se liberó al finalizar
    assert list(sistema.iterar_historial()) == [orden1]

    sistema.entregarOrden(orden1.get_id())
    assert orden1.get_estado() == EstadoOrden.ENTREGADA

    # ---------- Caso borde: sin mecánico disponible para la especialidad ----------
    orden2 = sistema.crearOrden("Frenos gastados", TipoServicio.FRENOS, cliente1)
    orden3 = sistema.crearOrden("Cambio de pastillas", TipoServicio.FRENOS, cliente1)
    sistema.asignarOrdenAutomatica()  # asigna orden2 al único mecánico de frenos
    assert orden2.get_estado() == EstadoOrden.ASIGNADA
    resultado = sistema.asignarOrdenAutomatica()  # mecanico_frenos ya está ocupado
    assert resultado is None
    assert sistema.listar_pendientes() == [orden3]

    # ---------- Iterador por estado ----------
    asignadas = list(sistema.obtenerOrdenesPorEstado(EstadoOrden.ASIGNADA))
    assert orden2 in asignadas
    assert orden1 not in asignadas  # orden1 ya está Entregada

    # ---------- Caso de error: id inexistente ----------
    try:
        sistema.cambiarEstadoOrden(99999, EstadoOrden.EN_REPARACION)
        assert False, "Debió lanzar excepción: id inexistente"
    except ValueError:
        pass

    # ---------- Estadísticas ----------
    stats = sistema.generarEstadisticas()
    assert stats["total_ordenes"] == 3
    assert stats["pendientes_en_cola"] == 1

    print("Todas las pruebas de TallerSystem pasaron correctamente.")
