# 🔹 Fase 3: Abstracción + herencia por roles (y repositorio opcional)

### 🎯 Objetivo

Introducir una **clase base abstracta** para usuarios, crear **subclases por rol** con permisos diferenciados, y (opcional) un **repositorio en memoria** para gestionar usuarios.

---

## 🧱 Scaffold (continúa en tu proyecto)

### 1) `app/modelos.py` — añade clase base y subclases

```python
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
```

### 2) (Opcional) `app/repositorio.py` — repositorio en memoria

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
        return self._por_email.get(email.lower().strip())

    def listar_activos(self) -> list[Usuario]:
        return [u for u in self._por_email.values() if u.activo]

    def eliminar(self, email: str):
        self._por_email.pop(email.lower().strip(), None)

    def buscar(self, predicado: Callable[[Usuario], bool]) -> list[Usuario]:
        return [u for u in self._por_email.values() if predicado(u)]
```

### 3) `main.py` — demo rápida

```python
# main.py
from app.modelos import Usuario, Admin, Invitado, BaseUsuario

if __name__ == "__main__":
    a = Admin("Root", "root@corp.com")
    g = Invitado("Visitante", "guest@mail.org")
    u = Usuario("Ana", "ana@test.com")

    print(a.presentarse(), a.permisos(), a.tiene_permiso("borrar"))
    print(g.presentarse(), g.permisos(), g.tiene_permiso("borrar"))
    print(u.presentarse(), u.permisos(), u.tiene_permiso("ver"))

    try:
        BaseUsuario()  # ❌ debe fallar: clase abstracta
    except TypeError as e:
        print("Abstracta OK:", e)
```

---

## 🧭 Pasos

1. **Crear `BaseUsuario(ABC)`** con `permisos()` abstracto y `tiene_permiso()` común.
2. **Heredar `Usuario` de `BaseUsuario`** e implementar `permisos()` por defecto.
3. **Crear `Admin` e `Invitado`** que especialicen `permisos()`.
4. (Opcional) **Repositorio en memoria** con `agregar/obtener/eliminar/listar/buscar`.
5. **Probar en `main.py`** permisos y errores esperados (instancia abstracta).

---

## ✅ Validación (criterios de aceptación)

* `Admin(...).tiene_permiso("borrar")` → `True`; `Invitado(...).tiene_permiso("borrar")` → `False`.
* Instanciar `BaseUsuario()` lanza `TypeError` (abstracta).
* `Usuario(...).permisos()` → `["ver"]`.
* (Repositorio) Añadir dos usuarios con el mismo email lanza `ValueError`.
* (Repositorio) `listar_activos()` excluye los desactivados.

---

## 🔥 Retos (opcionales)

1. **Factory por rol** en `Usuario.desde_dict`: devuelve `Admin` o `Invitado` si `rol` lo indica.
2. **Igualdad/Hash**: `__eq__` por email normalizado y `__hash__` consistente (para usar en `set`).
3. **Permisos compuestos**: añade un tipo `Permiso` y compón permisos por rol desde un “catálogo” central.
4. **Persistencia**: exporta/importa usuarios del repositorio a JSON (sin contraseñas en claro).

---

# ✅ Conclusión del Laboratorio 3

**Qué has construido:**

* Una **jerarquía POO** clara: `BaseUsuario` (contrato) → `Usuario` (impl. base) → `Admin`/`Invitado` (especializaciones).
* **Encapsulación real** con propiedades (`email`, `rol`) y estado privado de contraseña.
* **Permisos** expresados como capacidad de negocio (`tiene_permiso`).
* (Opcional) Un **repositorio** ligero para CRUD en memoria.

**Aprendizajes clave:**

* Diferenciar **atributos** de instancia/clase y usar **métodos especiales**.
* Encapsular con `@property` y validar en setters (fuente de la verdad).
* Definir **abstracciones** con `ABC` para garantizar contratos entre subclases.
* Diseñar **herencias útiles** (rol → comportamiento) evitando sobreacoplar.

**Listo para evolucionar:**

* Sustituir el repositorio en memoria por uno **persistente** (SQLite/SQLAlchemy).
* Añadir **tests `unittest/pytest`** para cada método crítico.
* Integrar **decoradores** (del Lab 1) para logging/timing en operaciones del repositorio.