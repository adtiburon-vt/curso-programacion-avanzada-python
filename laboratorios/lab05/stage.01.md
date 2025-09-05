# 🔹 Fase 1: Paquetización y separación por módulos

### 🎯 Objetivo

Crear el paquete `app/` y repartir el sistema de usuarios en **módulos**: `modelos.py`, `repositorio.py`, `utils.py`. Dejar listo `__init__.py` para exponer la API básica.

---

## 🧱 Scaffold (estructura inicial)

```
lab5_modular_cli/
├─ app/
│  ├─ __init__.py
│  ├─ modelos.py
│  ├─ repositorio.py
│  └─ utils.py
└─ main.py   # se usará en la Fase 2
```

---

## 🧭 Pasos

### 1) `app/utils.py` — utilidades comunes

```python
# app/utils.py
def validar_email(email: str) -> bool:
    email = (email or "").strip().lower()
    return (
        "@" in email and "." in email and
        not email.startswith("@") and not email.endswith("@")
    )
```

### 2) `app/modelos.py` — clases del dominio

> Pega aquí tus clases de Labs 3–4 (Usuario, Admin, Invitado, Moderador, mixins).
> Asegúrate de usar `validar_email` en el setter de `email`.

```python
# app/modelos.py
from __future__ import annotations
from abc import ABC, abstractmethod
from .utils import validar_email

class BaseUsuario(ABC):
    @abstractmethod
    def permisos(self) -> list[str]: ...
    def tiene_permiso(self, p: str) -> bool: return p in self.permisos()

class Usuario(BaseUsuario):
    contador = 0
    ROLES_VALIDOS = {"usuario", "admin", "invitado", "moderador"}

    def __init__(self, nombre: str, email: str, rol: str = "usuario", activo: bool = True):
        self.nombre = nombre
        self._email: str | None = None
        self.email = email       # setter valida
        self._rol: str | None = None
        self.rol = rol           # setter valida
        self.activo = activo
        self.__password_hash: str | None = None
        Usuario.contador += 1

    def presentarse(self) -> str:
        return f"Soy {self.nombre} ({self.email})"

    def activar(self): self.activo = True
    def desactivar(self): self.activo = False

    def __str__(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"{self.nombre} <{self.email}> ({self.rol}) [{estado}]"

    @property
    def email(self) -> str: return self._email or ""
    @email.setter
    def email(self, value: str):
        if not validar_email(value):
            raise ValueError(f"Email inválido: {value!r}")
        self._email = value.strip().lower()

    @property
    def rol(self) -> str: return self._rol or "usuario"
    @rol.setter
    def rol(self, value: str):
        v = (value or "").strip().lower()
        if v not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {value!r}")
        self._rol = v

    def set_password(self, p: str):
        if not p or len(p) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        self.__password_hash = f"hash::{p}"
    def check_password(self, p: str) -> bool:
        return self.__password_hash == f"hash::{p}"

    @classmethod
    def desde_dict(cls, d: dict) -> "Usuario":
        return cls(d.get("nombre",""), d.get("email",""), d.get("rol","usuario"), bool(d.get("activo", True)))

    def permisos(self) -> list[str]:
        return ["ver"]

class Admin(Usuario):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, rol="admin", activo=activo)
    def permisos(self) -> list[str]:
        return ["ver", "crear", "editar", "borrar"]
    def presentarse(self) -> str:
        return f"[ADMIN] {super().presentarse()}"

class Invitado(Usuario):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, rol="invitado", activo=activo)
    def permisos(self) -> list[str]:
        return ["ver"]
    def __str__(self) -> str:
        return f"[INVITADO] {super().__str__()}"

class Moderador(Usuario):
    def __init__(self, nombre: str, email: str, nivel: int = 1, activo: bool = True):
        super().__init__(nombre, email, rol="moderador", activo=activo)
        if not isinstance(nivel, int) or nivel < 1:
            raise ValueError("nivel debe ser int >= 1")
        self.nivel = nivel
    def permisos(self) -> list[str]:
        base = ["ver", "editar"]
        if self.nivel >= 2: base.append("borrar")
        return base
    def __str__(self) -> str:
        return f"[MODERADOR-N{self.nivel}] {super().__str__()}"
```

### 3) `app/repositorio.py` — almacenamiento en memoria

```python
# app/repositorio.py
from typing import Callable, Optional
from .modelos import Usuario

class RepositorioUsuarios:
    def __init__(self):
        self._por_email: dict[str, Usuario] = {}

    def agregar(self, u: Usuario):
        k = u.email
        if k in self._por_email:
            raise ValueError(f"Ya existe usuario con email {k}")
        self._por_email[k] = u

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        return self._por_email.get((email or "").strip().lower())

    def listar_activos(self) -> list[Usuario]:
        return [u for u in self._por_email.values() if u.activo]

    def eliminar(self, email: str):
        self._por_email.pop((email or "").strip().lower(), None)

    def buscar(self, predicado: Callable[[Usuario], bool]) -> list[Usuario]:
        return [u for u in self._por_email.values() if predicado(u)]
```

### 4) `app/__init__.py` — API del paquete

```python
# app/__init__.py
from .modelos import Usuario, Admin, Invitado, Moderador
from .repositorio import RepositorioUsuarios

__all__ = ["Usuario", "Admin", "Invitado", "Moderador", "RepositorioUsuarios"]
```

---

## ✅ Validación rápida

Desde la carpeta raíz:

```python
# prueba rápida interactiva
>>> from app import Usuario, Admin, RepositorioUsuarios
>>> u = Usuario("Ana", "ana@test.com")
>>> a = Admin("Root", "root@corp.com")
>>> repo = RepositorioUsuarios()
>>> repo.agregar(u); repo.agregar(a)
>>> [str(x) for x in repo.listar_activos()]
['Ana <ana@test.com> (usuario) [activo]', '[ADMIN] Soy Root (root@corp.com)']  # la representación exacta puede variar
```

**Criterios de aceptación**

* Importar desde `app` funciona y expone las clases clave.
* Crear usuarios/roles y almacenarlos en `RepositorioUsuarios` sin errores.
* Email inválido lanza `ValueError`.
* Duplicados por email lanzan `ValueError`.

---

## 🔥 Reto (opcional)

1. **`utils.hash_password` real**: crea funciones con `hashlib.sha256` y úsalo en `Usuario`.
2. **`__eq__` y `__hash__` en `Usuario`**: igualdad por email normalizado; permite usar usuarios en `set`.
3. **Dividir `modelos.py`** en submódulos (`dominio/usuario.py`, `dominio/roles.py`) y re-exportar desde `app/__init__.py`.