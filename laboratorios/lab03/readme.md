# 🧭 Laboratorio 3 — Modelado de un sistema de usuarios con clases

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 3 (POO: clases/atributos/métodos/constructores; encapsulación y abstracción)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

Diseñar y construir un **modelo orientado a objetos** para un sistema de usuarios, aplicando:

* Definición de clases con **atributos y métodos**.
* **Constructores** y métodos especiales (`__str__`, `__repr__`).
* **Encapsulación** con `@property` y convención `_protegido` / `__privado`.
* **Abstracción** con clases base y `@abstractmethod`.
* Herencia simple (usuarios con **roles** especializados).

---

## 📁 Estructura sugerida del proyecto

```
lab3_sistema_usuarios/
├─ app/
│  ├─ __init__.py
│  ├─ modelos.py          # Clases: Usuario (base), Admin, Invitado, etc.
│  ├─ repositorio.py      # Repositorio en memoria (opcional en Fase 3)
│  └─ utils.py            # Validaciones simples, helpers (email, etc.)
└─ main.py                # Script de demostración / pruebas manuales
```

> Puedes empezar con un único archivo `modelos.py` y extraer a `utils.py`/`repositorio.py` en la Fase 3.

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1: Clase `Usuario` (atributos, métodos y constructores)

**Objetivo:** modelar la entidad base `Usuario` con datos y comportamiento básicos.

**Requisitos mínimos**

* Clase `Usuario` con `nombre`, `email` y `activo` (bool, por defecto `True`).
* Métodos de instancia:

  * `presentarse()` → `str` legible (“Soy Ana ([ana@test.com](mailto:ana@test.com))”).
  * `desactivar()` / `activar()` → cambia `activo`.
* Métodos especiales:

  * `__str__` y `__repr__` coherentes.
* Contador de instancias (atributo de clase `contador`).

**Producto esperado:** `app/modelos.py` con la clase `Usuario` y pruebas en `main.py`.

**Validación**

* Crear 2–3 usuarios, comprobar `presentarse()`, estado `activo` y `contador`.

---

### 🔹 Fase 2: Encapsulación y validación con `@property`

**Objetivo:** proteger y validar atributos con propiedades y convenciones.

**Requisitos mínimos**

* Convertir `email` en atributo **encapsulado** (`_email`) con:

  * `@property email` y `@email.setter`: validar formato sencillo (`"@" in email`).
* Atributo protegido `_rol` (string) con getter/setter o propiedad:

  * Aceptar solo valores de `{"usuario", "admin", "invitado"}` (o los que definas).
* Atributo privado `__password_hash` (simulación; no hace falta hashing real):

  * Método `set_password(p)` que guarde algo como `f"hash::{p}"`.
  * Método `check_password(p)` → `True/False` comparando con el “hash”.
* Método de clase `desde_dict(cls, datos: dict)` que construya usuarios desde un diccionario.

**Producto esperado:** `Usuario` con propiedades y validaciones en `app/modelos.py`.

**Validación**

* Intentar asignar un email inválido debe lanzar `ValueError`.
* Asignar rol no permitido debe lanzar `ValueError`.
* `set_password("secreta")` + `check_password("secreta")` → `True`.

---

### 🔹 Fase 3: Abstracción + herencia por roles y repositorio simple

**Objetivo:** añadir **clase base abstracta** y subclases con comportamiento específico; opcionalmente un repositorio en memoria.

**Requisitos mínimos**

* Clase base abstracta `BaseUsuario` (`abc.ABC`) con:

  * `@abstractmethod permisos()` → devuelve `list[str]` o `set[str]`.
* Hacer que `Usuario` **herede de `BaseUsuario`** e implemente `permisos()`.
* Subclases:

  * `Admin(Usuario)` → `permisos()` amplios (p. ej. `{"crear","editar","borrar","ver"}`).
  * `Invitado(Usuario)` → permisos limitados (p. ej. `{"ver"}`).
* Método `tiene_permiso(nombre_permiso: str) -> bool`.

**(Opcional) Repositorio en memoria**

* `RepositorioUsuarios` con operaciones:

  * `agregar(usuario)`, `obtener_por_email(email)`, `listar_activos()`, `eliminar(email)`.
  * (Opcional) `buscar(predicate)` para filtrar arbitrario (lambda).

**Producto esperado:** `app/modelos.py` con jerarquía de clases; `app/repositorio.py` simple; `main.py` con demo.

**Validación**

* Instanciar `Admin` e `Invitado`, verificar `permisos()` y `tiene_permiso(...)`.
* Probar repositorio: agregar/listar/buscar/eliminar; evitar duplicados por email (lanzar `ValueError` si ya existe).

---

## 🧠 Reflexión final

* ¿Qué ventajas te dio **encapsular** `email` y `rol` con propiedades respecto a atributos públicos?
* ¿Qué **contrato** establece la clase base `BaseUsuario` y qué garantiza en las subclases?
* Si mañana añades un nuevo rol (`Moderador`), ¿qué partes del diseño permanecen **estables**?

---

## ✅ Comprobación de conocimientos

1. Implementa `__eq__` en `Usuario` para considerar **igualdad por email** (case-insensitive).
2. Añade un método de clase `administrador_por_defecto()` que cree un `Admin` con nombre y email predefinidos.
3. Implementa `RepositorioUsuarios.actualizar(email, **campos)` que use propiedades para validar cambios.

---

## 🔥 Retos (opcionales)

* **Factory por rol**: `Usuario.desde_dict` detecta `rol` y devuelve `Admin` o `Invitado` automáticamente.
* **Password real**: usa `hashlib.sha256` para calcular y verificar hash (sin almacenar el texto plano).
* **Persistencia ligera**: exporta/importa usuarios en JSON (solo datos públicos y el hash).

---

## 🧱 Scaffold de partida (mínimo)

**app/modelos.py**

```python
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
```

**app/repositorio.py** (opcional Fase 3)

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
        return self._por_email.get(email.lower().strip())

    def listar_activos(self):
        return [u for u in self._por_email.values() if u.activo]

    def eliminar(self, email: str):
        self._por_email.pop(email.lower().strip(), None)

    def buscar(self, predicado: Callable[[Usuario], bool]):
        return [u for u in self._por_email.values() if predicado(u)]
```

**main.py**

```python
from app.modelos import Usuario, Admin, Invitado, tiene_permiso
# from app.repositorio import RepositorioUsuarios

if __name__ == "__main__":
    u = Usuario("Ana", "ana@test.com")
    a = Admin("Root", "root@corp.com")
    g = Invitado("Visitante", "guest@example.org")

    print(u.presentarse(), u.permisos())
    print(a.presentarse(), a.permisos(), tiene_permiso(a, "borrar"))
    print(g)

    # u.email = "mal_email"  # descomenta para ver ValueError
```

