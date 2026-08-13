# Taller Práctico 01 — Sistema de Gestión de Taller de Reparación (AutoFix Ltda.)

## 1. Información del Equipo

| Integrante | ID |
|---         |---|
| Santiago Zuluaga | [000532192] |
| Nicolás Múnera | [completar] |

**Lenguaje y versión:** Python 3.14.3 
**Curso:** Estructuras de Datos y Algoritmos — 2026-20 — Facultad TIC, UPB.

## 2. Descripción del Proyecto

El sistema le permite a AutoFix Ltda. reemplazar el registro en papel de sus reparaciones por una gestión ordenada de **órdenes de reparación**. Permite:

- Registrar clientes y crear órdenes asociadas a un tipo de servicio válido (Motor, Frenos, Electricidad, Carrocería, Llantas, Suspensión).
- Encolar las órdenes en **estricto orden FIFO** de llegada.
- Asignarlas automáticamente al primer mecánico disponible que tenga la especialidad requerida (o manualmente a un mecánico específico).
- Llevar cada orden a través de su ciclo de vida: `Recibida → Asignada → EnReparacion → Reparada → Entregada`, validando que las transiciones sean coherentes (por ejemplo, no se puede pasar de `Recibida` directo a `Reparada`).
- Conservar un **historial** de reparaciones finalizadas, con la más reciente primero.
- Generar reportes filtrando órdenes por estado o por tipo de servicio, usando iteradores personalizados.

## 3. Estructura del Proyecto

```
taller01-codigo/
├── enums.py                # EstadoOrden, TipoServicio y tabla de transiciones válidas
├── queue_fifo.py            # ADT Queue (cola FIFO genérica, nodos enlazados)
├── bag.py                   # ADT Bag (bolsa genérica, permite duplicados)
├── lista_enlazada.py        # Lista enlazada usada como historial (más reciente primero)
├── cliente.py                # ADT Cliente
├── mecanico.py               # ADT Mecanico
├── orden_reparacion.py       # ADT OrdenReparacion (máquina de estados)
├── iterador_por_estado.py    # Iterador personalizado (patrón __iter__/__next__ explícito)
├── taller_system.py          # ADT TallerSystem: coordinador central del sistema
├── main_demo.py               # Programa de demostración end-to-end
├── README.md
└── desarrollo-ia.md           # Documentación de metodología de IA (PRD, prompts, validación)
```

**Qué contiene cada archivo:**

| Archivo | Contenido |
|---|---|
| `enums.py` | `EstadoOrden`, `TipoServicio`, y `TRANSICIONES_VALIDAS` (qué estado puede pasar a cuál). |
| `queue_fifo.py` | `Queue`: `enqueue`, `dequeue`, `peek`, `esta_vacia`, `size`, iterador de solo lectura. |
| `bag.py` | `Bag`: `add`, `contains`, `esta_vacio`, `size`, iterador. |
| `lista_enlazada.py` | `ListaEnlazada`: `agregar_al_frente`, `size`, iterador (más reciente → más antiguo). |
| `cliente.py` | `Cliente` con validación de nombre y formato de email. |
| `mecanico.py` | `Mecanico`: `asignarOrden`, `completarOrden`, `estaDisponible`, invariante de una sola orden. |
| `orden_reparacion.py` | `OrdenReparacion`: ciclo de vida completo con validación de transiciones. |
| `iterador_por_estado.py` | `IteradorPorEstado`, iterador explícito (clase con `__iter__`/`__next__`) para filtrar por estado. |
| `taller_system.py` | `TallerSystem`: integra Queue, Bag, ListaEnlazada y los ADTs de dominio; contiene `asignarOrdenAutomatica()`. |
| `main_demo.py` | Ejecuta un escenario completo en consola: crear → asignar → reparar → entregar → reportes. |

## 4. Instrucciones de Compilación/Ejecución

No requiere compilación (Python es interpretado). Tampoco requiere librerías externas — solo la biblioteca estándar.

**Ejecutar el programa principal (demo end-to-end):**
```bash
python3 main_demo.py
```

**Ejecutar las pruebas (cada archivo tiene su propio `main` con asserts):**
```bash
python3 enums.py
python3 queue_fifo.py
python3 bag.py
python3 lista_enlazada.py
python3 cliente.py
python3 mecanico.py
python3 orden_reparacion.py
python3 iterador_por_estado.py
python3 taller_system.py
```

O para correr todas de una vez:
```bash
for f in enums.py queue_fifo.py bag.py lista_enlazada.py cliente.py mecanico.py orden_reparacion.py iterador_por_estado.py taller_system.py; do
    python3 "$f"
done
```

Cada módulo imprime `Todas las pruebas de <Componente> pasaron correctamente.` si todos sus asserts se cumplen. En total el proyecto tiene 78 asserts distribuidos en las 9 categorías exigidas (creación, getters/setters, cambios de estado, asignación, validaciones que fallan, iteradores y sistema completo).

## 5. Decisiones de Diseño

- **Estructuras propias, no de la librería estándar:** `Queue`, `Bag` y `ListaEnlazada` se implementaron con nodos enlazados propios en vez de `collections.deque` o `list`, para demostrar explícitamente el manejo de referencias que exige el taller y garantizar las complejidades esperadas (O(1) amortizado en las operaciones principales).

- **Bag sin remoción:** se respetó estrictamente el contrato del ADT Bag (no expone ningún método para quitar elementos), ya que el sistema nunca necesita remover mecánicos ni tipos de servicio una vez registrados.

- **Validación de transiciones vía tabla (`TRANSICIONES_VALIDAS`)** en lugar de una cadena de `if/elif`: centraliza la regla de negocio en un solo lugar, es más fácil de auditar y evita que se cuelen transiciones inválidas si se agrega un nuevo estado en el futuro.

- **`asignarOrdenAutomatica()` no muta estado hasta confirmar éxito:** primero se hace `peek()` (sin remover) y se busca mecánico candidato; solo si existe uno disponible se hace `dequeue()` y se asigna. Esto evita dejar el sistema en un estado inconsistente si no hay mecánico disponible — la orden permanece intacta en la cola para el siguiente intento.

- **Dos iteradores personalizados con estilos distintos a propósito:** `IteradorPorEstado` implementa el patrón Iterator de forma explícita (clase con `__iter__`/`__next__` y `StopIteration` manual) para demostrar el mecanismo subyacente; el historial usa un generador (`yield`) en `ListaEnlazada.__iter__`, que es la forma idiomática y más concisa en Python. Ambos cumplen el mismo contrato de iterador.

- **IDs autogenerados con `itertools.count`:** en `Cliente`, `Mecanico` y `OrdenReparacion`, en lugar de un contador manual, para garantizar unicidad sin depender de estado externo.

- **Excepciones estándar de Python (`ValueError`, `IndexError`, `StopIteration`)** con mensajes descriptivos, en vez de clases de excepción personalizadas — el taller no lo exige y mantiene el código más simple.

- **`asignarOrdenManual()` implementado** aunque el taller lo marca como opcional, porque era una extensión natural del diseño (reutiliza `_remover_de_pendientes` para sacar la orden de la cola si estaba ahí).

- **No se implementó "Reingresar Orden"**, ya que el taller indica explícitamente que no es necesario.
