"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [completar]
- Nicolás Múnera - ID: [completar]

Iterador personalizado #1: recorre únicamente las órdenes que se encuentran
en un estado específico. Implementa explícitamente el patrón Iterator de
Python (__iter__ / __next__), a diferencia de los iteradores basados en
generadores usados en Queue, Bag y ListaEnlazada (iterador #2: historial).
"""


class IteradorPorEstado:
    """
    Recibe una colección de OrdenReparacion y un EstadoOrden objetivo.
    Al iterar, va devolviendo solo las órdenes cuyo estado coincide,
    avanzando de forma perezosa sobre una copia (snapshot) de la colección.
    """

    def __init__(self, ordenes, estado):
        self._ordenes = list(ordenes)  # snapshot: evita efectos de mutaciones concurrentes
        self._estado = estado
        self._indice = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self._indice < len(self._ordenes):
            orden = self._ordenes[self._indice]
            self._indice += 1
            if orden.get_estado() == self._estado:
                return orden
        raise StopIteration


if __name__ == "__main__":
    from enums import EstadoOrden, TipoServicio
    from orden_reparacion import OrdenReparacion
    from cliente import Cliente

    cliente = Cliente("Test Cliente", "test@example.com", "300", "TST111")
    o1 = OrdenReparacion("Falla 1", TipoServicio.MOTOR, cliente)
    o2 = OrdenReparacion("Falla 2", TipoServicio.MOTOR, cliente)

    # --- Caso típico: filtra solo las que están en RECIBIDA ---
    it = IteradorPorEstado([o1, o2], EstadoOrden.RECIBIDA)
    assert list(it) == [o1, o2]

    # --- Caso borde: colección vacía ---
    it_vacio = IteradorPorEstado([], EstadoOrden.RECIBIDA)
    assert list(it_vacio) == []

    # --- Sigue el protocolo estándar de Python: StopIteration al agotarse ---
    it2 = IteradorPorEstado([o1], EstadoOrden.RECIBIDA)
    assert next(it2) is o1
    try:
        next(it2)
        assert False, "Debió lanzar StopIteration al agotarse el iterador"
    except StopIteration:
        pass

    print("Todas las pruebas de IteradorPorEstado pasaron correctamente.")
