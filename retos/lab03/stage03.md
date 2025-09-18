# ✅ Resolución paso a paso

---

## 🔹 Reto 1 — Confirmar que `BaseUsuario` es abstracta

### 🎯 Objetivo:

Demostrar que **no se puede instanciar** directamente una clase abstracta.

---

### 1. Asegúrate de que `BaseUsuario` hereda de `ABC` y tiene al menos un `@abstractmethod`:

```python
from abc import ABC, abstractmethod

class BaseUsuario(ABC):
    @abstractmethod
    def permisos(self) -> list[str]:
        ...
```

---

### 2. En `main.py`, añade este bloque:

```python
from app.modelos import BaseUsuario

try:
    b = BaseUsuario()
except TypeError as e:
    print("Instancia bloqueada correctamente:", e)
```

---

### ✅ Resultado esperado:

Al ejecutar `python main.py`, deberías ver algo como:

```
Instancia bloqueada correctamente: Can't instantiate abstract class BaseUsuario with abstract method permisos
```

---

## 🔹 Reto 2 — Verificar los permisos por rol

### 🎯 Objetivo:

Comparar los métodos `permisos()` y `tiene_permiso()` según el tipo de usuario.

---

### 1. Asegúrate de que las subclases sobrescriben correctamente `permisos()`:

```python
class Admin(Usuario):
    def permisos(self) -> list[str]:
        return ["ver", "crear", "editar", "borrar"]

class Invitado(Usuario):
    def permisos(self) -> list[str]:
        return ["ver"]
```

La clase `Usuario` ya define:

```python
def permisos(self) -> list[str]:
    return ["ver"]
```

---

### 2. En `main.py`, añade:

```python
from app.modelos import Usuario, Admin, Invitado

a = Admin("Root", "root@corp.com")
i = Invitado("Visitante", "visitante@mail.com")
u = Usuario("Ana", "ana@mail.com")

print("Admin:", a.permisos(), a.tiene_permiso("borrar"))     # True
print("Invitado:", i.permisos(), i.tiene_permiso("borrar"))  # False
print("Usuario:", u.permisos(), u.tiene_permiso("ver"))      # True
```

---

### ✅ Resultado esperado:

```
Admin: ['ver', 'crear', 'editar', 'borrar'] True
Invitado: ['ver'] False
Usuario: ['ver'] True
```

---

## 🔹 Reto 3 — Personalizar `__str__` para `Admin`

### 🎯 Objetivo:

Redefinir el método `__str__()` para una subclase y conservar lo del padre.

---

### 1. Modifica `Admin` en `modelos.py`:

```python
class Admin(Usuario):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, rol="admin", activo=activo)

    def permisos(self) -> list[str]:
        return ["ver", "crear", "editar", "borrar"]

    def __str__(self) -> str:
        return f"[ADMIN] {super().__str__()}"
```

> Ya se está usando `__str__()` en `Usuario`, así que reutilizamos la salida.

---

### 2. En `main.py`, añade:

```python
print(a)  # objeto de tipo Admin
```

---

### ✅ Resultado esperado:

```
[ADMIN] Root <root@corp.com> (admin) [activo]
```

---

## ✅ Conclusión

Con estos tres retos resueltos, los alumnos comprenden de forma clara:

| Concepto            | Aprendido a través de…                    |
| ------------------- | ----------------------------------------- |
| Abstracción         | Clase `BaseUsuario` y error al instanciar |
| Herencia funcional  | `.permisos()` personalizado en subclases  |
| Polimorfismo visual | `__str__()` específico para `Admin`       |