# main.py
from app.modelos import Usuario

if __name__ == "__main__":
    # Caso feliz
    u = Usuario("Ana", "ANA@Test.com", rol="admin")
    u.set_password("secreta!")
    print(u.presentarse(), u.rol, u.check_password("secreta!"))

    # Email inválido
    try:
        u.email = "sin-arroba"
    except ValueError as e:
        print("Email inválido OK:", e)

    # Rol inválido
    try:
        u.rol = "superuser"
    except ValueError as e:
        print("Rol inválido OK:", e)

    # desde_dict
    datos = {"nombre": "Luis", "email": "luis@test.com", "rol": "invitado", "activo": False}
    u2 = Usuario.desde_dict(datos)
    print(repr(u2))

    # Password mínima
    try:
        u2.set_password("123")
    except ValueError as e:
        print("Password corta OK:", e)



    


# app/modelos.py
from __future__ import annotations
from abc import ABC, abstractmethod

# --- Base abstracta ---
class BaseUsuario(ABC):
    @abstractmethod
    def permisos(self) -> list[str]:
        """Lista de permisos concedidos al usuario."""
        ...

    def tiene_permiso(self, permiso: str) -> bool:
        return permiso in self.permisos()

# --- Usuario (de Fase 2) HEREDA de BaseUsuario ---
class Usuario(BaseUsuario):
    contador = 0
    ROLES_VALIDOS = {"usuario", "admin", "invitado"}

    def __init__(self, nombre: str, email: str, rol: str = "usuario", activo: bool = True):
        self.nombre = nombre
        self._email: str | None = None
        self.email = email
        self._rol: str | None = None
        self.rol = rol
        self.activo = activo
        self.__password_hash: str | None = None
        Usuario.contador += 1

    # Representación
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

    # Email
    @property
    def email(self) -> str:
        return self._email or ""

    @email.setter
    def email(self, value: str) -> None:
        v = (value or "").strip().lower()
        if "@" not in v or v.startswith("@") or v.endswith("@"):
            raise ValueError(f"Email inválido: {value!r}")
        self._email = v

    # Rol
    @property
    def rol(self) -> str:
        return self._rol or "usuario"

    @rol.setter
    def rol(self, value: str) -> None:
        v = (value or "").strip().lower()
        if v not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {value!r}. Válidos: {sorted(self.ROLES_VALIDOS)}")
        self._rol = v

    # Password (demo)
    def set_password(self, p: str) -> None:
        if not p or len(p) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        self.__password_hash = f"hash::{p}"

    def check_password(self, p: str) -> bool:
        return self.__password_hash == f"hash::{p}"

    @classmethod
    def desde_dict(cls, datos: dict) -> "Usuario":  
        return cls(
            nombre=datos.get("nombre", ""),
            email=datos.get("email", ""),
            rol=datos.get("rol", "usuario"), 
            activo=bool(datos.get("activo", True)),
        )

    # Permisos por defecto del rol "usuario"
    def permisos(self) -> list[str]:
        return ["ver"]

# --- Subclases por rol ---
class Admin(Usuario):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, rol="admin", activo=activo)

    def permisos(self) -> list[str]:
        return ["ver", "crear", "editar", "borrar"]

class Invitado(Usuario):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, rol="invitado", activo=activo)

    def permisos(self) -> list[str]:
        return ["ver"]

    def __str__(self) -> str:
        return f"[INVITADO] {super().__str__()}"
    



Usuario.desde_dict()
Admin.desde_dict()
Invitado.desde_dict()