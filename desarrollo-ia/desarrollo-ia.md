# Documento de Ingeniería con IA — Taller 01
## Sistema de Gestión de Taller de Reparación (AutoFix Ltda.)

**Curso:** Estructuras de Datos y Algoritmos — 2026-20
**Integrantes:**
- Santiago Zuluaga — ID: [completar]
- Nicolás Múnera — ID: [completar]

**Lenguaje:** Python 3.14.3 (a confirmar)

**Estado del documento:** 🟡 En construcción — Parte 2 (PRD) completa. Partes 1, 3, 4, 5 y 6 pendientes de completar durante el desarrollo, siguiendo la metodología del curso.

---

# COMPONENTE 1: Queue (cola FIFO genérica)

## 1. Entender y descomponer (sin IA)
> **TODO (equipo, sin IA):** reescribir el problema con sus propias palabras, identificar subproblemas y plantear la hipótesis de solución (qué estructura, qué algoritmo, por qué).

## 2. PRD

### Requerimientos
- **Entradas:** elementos genéricos de tipo `T` (en este sistema, principalmente objetos `OrdenReparacion`, pero la estructura debe ser reutilizable para cualquier tipo).
- **Salidas:** elementos de tipo `T` (al hacer `dequeue()` o `peek()`); booleano en `is_empty()`; entero en `size()`.

### Contrato
- **Precondiciones:**
  - `dequeue()`: la cola no debe estar vacía.
  - `peek()`: la cola no debe estar vacía.
  - `enqueue(item)`: `item` no debe ser `None`.
- **Postcondiciones:**
  - `enqueue(item)`: el tamaño de la cola aumenta en 1; `item` queda en la posición final (última en salir).
  - `dequeue()`: retorna y remueve el elemento más antiguo (el primero insertado que aún no ha salido); el tamaño disminuye en 1.
  - `peek()`: retorna el elemento más antiguo sin removerlo; el tamaño no cambia.
  - `is_empty()`: retorna `True` si y solo si `size() == 0`.
- **Invariantes:**
  - El orden relativo de inserción se preserva siempre (FIFO estricto): si A se encoló antes que B, A sale antes que B.
  - `size()` nunca es negativo.

### Restricciones de implementación
- **Complejidad temporal esperada:** O(1) amortizado tanto para `enqueue` como para `dequeue`.
- **Complejidad espacial esperada:** O(n), n = número de elementos actuales.
- **Buenas prácticas / patrones exigidos:** implementación basada en nodos enlazados (referencia a `head`/primero y `tail`/último), siguiendo el estilo visto en clase (estilo algs4/Sedgewick); usar tipado genérico (`Generic[T]` en Python) para que sea reutilizable.
- **Prohibiciones:** no usar `list.pop(0)` de Python como mecanismo de dequeue (es O(n), viola la complejidad esperada). El taller permite reusar la versión de clase o de biblioteca estándar ajustada a convenciones — si se opta por `collections.deque`, debe encapsularse detrás de la propia API del ADT (`enqueue`/`dequeue`), sin exponer métodos nativos de `deque` directamente.

### Criterios de aceptación (casos de prueba)
- **Caso típico:** `enqueue(A)`, `enqueue(B)`, `enqueue(C)` → `dequeue()` devuelve `A`, luego `B`, luego `C`, en ese orden exacto.
- **Casos borde:** cola con un solo elemento (enqueue + dequeue devuelve ese mismo elemento y deja la cola vacía); `is_empty()` correcto antes y después de operaciones; muchos elementos (orden se mantiene con N grande).
- **Casos de error:** `dequeue()` o `peek()` sobre cola vacía → debe lanzar una excepción descriptiva (no debe retornar `None` silenciosamente, para evitar errores encubiertos aguas abajo).

## 3. Prompt(s) utilizado(s)
> **TODO:** pegar aquí el/los prompt(s) textuales usados, herramienta y fecha (o indicar "no se usó IA" si aplica).

## 4. Registro de validación crítica
> **TODO:** casos de aceptación ejecutados (resultado), casos borde probados (resultado), complejidad deducida por el equipo (no la que afirme la IA), verificación de pre/postcondiciones e invariantes.

## 5. Problemas encontrados y correcciones
> **TODO**

## 6. Reflexión final (prueba de propiedad)
> **TODO**

---

# COMPONENTE 2: List enlazada (historial de reparaciones)

## 1. Entender y descomponer (sin IA)
> **TODO (equipo, sin IA)**

## 2. PRD

### Requerimientos
- **Entradas:** objetos `OrdenReparacion` que acaban de finalizar (pasar a estado "Reparada").
- **Salidas:** un iterador que recorre las órdenes del historial de la más reciente a la más antigua; entero en `size()`.

### Contrato
- **Precondiciones:** `agregar_al_frente(orden)` requiere que `orden` no sea `None` y que su estado sea "Reparada" (o posterior) en el momento de agregarse.
- **Postcondiciones:** `agregar_al_frente(orden)` inserta `orden` como nuevo primer nodo (head); el nodo anterior queda enlazado inmediatamente después; `size()` aumenta en 1.
- **Invariantes:**
  - El `head` siempre referencia al elemento agregado más recientemente (la última reparación finalizada).
  - No existen ciclos en la lista.
  - Recorrer la lista siempre produce las órdenes en orden estrictamente descendente de `fechaFinalizacion`.

### Restricciones de implementación
- **Complejidad temporal esperada:** O(1) para inserción al frente; O(n) para recorrido completo.
- **Complejidad espacial esperada:** O(n).
- **Buenas prácticas / patrones exigidos:** nodo propio con referencia a `next`; iterador propio (`__iter__`/`__next__`) que recorra desde `head` hacia el final.
- **Prohibiciones:** no usar `list.insert(0, x)` de Python como "lista enlazada" — no demuestra el concepto pedagógico que exige el taller (nodos + referencias explícitas).

### Criterios de aceptación (casos de prueba)
- **Caso típico:** agregar orden1, luego orden2, luego orden3 (en ese orden temporal) → iterar el historial retorna orden3, orden2, orden1.
- **Casos borde:** historial vacío (iterar no falla, produce 0 elementos); historial con un solo elemento.
- **Casos de error:** intentar agregar `None` → excepción; intentar agregar una orden que no está en estado válido para historial → excepción.

## 3. Prompt(s) utilizado(s)
> **TODO**

## 4. Registro de validación crítica
> **TODO**

## 5. Problemas encontrados y correcciones
> **TODO**

## 6. Reflexión final (prueba de propiedad)
> **TODO**

---

# COMPONENTE 3: Bag

## 1. Entender y descomponer (sin IA)
> **TODO (equipo, sin IA)**

## 2. PRD

### Requerimientos
- **Entradas:** elementos de tipo `T` — en este sistema se usa para: todas las órdenes registradas, los mecánicos del taller, y los tipos de servicio válidos.
- **Salidas:** un iterador sobre los elementos (orden no garantizado); entero en `size()`; booleano en `contains(item)` (necesario para validar tipos de servicio).

### Contrato
- **Precondiciones:** `add(item)` requiere que `item` no sea `None`.
- **Postcondiciones:** `add(item)` incrementa `size()` en 1 y hace que `item` sea alcanzable mediante iteración; se permiten duplicados (a diferencia de un `Set`).
- **Invariantes:**
  - `size()` solo puede crecer o mantenerse igual — nunca decrece (el Bag, por definición del ADT, no soporta remoción).
  - El número de elementos producidos al iterar siempre es igual a `size()`.

### Restricciones de implementación
- **Complejidad temporal esperada:** O(1) amortizado para `add`; O(1) para `contains` si se usa una estructura auxiliar de apoyo (opcional) u O(n) si se recorre linealmente — aceptable dado el tamaño del problema.
- **Complejidad espacial esperada:** O(n).
- **Buenas prácticas / patrones exigidos:** implementación basada en lista enlazada (consistente con el estilo del curso) o envoltura de `list` de Python que **no** exponga métodos de remoción (`pop`, `remove`) para respetar el contrato del ADT.
- **Prohibiciones:** no usar `set` de Python (pierde duplicados y no es el ADT pedido); no exponer ninguna operación de remoción pública.

### Criterios de aceptación (casos de prueba)
- **Caso típico:** agregar 3 tipos de servicio distintos → iterar los devuelve los 3 (sin garantía de orden).
- **Casos borde:** bag vacío; agregar el mismo tipo de servicio dos veces (debe permitirse, `size()` refleja ambos).
- **Casos de error:** `add(None)` → excepción; `contains()` sobre bag vacío → `False`, no excepción.

## 3. Prompt(s) utilizado(s)
> **TODO**

## 4. Registro de validación crítica
> **TODO**

## 5. Problemas encontrados y correcciones
> **TODO**

## 6. Reflexión final (prueba de propiedad)
> **TODO**

---

# COMPONENTE 4: Algoritmo `asignarOrdenAutomatica()`

## 1. Entender y descomponer (sin IA)
> **TODO (equipo, sin IA)**

## 2. PRD

### Requerimientos
- **Entradas:** ninguna explícita — el método opera sobre el estado interno del `TallerSystem` (`ordenesPendientes: Queue[OrdenReparacion]`, `mecanicos: Bag[Mecanico]`).
- **Salidas:** la orden asignada y el mecánico asignado (o una señal clara de que no fue posible asignar, p. ej. `None` o una excepción controlada, a decidir en la implementación).

### Contrato
- **Precondiciones:** el sistema debe tener al menos un mecánico registrado (si no hay ninguno, no hay nada que asignar — comportamiento definido, no error). No se exige que `ordenesPendientes` tenga elementos: si está vacía, simplemente no hay trabajo por hacer.
- **Postcondiciones:**
  - Si existe una orden pendiente **y** un mecánico disponible (`disponible == True`) con la especialidad requerida por esa orden: la orden se remueve de `ordenesPendientes`, su `estado` cambia a `Asignada`, se liga `mecanicoAsignado`; el mecánico pasa a `disponible = False` y `ordenAsignada = esa orden`.
  - Si no existe mecánico disponible con la especialidad requerida: la orden **permanece intacta** al frente de `ordenesPendientes` (no se pierde ni se remueve).
- **Invariantes:**
  - Ninguna orden queda en estado `Asignada` sin un `mecanicoAsignado` válido.
  - Ningún mecánico queda con más de una orden asignada simultáneamente.
  - El orden FIFO de las demás órdenes en la cola no se altera por un intento de asignación fallido.

### Restricciones de implementación
- **Complejidad temporal esperada:** O(1) para el `dequeue` propuesto + O(m) para buscar un mecánico disponible con la especialidad requerida, donde m = número de mecánicos registrados (aceptable para el tamaño del taller; no se exige optimizar con un índice por especialidad, aunque es una mejora válida a mencionar).
- **Complejidad espacial esperada:** O(1) adicional (no se crean estructuras nuevas proporcionales a n).
- **Buenas prácticas / patrones exigidos:** separar claramente "buscar mecánico candidato" (función auxiliar de solo lectura) de "efectuar la asignación" (mutación de estado) — principio de responsabilidad única; no mutar nada hasta confirmar que existe un mecánico disponible.
- **Prohibiciones:** no remover la orden de la cola antes de confirmar que hay mecánico disponible (si no se encuentra, la orden no debe desaparecer de `ordenesPendientes`).

### Criterios de aceptación (casos de prueba)
- **Caso típico:** una orden tipo "Motor" en cola, un mecánico de especialidad "Motor" disponible → se asigna correctamente; orden pasa a `Asignada`; mecánico queda `disponible = False`.
- **Casos borde:** cola vacía (no debe lanzar error, no debe hacer nada); varios mecánicos con la misma especialidad pero solo uno disponible → debe elegirse el disponible, no uno ocupado; ningún mecánico tiene la especialidad requerida → la orden permanece en cola para el siguiente intento.
- **Casos de error:** invocar el método con el sistema recién creado (sin mecánicos registrados) → debe manejarse sin excepción no controlada (comportamiento definido: no asigna nada).

## 3. Prompt(s) utilizado(s)
> **TODO**

## 4. Registro de validación crítica
> **TODO**

## 5. Problemas encontrados y correcciones
> **TODO**

## 6. Reflexión final (prueba de propiedad)
> **TODO**

---

# CONTRATOS DE LOS ADTs (Precondiciones, Postcondiciones, Invariantes) + Criterios de Aceptación

## ADT: OrdenReparacion

**Contrato:**
- *Precondiciones:* el constructor requiere `descripcion` no vacía, `tipoServicio` válido (registrado en el sistema), `cliente` no `None`.
- *Postcondiciones:* al construirse, `estado = Recibida`, `fechaIngreso = ahora`, `fechaFinalizacion = None`, `mecanicoAsignado = None`, `id` autogenerado y único.
- *Invariantes:*
  - `id` es inmutable una vez creado.
  - No puede pasar a `Reparada` sin tener `mecanicoAsignado`.
  - Solo puede pasar a `Entregada` si el estado actual es `Reparada`.
  - `fechaFinalizacion` (cuando existe) siempre es posterior o igual a `fechaIngreso`.

**Criterios de aceptación:**
- Crear una orden válida → estado inicial correcto, id único generado.
- Intentar `finalizarReparacion()` sin mecánico asignado → excepción.
- Intentar `entregar()` sin estar en estado `Reparada` → excepción.
- Intentar `cambiarEstado()` con una transición inválida (ej. `Recibida → Reparada` directo, saltándose `Asignada`/`EnReparacion`) → excepción.
- `tiempoEnTaller()` calcula correctamente usando `fechaFinalizacion` si existe, o el tiempo transcurrido hasta el momento si aún está abierta.

## ADT: Cliente

**Contrato:**
- *Precondiciones:* `nombre` no vacío; `email` con formato válido.
- *Postcondiciones:* cliente creado con `id` único; todos los atributos quedan accesibles vía getters.
- *Invariantes:* `id` inmutable; el email mantiene formato válido durante toda la vida del objeto (validado también en el setter, si existe).

**Criterios de aceptación:**
- Crear cliente con datos válidos → éxito.
- Crear cliente con email mal formado (ej. sin `@`) → excepción.
- Crear cliente con `nombre` vacío → excepción.

## ADT: Mecánico

**Contrato:**
- *Precondiciones:* `nombre` y `especialidad` no vacíos al construir.
- *Postcondiciones:* mecánico creado con `disponible = True`, `ordenAsignada = None`. `asignarOrden(orden)` deja `disponible = False` y liga la orden. `completarOrden()` deja `disponible = True` y `ordenAsignada = None`.
- *Invariantes:* nunca tiene más de una orden asignada simultáneamente.

**Criterios de aceptación:**
- Asignar una orden a un mecánico disponible → éxito, `estaDisponible()` retorna `False`.
- Intentar asignar una segunda orden sin liberar la primera → excepción.
- `completarOrden()` sobre un mecánico sin orden asignada → excepción (o no-op documentado, a decidir).
- `marcarDisponibilidad()` cambia el estado correctamente sin afectar la orden asignada existente.

## ADT: TallerSystem

**Contrato:**
- *Precondiciones:* `crearOrden()` exige que `tipoServicio` exista en el `Bag` de tipos válidos.
- *Postcondiciones:* `crearOrden()` agrega la orden a `todasLasOrdenes` y a `ordenesPendientes`. `finalizarOrden()` mueve la orden al `historial` (al frente) y libera al mecánico correspondiente.
- *Invariantes:*
  - Cada orden tiene un `id` único en todo el sistema.
  - `ordenesPendientes` siempre refleja el orden real de llegada (FIFO).
  - Solo existen órdenes con tipos de servicio previamente registrados como válidos.

**Criterios de aceptación:**
- `crearOrden()` con tipo de servicio inválido → excepción.
- Flujo completo: crear → asignar automáticamente → cambiar a `EnReparacion` → `finalizarOrden()` → `entregarOrden()` funciona de punta a punta sin errores.
- `obtenerOrdenesPorEstado(estado)` retorna exactamente las órdenes que están en ese estado, ni más ni menos.
- `obtenerOrdenesPorTipo(tipo)` filtra correctamente.
- `cambiarEstadoOrden()` con un `ordenId` inexistente → excepción.

---

*Fin de la Parte 2 (PRD). Las Partes 1, 3, 4, 5 y 6 se completarán a medida que se avance en la implementación de cada componente, según la metodología del curso.*
