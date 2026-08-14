"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [000532192]
- Nicolás Múnera - ID: [000280908]

Programa de demostración end-to-end: crea órdenes, las asigna
automáticamente, las repara, las entrega y genera reportes usando
los iteradores implementados.
"""

from enums import EstadoOrden, TipoServicio
from taller_system import TallerSystem
from mecanico import Mecanico
from cliente import Cliente


def linea(titulo: str) -> None:
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def main() -> None:
    sistema = TallerSystem()

    linea("1. Configuración inicial")
    for tipo in [TipoServicio.MOTOR, TipoServicio.FRENOS, TipoServicio.ELECTRICIDAD]:
        sistema.agregarTipoServicio(tipo)
        print(f"Tipo de servicio habilitado: {tipo.value}")

    mecanicos = [
        Mecanico("Carlos Vélez", TipoServicio.MOTOR),
        Mecanico("Julia Ospina", TipoServicio.FRENOS),
        Mecanico("Pedro Salazar", TipoServicio.ELECTRICIDAD),
    ]
    for m in mecanicos:
        sistema.agregarMecanico(m)
        print(f"Mecánico registrado: {m}")

    linea("2. Creación de órdenes")
    cliente1 = Cliente("Santiago Zuluaga", "santi@gmail.com", "3011112222", "GVN211")
    cliente2 = Cliente("Cristiano Ronaldo", "marta@hotmail.com", "3013334444", "ABC695")

    orden1 = sistema.crearOrden("Motor con ruido extraño", TipoServicio.MOTOR, cliente1)
    orden2 = sistema.crearOrden("Frenos chillan", TipoServicio.FRENOS, cliente2)
    orden3 = sistema.crearOrden("Cortocircuito en luces", TipoServicio.ELECTRICIDAD, cliente1)
    for o in (orden1, orden2, orden3):
        print(f"Creada: {o} - Cliente: {o.get_cliente().get_nombre()}")

    linea("3. Asignación automática (FIFO)")
    for _ in range(3):
        asignada = sistema.asignarOrdenAutomatica()
        print(f"Asignada automáticamente: {asignada}")

    linea("4. Ciclo de reparación y entrega")
    for orden in (orden1, orden2, orden3):
        sistema.cambiarEstadoOrden(orden.get_id(), EstadoOrden.EN_REPARACION)
        sistema.finalizarOrden(orden.get_id())
        sistema.entregarOrden(orden.get_id())
        print(f"Ciclo completo para: {orden}")

    linea("5. Reportes con iteradores")
    print("Órdenes en estado Entregada (IteradorPorEstado):")
    for orden in sistema.obtenerOrdenesPorEstado(EstadoOrden.ENTREGADA):
        print(f"  - {orden}")

    print("\nHistorial, más reciente primero (ListaEnlazada):")
    for orden in sistema.iterar_historial():
        print(f"  - {orden}")

    linea("6. Estadísticas")
    for clave, valor in sistema.generarEstadisticas().items():
        print(f"{clave}: {valor}")


if __name__ == "__main__":
    main()
