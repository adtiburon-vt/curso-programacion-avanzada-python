# 🩹 Parche 1 — `Admin.presentarse` usando `super()`

**En `app/modelos.py`, dentro de `class Admin(Usuario):` añade:**

```python
def presentarse(self) -> str:
    base = super().presentarse()   # "Soy {nombre} ({email})"
    return f"[ADMIN] {base}"
```

---

# 🩹 Parche 2 — `Moderador.__str__` reutilizando `Usuario.__str__`

**Sustituye el `__str__` actual de `Moderador` por:**

```python
def __str__(self) -> str:
    return f"[MODERADOR-N{self.nivel}] {super().__str__()}"
```

*(No toques `Usuario.__str__`: sigue siendo la fuente de verdad del formato base.)*

---

## 🧪 Checks exprés (añadir 4–6 líneas en `main.py`)

```python
from app.modelos import Admin, Moderador

a = Admin("Root", "root@corp.com")
m1 = Moderador("Lucía", "lucia@test.com", nivel=1)
m2 = Moderador("Carlos", "carlos@test.com", nivel=2, activo=False)

print(a.presentarse())  # [ADMIN] Soy Root (root@corp.com)
print(str(m1))          # [MODERADOR-N1] Lucía <lucia@test.com> (moderador) [activo]
print(str(m2))          # [MODERADOR-N2] Carlos <carlos@test.com> (moderador) [inactivo]
```

---

## ✅ Criterios rápidos

* `Admin(...).presentarse()` → `"[ADMIN] Soy …"`.
* `str(Moderador(..., nivel=1))` empieza con `"[MODERADOR-N1]"` y luego el `__str__` base.
* `Moderador(..., nivel=2).permisos()` incluye `"borrar"` (sin cambios en este parche).
