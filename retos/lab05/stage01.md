# ✅ Resolución Paso a Paso

---

## 🔹 Reto 1 — Normalización centralizada de email

### 🎯 Objetivo:

Evitar repetir `email.strip().lower()` en `modelos.py` y `repositorio.py`.

---

### 1. Añade en `app/utils.py`:

Debajo de `validar_email`, define la función:

```python
def normalizar_email(email: str) -> str:
    return (email or "").strip().lower()
```

---

### 2. En `app/modelos.py`

#### 🟡 Sustituye esta línea del setter:

```python
self._email = value.strip().lower()
```

#### ✅ Por esta:

```python
from .utils import validar_email, normalizar_email
...
self._email = normalizar_email(value)
```

---

### 3. En `app/repositorio.py`

#### 🟡 Sustituye esto (aparece 2 veces):

```python
(email or "").strip().lower()
```

#### ✅ Por esto:

```python
from .utils import normalizar_email
...
normalizar_email(email)
```

Así:

```python
def obtener_por_email(self, email: str) -> Optional[Usuario]:
    return self._por_email.get(normalizar_email(email))

def eliminar(self, email: str):
    self._por_email.pop(normalizar_email(email), None)
```

---

## 🔹 Reto 2 — Alias semántico: `usuarios.py`

### 🎯 Objetivo:

Evitar tener que importar desde `modelos.py` directamente, y usar un nombre más intuitivo como `app.usuarios`.

---

### 1. Crea archivo nuevo: `app/usuarios.py`

```python
# app/usuarios.py
from .modelos import Usuario, Admin, Invitado, Moderador

__all__ = ["Usuario", "Admin", "Invitado", "Moderador"]
```

---

### 2. Desde fuera del paquete, ya puedes hacer:

```python
from app.usuarios import Admin
```

---

## 🔹 Reto 3 — Script de prueba real (`main.py`)

### 🎯 Objetivo:

Validar que el paquete funciona correctamente cuando se usa externamente.

---

### 1. Crea archivo raíz: `main.py`

```python
# main.py
from app.usuarios import Admin
from app.repositorio import RepositorioUsuarios

if __name__ == "__main__":
    admin = Admin("Root", "root@corp.com")
    repo = RepositorioUsuarios()
    repo.agregar(admin)

    for u in repo.listar_activos():
        print(u)
```

---

### 2. Ejecuta en consola:

```bash
python main.py
```

### 🟢 Resultado esperado:

```
[ADMIN] Soy Root (root@corp.com)
```

---

# ✅ Conclusión

Con estos 3 retos:

| Reto | Qué refuerza                             |
| ---- | ---------------------------------------- |
| 1    | Reutilización de lógica + DRY            |
| 2    | Facilidad de imports y fachada semántica |
| 3    | Validación del uso externo del paquete   |
