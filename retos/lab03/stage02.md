# Fase 2 – Retos opcionales

## 1) Reto 1 — Validador de email mejorado en `utils.py`

### Pasos

1. Crea `app/utils.py`.
2. Implementa `normalizar_email` con **regex pragmática** (dominio con al menos un punto, admite guiones).
3. Reutiliza esta función desde el **setter** de `email`.

### Código

```python
# app/utils.py
import re

# Regex pragmática (no 100% RFC, suficiente para el lab)
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")

def normalizar_email(value: str) -> str:
    v = (value or "").strip().lower()
    if not EMAIL_RE.match(v):
        raise ValueError(f"Email inválido: {value!r}")
    return v
```

```python
# app/modelos.py (solo el setter de email cambia)
from app.utils import normalizar_email

# ...
    @email.setter
    def email(self, value: str) -> None:
        self._email = normalizar_email(value)
# ...
```

### Prueba rápida (añadir al final de main.py)

```python
for malo in ["sin-arroba", "x@", "@x", "a@b", "a@b.", "a@.com", "a@-dominio.com"]:
    try:
        u.email = malo
        print("ERROR: debería fallar:", malo)
    except ValueError:
        print("Email inválido OK:", malo)
```

---

## 2) Reto 2 — `__eq__` y `__hash__` por email normalizado

### Pasos

1. Define `__eq__` comparando `self.email` con `other.email`.
2. Define `__hash__` consistente con `__eq__` (mismo campo).
3. Así dos usuarios con el **mismo email normalizado** serán iguales.

### Código

```python
# app/modelos.py (añadir estos métodos)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Usuario):
            return NotImplemented
        return self.email == other.email  # ya normalizado por el setter

    def __hash__(self) -> int:
        return hash(self.email)
```

### Prueba rápida (añadir al final de main.py)

```python
u1 = Usuario("A", "X@Y.com")
u2 = Usuario("B", "x@y.com")
print("Igualdad por email OK:", u1 == u2)
print("Set compacta OK:", len({u1, u2}) == 1)
```

---

## 3) Reto 3 — Roles extensibles con `@classmethod add_rol`

### Pasos

1. Añade `add_rol(cls, rol)` que:

   * normaliza a minúsculas,
   * valida formato simple (minúsculas y `-`),
   * evita duplicados/vacíos,
   * añade a `ROLES_VALIDOS`.
2. Comprueba que luego puedas asignar ese rol a un usuario.

### Código

```python
# app/modelos.py (añadir al final de la clase)
    @classmethod
    def add_rol(cls, rol: str) -> None:
        r = (rol or "").strip().lower()
        if not r or r in cls.ROLES_VALIDOS:
            raise ValueError(f"Rol ya existe o vacío: {rol!r}")
        if not all(c.islower() or c == "-" for c in r):
            raise ValueError("Formato de rol inválido (usa minúsculas y guiones)")
        cls.ROLES_VALIDOS.add(r)
```

### Prueba rápida (añadir al final de main.py)

```python
try:
    Usuario.add_rol("editor-jr")
    u3 = Usuario("C", "c@x.com", rol="editor-jr")
    print("Rol extendido OK:", u3.rol in Usuario.ROLES_VALIDOS, "->", u3.rol)
except ValueError as e:
    print("Fallo al extender rol:", e)

# Casos negativos
for r in ["", "Admin", "editor jr", "usuario"]:
    try:
        Usuario.add_rol(r)
        print("ERROR: no debería aceptarse:", r)
    except ValueError:
        print("Rechazo de rol OK:", r)
```

---

## ✅ Checklist de aceptación

* `Usuario("Ana","ANA@Test.com").email == "ana@test.com"` ✅
* `u.email = "x@"` o `"@x"` → `ValueError` (regex de `utils.py`) ✅
* `u1 == u2` si emails equivalen normalizados; `len({u1,u2}) == 1` ✅
* `Usuario.add_rol("editor-jr")` añade; asignar `rol="editor-jr"` funciona ✅
* Roles inválidos se rechazan (`"", "Admin", "editor jr", "usuario"`) ✅