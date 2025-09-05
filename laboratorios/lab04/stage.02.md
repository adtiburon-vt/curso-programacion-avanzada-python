# 🔹 Fase 2: Sobrescritura de métodos con `super()` (Admin y Moderador)

### 🎯 Objetivo

Aprender a **extender** comportamiento sin duplicar código:

* Sobrescribir `presentarse()` en `Admin` usando `super()`.
* Reescribir `__str__()` en `Moderador` para **reutilizar** la versión de `Usuario` con `super()` y añadir el nivel.

> Partimos del proyecto del Lab 3 + Fase 1 (ya tienes `Usuario`, `Admin`, `Invitado`, `Moderador`).

---

### 🧱 Cambios en `app/modelos.py`

**1) `Admin.presentarse` con `super()`**

```python
class Admin(Usuario):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, rol="admin", activo=activo)

    def permisos(self) -> list[str]:
        return ["ver", "crear", "editar", "borrar"]

    # ✅ NUEVO: extender sin duplicar
    def presentarse(self) -> str:
        base = super().presentarse()   # "Soy {nombre} ({email})"
        return f"[ADMIN] {base}"
```

**2) `Moderador.__str__` reusando `Usuario.__str__` con `super()`**

Sustituye la implementación anterior para no repetir lógica:

```python
class Moderador(Usuario):
    def __init__(self, nombre: str, email: str, nivel: int = 1, activo: bool = True):
        super().__init__(nombre, email, rol="moderador", activo=activo)
        self.nivel = nivel

    def permisos(self) -> list[str]:
        base = ["ver", "editar"]
        if self.nivel >= 2:
            base.append("borrar")
        return base

    # ✅ REESCRITO: aprovechar el __str__ del padre
    def __str__(self) -> str:
        return f"[MODERADOR-N{self.nivel}] {super().__str__()}"
```

*(Asegúrate de mantener el `__str__` de `Usuario` como la fuente de verdad del formato base.)*

---

### 🧪 `main.py` (pruebas rápidas)

```python
from app.modelos import Admin, Moderador

if __name__ == "__main__":
    a = Admin("Root", "root@corp.com")
    m1 = Moderador("Lucía", "lucia@test.com", nivel=1)
    m2 = Moderador("Carlos", "carlos@test.com", nivel=2, activo=False)

    print(a.presentarse())           # [ADMIN] Soy Root (root@corp.com)
    print(str(m1))                   # [MODERADOR-N1] Lucía <lucia@test.com> (moderador) [activo]
    print(str(m2))                   # [MODERADOR-N2] Carlos <carlos@test.com> (moderador) [inactivo]

    print("Permisos m1:", m1.permisos())  # ['ver','editar']
    print("Permisos m2:", m2.permisos())  # ['ver','editar','borrar']
```

---

### 🧭 Pasos

1. En `Admin`, sobrescribe `presentarse()` y **antepone** `[ADMIN]` al mensaje **base** obtenido con `super().presentarse()`.
2. En `Moderador`, reescribe `__str__()` para **envolver** el `__str__` de `Usuario` con un prefijo que muestre el nivel.
3. Ejecuta `python main.py` y verifica las salidas.

---

### ✅ Criterios de aceptación

* `Admin("Root","root@corp.com").presentarse()` → `"[ADMIN] Soy Root (root@corp.com)"`.
* `str(Moderador("Lucía","lucia@test.com",1))` → empieza por `"[MODERADOR-N1]"` y luego el `__str__` base del usuario.
* `Moderador(nivel=2).permisos()` incluye `"borrar"`.

---

### 🔥 Reto (opcional)

1. **Extensión en cadena**: crea `SuperAdmin(Admin)` que en `presentarse()` añada otro prefijo `[SUPER]` pero siga usando `super()` (debe quedar `"[SUPER][ADMIN] Soy ..."`).
2. **Hook de activación**: sobrescribe `activar()` en `Moderador` para imprimir un aviso y luego llamar a `super().activar()`.
3. **Validación de `nivel`**: convierte `nivel` en propiedad con setter que solo admita enteros ≥ 1 (lanza `ValueError` si no).