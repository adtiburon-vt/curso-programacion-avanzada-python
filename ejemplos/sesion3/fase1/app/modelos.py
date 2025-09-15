from abc import ABC, abstractmethod

class BaseUsuario(ABC):
    @abstractmethod
    def permisos(self) -> list[str]:
        ...

class Usuario(BaseUsuario):
    contador = 0
    ROLES_VALIDOS = {"usuario", "admin", "invitado"}

    def __init__(self, nombre: str, email: str, rol: str = "usuario", activo: bool = True):
        self.nombre = nombre
        self._email = None
        self.email = email  # dispara setter
        self._rol = None
        self.rol = rol      # dispara setter
        self.activo = activo
        self.__password_hash = None
        Usuario.contador += 1

    def __str__(self):
        return f"{self.nombre} <{self.email}> ({self.rol})"

    def __repr__(self):
        return f"Usuario(nombre={self.nombre!r}, email={self.email!r}, rol={self.rol!r}, activo={self.activo!r})"

    # Encapsulación email
    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if "@" not in (value or ""):
            raise ValueError("Email inválido")
        self._email = value.strip().lower()

    # Encapsulación rol
    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, value: str):
        v = (value or "").lower().strip()
        if v not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {value!r}")
        self._rol = v

    # Password simulada
    def set_password(self, p: str):
        self.__password_hash = f"hash::{p}"

    def check_password(self, p: str) -> bool:
        return self.__password_hash == f"hash::{p}"

    def presentarse(self) -> str:
        return f"Soy {self.nombre} ({self.email})"

    def activar(self): self.activo = True
    def desactivar(self): self.activo = False

    @classmethod
    def desde_dict(cls, datos: dict) -> "Usuario":
        return cls(
            nombre=datos.get("nombre",""),
            email=datos.get("email",""),
            rol=datos.get("rol","usuario"),
            activo=datos.get("activo", True),
        )

    def permisos(self) -> list[str]:
        # Por defecto, permisos básicos
        return ["ver"]

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

    def __str__(self):
        return f"[INVITADO] {super().__str__()}"

def tiene_permiso(usuario: Usuario, permiso: str) -> bool:
    return permiso in usuario.permisos()