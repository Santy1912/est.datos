"""
Taller Práctico 01 - Sistema de Gestión de Taller de Reparación
Estructuras de Datos y Algoritmos - 2026-20

Integrantes:
- Santiago Zuluaga - ID: [completar]
- Nicolás Múnera - ID: [000280908]

ADT Cliente: representa al dueño del vehículo que ingresa al taller.
"""

import itertools
import re

_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Cliente:
    """
    Representa un cliente. El id es único e inmutable, autogenerado por
    un contador de clase. El email se valida en construcción y en el setter.
    """

    _contador_id = itertools.count(1)

    def __init__(self, nombre: str, email: str, telefono: str, placa_vehiculo: str):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacío")
        if not _EMAIL_REGEX.match(email or ""):
            raise ValueError(f"Email inválido: {email!r}")

        self._id = next(Cliente._contador_id)
        self._nombre = nombre.strip()
        self._email = email
        self._telefono = telefono
        self._placa_vehiculo = placa_vehiculo

    # ---------- Getters ----------
    def get_id(self) -> int:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def get_email(self) -> str:
        return self._email

    def get_telefono(self) -> str:
        return self._telefono

    def get_placa_vehiculo(self) -> str:
        return self._placa_vehiculo

    # ---------- Setters (con validación donde aplica) ----------
    def set_email(self, nuevo_email: str) -> None:
        if not _EMAIL_REGEX.match(nuevo_email or ""):
            raise ValueError(f"Email inválido: {nuevo_email!r}")
        self._email = nuevo_email

    def set_telefono(self, nuevo_telefono: str) -> None:
        self._telefono = nuevo_telefono

    def __str__(self) -> str:
        return f"Cliente[{self._id}] {self._nombre} - {self._email} - Placa: {self._placa_vehiculo}"


if __name__ == "__main__":
    # --- Caso típico ---
    c1 = Cliente("Ana Pérez", "ana@example.com", "3001234567", "ABC123")
    assert c1.get_nombre() == "Ana Pérez"
    assert c1.get_placa_vehiculo() == "ABC123"

    # --- IDs únicos ---
    c2 = Cliente("Luis Gómez", "luis@example.com", "3007654321", "XYZ987")
    assert c1.get_id() != c2.get_id()

    # --- Casos de error: nombre vacío y email inválido ---
    try:
        Cliente("", "correo@valido.com", "300", "AAA111")
        assert False, "Debió lanzar excepción por nombre vacío"
    except ValueError:
        pass

    try:
        Cliente("Carlos Ruiz", "correo-invalido", "300", "BBB222")
        assert False, "Debió lanzar excepción por email inválido"
    except ValueError:
        pass

    # --- Setter válido y setter inválido ---
    c1.set_email("ana.nueva@example.com")
    assert c1.get_email() == "ana.nueva@example.com"
    try:
        c1.set_email("no-es-email")
        assert False, "Debió lanzar excepción por email inválido en el setter"
    except ValueError:
        pass

    print("Todas las pruebas de Cliente pasaron correctamente.")
