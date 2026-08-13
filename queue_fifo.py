"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [completar]
- Nicolás Múnera - ID: [completar]

ADT Queue: cola FIFO genérica implementada con nodos enlazados.
"""

from typing import Generic, TypeVar, Optional, Iterator

T = TypeVar("T")


class _Nodo(Generic[T]):
    __slots__ = ("valor", "siguiente")

    def __init__(self, valor: T):
        self.valor = valor
        self.siguiente: Optional["_Nodo[T]"] = None


class Queue(Generic[T]):
    """
    Cola FIFO genérica. enqueue() agrega al final, dequeue() remueve y
    retorna el elemento más antiguo. Ambas operaciones son O(1) amortizado
    gracias a mantener referencias a primero y último nodo.
    """

    def __init__(self):
        self._primero: Optional[_Nodo[T]] = None
        self._ultimo: Optional[_Nodo[T]] = None
        self._tamano: int = 0

    def enqueue(self, item: T) -> None:
        if item is None:
            raise ValueError("No se puede encolar un elemento None")
        nodo = _Nodo(item)
        if self.esta_vacia():
            self._primero = nodo
        else:
            self._ultimo.siguiente = nodo
        self._ultimo = nodo
        self._tamano += 1

    def dequeue(self) -> T:
        if self.esta_vacia():
            raise IndexError("No se puede hacer dequeue: la cola está vacía")
        nodo = self._primero
        self._primero = nodo.siguiente
        if self._primero is None:
            self._ultimo = None
        self._tamano -= 1
        return nodo.valor

    def peek(self) -> T:
        if self.esta_vacia():
            raise IndexError("No se puede hacer peek: la cola está vacía")
        return self._primero.valor

    def esta_vacia(self) -> bool:
        return self._tamano == 0

    def size(self) -> int:
        return self._tamano

    def __iter__(self) -> Iterator[T]:
        """Recorre la cola en orden FIFO SIN remover elementos (útil para reportes)."""
        actual = self._primero
        while actual is not None:
            yield actual.valor
            actual = actual.siguiente

    def __len__(self) -> int:
        return self._tamano


if __name__ == "__main__":
    # --- Caso típico ---
    q: Queue = Queue()
    assert q.esta_vacia() is True

    q.enqueue("A")
    q.enqueue("B")
    q.enqueue("C")
    assert q.size() == 3

    assert q.dequeue() == "A"
    assert q.dequeue() == "B"
    assert q.size() == 1

    # --- Caso de error: dequeue/peek sobre cola vacía ---
    try:
        Queue().dequeue()
        assert False, "Debió lanzar excepción en dequeue de cola vacía"
    except IndexError:
        pass

    try:
        Queue().peek()
        assert False, "Debió lanzar excepción en peek de cola vacía"
    except IndexError:
        pass

    # --- Caso borde: iterador no debe vaciar la cola (solo lectura) ---
    q2: Queue = Queue()
    for i in [1, 2, 3, 4]:
        q2.enqueue(i)
    assert list(q2) == [1, 2, 3, 4]
    assert q2.size() == 4

    # --- Caso de error: encolar None ---
    try:
        q2.enqueue(None)
        assert False, "Debió lanzar excepción al encolar None"
    except ValueError:
        pass

    print("Todas las pruebas de Queue pasaron correctamente.")
