# 🩹 Parche 1 — Importar ABC y declarar base abstracta

**En `app/modelos.py` (cabecera del módulo):**

```python
from __future__ import annotations
from abc import ABC, abstractmethod
```

**Debajo de los imports (antes de `Usuario`):**

```python
class BaseUsuario(ABC):
    @abstractmethod
    def permisos(self) -> list[str]:
        ...

    def tiene_permiso(self, permiso: str) -> bool:
        return permiso in self.permisos()
```

---

# 🩹 Parche 2 — `Usuario` hereda de `BaseUsuario` e implementa permisos

**Cambia la firma de clase:**

```python
class Usuario(BaseUsuario):
```

**Añade al final de la clase `Usuario` (método concreto):**

```python
def permisos(self) -> list[str]:
    return ["ver"]
```

> Con esto `Usuario` cumple el contrato abstracto.

---

# 🩹 Parche 3 — Subclases por rol

**Añade debajo de `Usuario`:**

```python
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

---

# 🧪 Checks exprés (añade 5–7 líneas a `main.py`)

```python
from app.modelos import BaseUsuario, Usuario, Admin, Invitado

a = Admin("Root", "root@corp.com")
g = Invitado("Guest", "guest@mail.org")
u = Usuario("Ana", "ana@test.com")

print(a.tiene_permiso("borrar"))  # True
print(g.tiene_permiso("borrar"))  # False
print(u.permisos())               # ["ver"]

try:
    BaseUsuario()  # debe fallar (abstracta)
except TypeError as e:
    print("Abstracta OK:", e)
```

---

## (Opcional) 🩹 Parche 4 — Repositorio en memoria

**Crear `app/repositorio.py` con lo mínimo:**

```python
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

**Test opcional en `main.py` (3 líneas):**

```python
from app.repositorio import RepositorioUsuarios
repo = RepositorioUsuarios(); repo.agregar(u); print(len(repo.listar_activos()))
```

---

### ✅ Validación rápida

* `Admin(...).tiene_permiso("borrar") → True`; `Invitado(...).tiene_permiso("borrar") → False`.
* Instanciar `BaseUsuario()` → `TypeError`.
* `Usuario(...).permisos() → ["ver"]`.
* (Repo) Duplicar email → `ValueError`; `listar_activos()` excluye desactivados.