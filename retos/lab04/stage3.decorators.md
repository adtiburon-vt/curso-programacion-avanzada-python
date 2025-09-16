Perfecto. Si ahora quieres saber **cómo usar decoradores para integrar funcionalidad similar a estos mixins**, te explico paso a paso **cómo convertir el comportamiento de los mixins en decoradores**, y **cómo aplicarlos sin modificar la jerarquía de clases**.

---

## 🎯 Objetivo

Usar **decoradores** para **extender el comportamiento de los métodos** `activar()`, `presentarse()` o incluso `__init__()`, **sin necesidad de heredar mixins como clases**.

Esto refuerza el concepto de **composición por funciones** (decoradores), como alternativa a **composición por clases** (mixins).

---

# ✅ Versión con decoradores – Resolución paso a paso

---

## 🔹 Decorador 1 — Logging simple (sustituye a `LoggerMixin`)

### 1. En `app/utils.py`, define el decorador `con_logging`:

```python
from functools import wraps
from datetime import datetime
from typing import Any, Callable

def con_logging(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        ts = datetime.now().isoformat(timespec="seconds")
        who = getattr(self, "email", "desconocido")
        print(f"[{ts}] [{self.__class__.__name__}] <{who}> INICIO: {func.__name__}")
        res = func(self, *args, **kwargs)
        print(f"[{ts}] [{self.__class__.__name__}] <{who}> FIN: {func.__name__}")
        return res
    return wrapper
```

---

### 2. En `app/modelos.py`, aplica el decorador a `activar()` de `Admin`:

```python
from .utils import con_logging

class Admin(Usuario):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, rol="admin", activo=activo)

    @con_logging
    def activar(self):
        super().activar()

    def permisos(self) -> list[str]:
        return ["ver", "crear", "editar", "borrar"]

    def presentarse(self) -> str:
        return f"[ADMIN] {super().presentarse()}"
```

> 🔁 Esto **elimina la necesidad de LoggerMixin** por completo.

---

### ✅ Resultado esperado en `main.py`:

```python
a = Admin("Root", "root@corp.com")
a.activar()
```

🟢 Imprime:

```
[ts] [Admin] <root@corp.com> INICIO: activar
[ts] [Admin] <root@corp.com> FIN: activar
```

---

## 🔹 Decorador 2 — Auditoría (sustituye a `AuditoriaMixin`)

### 1. En `app/utils.py`, añade este decorador con almacenamiento en `self._audit`:

```python
def con_auditoria(evento: str):
    def decorador(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "_audit"):
                self._audit = []
            self._audit.append(f"ANTES: {evento}")
            res = func(self, *args, **kwargs)
            self._audit.append(f"DESPUÉS: {evento}")
            return res
        return wrapper
    return decorador
```

---

### 2. En `app/modelos.py`, aplica el decorador:

```python
from .utils import con_auditoria

class Admin(Usuario):
    ...

    @con_auditoria("activar usuario")
    def activar(self):
        super().activar()
```

---

### 3. En `main.py`, comprueba el historial:

```python
a = Admin("Eva", "eva@corp.com")
a.activar()
print("Auditoría:", getattr(a, "_audit", []))
```

🟢 Resultado:

```
Auditoría: ['ANTES: activar usuario', 'DESPUÉS: activar usuario']
```

---

## 🔹 Decorador 3 — Enviar email (como el `NotificadorMixin`)

### 1. En `app/utils.py`, añade:

```python
def enviar_email_al_final(asunto: str, cuerpo: str):
    def decorador(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            print(f"[EMAIL a {self.email}] {asunto}: {cuerpo}")
            return res
        return wrapper
    return decorador
```

---

### 2. En `app/modelos.py`, aplica a `presentarse()`:

```python
from .utils import enviar_email_al_final

class Admin(Usuario):
    ...

    @enviar_email_al_final("Presentación", "El usuario se ha presentado.")
    def presentarse(self) -> str:
        return f"[ADMIN] {super().presentarse()}"
```

---

### 3. En `main.py`:

```python
a = Admin("Alice", "alice@corp.com")
print(a.presentarse())
```

🟢 Resultado:

```
[ADMIN] Soy Alice (alice@corp.com)
[EMAIL a alice@corp.com] Presentación: El usuario se ha presentado.
```

---

# 🧠 Comparación: Decoradores vs. Mixins

| Mixins                                 | Decoradores                         |
| -------------------------------------- | ----------------------------------- |
| Se aplican vía herencia (`class A(B)`) | Se aplican directamente a métodos   |
| Afectan a toda la clase                | Puedes usarlos en métodos puntuales |
| Se agrupan como capacidades (clases)   | Se agrupan como funciones           |
| Componen el MRO                        | No afectan la herencia              |

---

# APLICAR DECORADORES EN METODOS EN LUGAR DE EN CLASES

---

## ✅ 1. ¿Por qué aplicar el decorador al método?

Porque el comportamiento deseado (log, auditoría, email…) se quiere aplicar **solo a una acción concreta** como `activar()` o `presentarse()`, no a todos los métodos de la clase.

---

### 🧪 Ejemplo:

```python
@con_logging
def activar(self):
    ...
```

👉 Solo se logueará esa función. No se modifican otros métodos como `desactivar()` o `presentarse()`.

---

## ❌ 2. ¿Y si aplicamos el decorador a la clase?

```python
@mi_decorador
class Admin(Usuario):
    ...
```

Esto es **válido**, pero **muy diferente**:

* El decorador recibe la clase **entera** como argumento.
* Se usa para **alterar o envolver toda la clase**: su constructor, atributos, todos los métodos, etc.
* Es más invasivo y requiere lógica más compleja.

---

### 🧠 Ejemplo de decorador de clase (avanzado):

```python
def decorador_de_clase(cls):
    original_init = cls.__init__

    def nuevo_init(self, *args, **kwargs):
        print("Instanciando con logging")
        original_init(self, *args, **kwargs)

    cls.__init__ = nuevo_init
    return cls

@decorador_de_clase
class Admin:
    ...
```

Esto solo afecta al `__init__`, pero no te da control fino sobre otros métodos como `activar`.

---

## 🛠️ Comparación

| Decorador aplicado a...  | Afecta a...                            | Uso típico                             |
| ------------------------ | -------------------------------------- | -------------------------------------- |
| Un **método específico** | Solo ese método                        | Logging, auditoría, validación, timing |
| Una **clase completa**   | Toda la clase: constructor y/o métodos | Meta-programación, wrappers globales   |

---

## 🎯 En resumen

En tu caso, **querías modularizar comportamientos transversales como logging o auditoría** de forma muy similar a cómo funcionan los mixins → y esos mixins redefinían métodos concretos.

Por eso:
✅ **Lo más limpio y controlado es aplicar decoradores directamente a los métodos** que te interesa extender.




# 📁 Estructura y codigo final del proyecto

```
lab_mixins_decorators/
├─ app/
│  ├─ __init__.py
│  ├─ modelos.py
│  └─ utils.py
└─ main.py
```

---

## 📄 `app/__init__.py`

```python
from .modelos import Usuario, Admin
```

---

## 📄 `app/utils.py`

```python
from functools import wraps
from datetime import datetime
from typing import Callable, Any


def con_logging(func: Callable) -> Callable:
    """Log simple antes y después de ejecutar el método."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        ts = datetime.now().isoformat(timespec="seconds")
        who = getattr(self, "email", "desconocido")
        print(f"[{ts}] [{self.__class__.__name__}] <{who}> INICIO: {func.__name__}")
        res = func(self, *args, **kwargs)
        print(f"[{ts}] [{self.__class__.__name__}] <{who}> FIN: {func.__name__}")
        return res
    return wrapper


def con_auditoria(evento: str):
    """Decora el método para registrar eventos en self._audit."""
    def decorador(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, "_audit"):
                self._audit = []
            self._audit.append(f"ANTES: {evento}")
            res = func(self, *args, **kwargs)
            self._audit.append(f"DESPUÉS: {evento}")
            return res
        return wrapper
    return decorador


def enviar_email_al_final(asunto: str, cuerpo: str):
    """Al terminar el método, simula envío de email al usuario."""
    def decorador(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            print(f"[EMAIL a {self.email}] {asunto}: {cuerpo}")
            return res
        return wrapper
    return decorador
```

---

## 📄 `app/modelos.py`

```python
from .utils import con_logging, con_auditoria, enviar_email_al_final


class BaseUsuario:
    def permisos(self) -> list[str]:
        raise NotImplementedError("Debe implementarse en subclases.")

    def tiene_permiso(self, p: str) -> bool:
        return p in self.permisos()


class Usuario(BaseUsuario):
    def __init__(self, nombre: str, email: str, rol: str = "usuario", activo: bool = True):
        super().__init__()
        self.nombre = nombre
        self.email = email
        self.rol = rol
        self.activo = activo

    def __str__(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"{self.nombre} <{self.email}> ({self.rol}) [{estado}]"

    def activar(self):
        self.activo = True

    def desactivar(self):
        self.activo = False

    def permisos(self) -> list[str]:
        return ["ver"]

    def presentarse(self) -> str:
        return f"Soy {self.nombre} ({self.email})"


class Admin(Usuario):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, rol="admin", activo=activo)

    @con_logging
    @con_auditoria("activar usuario")
    def activar(self):
        super().activar()

    @enviar_email_al_final("Presentación", "El usuario se ha presentado.")
    def presentarse(self) -> str:
        return f"[ADMIN] {super().presentarse()}"

    def permisos(self) -> list[str]:
        return ["ver", "crear", "editar", "borrar"]
```

---

## 📄 `main.py`

```python
from app.modelos import Admin

if __name__ == "__main__":
    a = Admin("Alice", "alice@corp.com")

    # Presentarse (debería enviar un email)
    print(a.presentarse())

    # Activar (debería auditar y hacer logging)
    a.activar()

    # Mostrar la auditoría
    print("Auditoría:", getattr(a, "_audit", []))
```

---

## ✅ Resultado al ejecutar `python main.py`:

Ejemplo de salida:

```
[EMAIL a alice@corp.com] Presentación: El usuario se ha presentado.
[2025-09-16T13:42:10] [Admin] <alice@corp.com> INICIO: activar
[2025-09-16T13:42:10] [Admin] <alice@corp.com> FIN: activar
Auditoría: ['ANTES: activar usuario', 'DESPUÉS: activar usuario']
```
