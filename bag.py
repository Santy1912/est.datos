"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [completar]
- Nicolás Múnera - ID: [completar]

ADT Bag: colección no ordenada que permite duplicados y NO soporta remoción.
"""

from typing import Generic, TypeVar, Optional, Iterator

T = TypeVar("T")


class _Nodo(Generic[T]):
    __slots__ = ("valor", "siguiente")

    def __init__(self, valor: T):
        self.valor = valor
        self.siguiente: Optional["_Nodo[T]"] = None


class Bag(Generic[T]):
    """
    Bolsa genérica: add() en O(1), permite duplicados, no expone remoción
    (por definición del ADT). Se usa para colecciones donde no importa el
    orden ni se necesita quitar elementos (mecánicos, tipos de servicio,
    todas las órdenes registradas).
    """

    def __init__(self):
        self._primero: Optional[_Nodo[T]] = None
        self._tamano: int = 0

    def add(self, item: T) -> None:
        if item is None:
            raise ValueError("No se puede agregar un elemento None al Bag")
        nodo = _Nodo(item)
        nodo.siguiente = self._primero
        self._primero = nodo
        self._tamano += 1

    def contains(self, item: T) -> bool:
        return any(elemento == item for elemento in self)

    def esta_vacio(self) -> bool:
        return self._tamano == 0

    def size(self) -> int:
        return self._tamano

    def __iter__(self) -> Iterator[T]:
        actual = self._primero
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def __len__(self) -> int:
        return self._tamano


if __name__ == "__main__":
    # --- Caso típico ---
    b: Bag = Bag()
    assert b.esta_vacio() is True

    b.add("Motor")
    b.add("Frenos")
    b.add("Motor")  # duplicado: debe permitirse
    assert b.size() == 3
    assert b.contains("Frenos") is True
    assert b.contains("Llantas") is False

    # --- Caso de error: agregar None ---
    try:
        b.add(None)
        assert False, "Debió lanzar excepción al agregar None"
    except ValueError:
        pass

    # --- Caso borde: bag vacío ---
    vacio: Bag = Bag()
    assert vacio.contains("cualquier_cosa") is False
    assert list(vacio) == []

    # --- Iteración produce exactamente size() elementos ---
    contados = list(b)
    assert len(contados) == b.size() == 3

    print("Todas las pruebas de Bag pasaron correctamente.")
