"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [completar]
- Nicolás Múnera - ID: [000280908]

Lista enlazada simple usada como historial: cada elemento nuevo se agrega
al frente, así que recorrerla produce del más reciente al más antiguo.
"""

from typing import Generic, TypeVar, Optional, Iterator

T = TypeVar("T")


class _Nodo(Generic[T]):
    __slots__ = ("valor", "siguiente")

    def __init__(self, valor: T):
        self.valor = valor
        self.siguiente: Optional["_Nodo[T]"] = None


class ListaEnlazada(Generic[T]):
    """
    Lista enlazada simple orientada a historial. agregar_al_frente() es
    O(1); recorrer todo el historial es O(n).
    """

    def __init__(self):
        self._cabeza: Optional[_Nodo[T]] = None
        self._tamano: int = 0

    def agregar_al_frente(self, item: T) -> None:
        if item is None:
            raise ValueError("No se puede agregar un elemento None al historial")
        nodo = _Nodo(item)
        nodo.siguiente = self._cabeza
        self._cabeza = nodo
        self._tamano += 1

    def esta_vacia(self) -> bool:
        return self._tamano == 0

    def size(self) -> int:
        return self._tamano

    def __iter__(self) -> Iterator[T]:
        """Recorre de la más reciente a la más antigua."""
        actual = self._cabeza
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def __len__(self) -> int:
        return self._tamano


if __name__ == "__main__":
    # --- Caso borde: historial vacío ---
    historial: ListaEnlazada = ListaEnlazada()
    assert historial.esta_vacia() is True
    assert list(historial) == []

    # --- Caso típico: orden de recorrido más reciente primero ---
    historial.agregar_al_frente("Orden1")
    historial.agregar_al_frente("Orden2")
    historial.agregar_al_frente("Orden3")

    assert list(historial) == ["Orden3", "Orden2", "Orden1"]
    assert historial.size() == 3

    # --- Caso de error: agregar None ---
    try:
        historial.agregar_al_frente(None)
        assert False, "Debió lanzar excepción al agregar None"
    except ValueError:
        pass

    print("Todas las pruebas de ListaEnlazada pasaron correctamente.")
