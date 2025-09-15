# app/modelos.py
from __future__ import annotations

class Usuario:
    contador = 0
    ROLES_VALIDOS = {"usuario", "admin", "invitado"}

    def __init__(self, nombre: str, email: str, rol: str = "usuario", activo: bool = True):
        self.nombre = nombre
        # Encapsulados
        self._email: str | None = None
        self.email = email  # dispara setter (valida y normaliza)
        self._rol: str | None = None
        self.rol = rol      # dispara setter (valida)
        self.activo = activo
        # Privado (name mangling)
        self.__password_hash: str | None = None

        Usuario.contador += 1

    # ------------------ Representación y básicos ------------------
    def presentarse(self) -> str:
        return f"Soy {self.nombre} ({self.email})"

    def activar(self) -> None: self.activo = True
    def desactivar(self) -> None: self.activo = False

    def __str__(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"{self.nombre} <{self.email}> ({self.rol}) [{estado}]"

    def __repr__(self) -> str:
        return (f"Usuario(nombre={self.nombre!r}, email={self.email!r}, "
                f"rol={self.rol!r}, activo={self.activo!r})")

    # ------------------ Email (propiedad) ------------------
    @property
    def email(self) -> str:
        return self._email or ""

    @email.setter
    def email(self, value: str) -> None:
        v = (value or "").strip().lower()
        if "@" not in v or v.startswith("@") or v.endswith("@"):
            raise ValueError(f"Email inválido: {value!r}")
        self._email = v

    # ------------------ Rol (propiedad) ------------------
    @property
    def rol(self) -> str:
        return self._rol or "usuario"

    @rol.setter
    def rol(self, value: str) -> None:
        v = (value or "").strip().lower()
        if v not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {value!r}. Válidos: {sorted(self.ROLES_VALIDOS)}")
        self._rol = v

    # ------------------ Password (privado simulado) ------------------
    def set_password(self, p: str) -> None:
        if not p or len(p) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        # Simulación: NO uses esto en producción
        self.__password_hash = f"hash::{p}"

    def check_password(self, p: str) -> bool:
        return self.__password_hash == f"hash::{p}"

    # ------------------ Constructores alternativos ------------------
    @classmethod
    def desde_dict(cls, datos: dict) -> "Usuario":
        """
        Espera claves: nombre, email, rol?, activo?
        """
        return cls(
            nombre=datos.get("nombre", ""),
            email=datos.get("email", ""),
            rol=datos.get("rol", "usuario"),
            activo=bool(datos.get("activo", True)),
        )