# 🩹 Parche 1 — Inmutabilidad parcial del email + método `cambiar_email`

**En `app/modelos.py`**:

1. En `__init__` **sustituye** la asignación del email por un atributo interno:

```python
self._email = email  # en lugar de self.email = email
```

2. **Añade** la propiedad (getter + setter que bloquea asignación directa) y el método:

```python
@property
def email(self) -> str:
    return self._email

@email.setter
def email(self, _):
    raise AttributeError("Usa cambiar_email(nuevo_email)")

def cambiar_email(self, nuevo_email: str) -> None:
    self._email = nuevo_email
```

> Resultado: `u.email = "x@y.com"` lanza error; solo vale `u.cambiar_email(...)`.

---

# 🩹 Parche 2 — Igualdad por email (normalizado)

**En `app/modelos.py`**, añade:

```python
@staticmethod
def _norm_email(e: str) -> str:
    return (e or "").strip().lower()

def __eq__(self, other) -> bool:
    if not isinstance(other, Usuario):
        return NotImplemented
    return self._norm_email(self.email) == self._norm_email(other.email)

def __hash__(self) -> int:
    return hash(self._norm_email(self.email))
```

> Permite comparar usuarios por email ignorando mayúsculas/espacios y usarlos en `set`/`dict`.

---

# 🩹 Parche 3 — Factory `desde_tupla`

**En `app/modelos.py`**, añade:

```python
@classmethod
def desde_tupla(cls, t):
    nombre, email, activo = t
    return cls(nombre, email, activo)
```

---

## 🧪 Checks rápidos (añade al final de `main.py`, o en tu bloque de pruebas)

```python
# Inmutabilidad parcial
try:
    u1.email = "otro@test.com"
except AttributeError:
    print("OK: email no se puede asignar directamente")

u1.cambiar_email("nuevo@test.com")
print("Email cambiado:", u1.email)

# Igualdad por email (normalizado)
a = Usuario("Ana", "ANA@test.com  ")
b = Usuario("Otra", "ana@test.com")
print("Iguales por email:", a == b)  # True

# Factory
u4 = Usuario.desde_tupla(("Pepe", "pepe@test.com", True))
print("Factory:", u4.presentarse())
```
