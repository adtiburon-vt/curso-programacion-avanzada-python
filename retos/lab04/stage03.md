# ✅ Resolución paso a paso — Mixins y MRO

---

## 🔹 Reto 1 — `NotificadorMixin` y `AdminFull`

### 🎯 Objetivo:

Crear un mixin que añada comportamiento **independiente** (no ligado al ciclo de vida de usuario) y combinarlo con otros mixins.

---

### 1. Añade en `app/modelos.py`:

```python
class NotificadorMixin:
    def enviar_email(self, asunto: str, cuerpo: str) -> None:
        print(f"[EMAIL a {self.email}] {asunto}: {cuerpo}")
```

---

### 2. Crea la clase `AdminFull`:

```python
class AdminFull(NotificadorMixin, LoggerMixin, Admin):
    pass
```

---

### 3. Prueba en `main.py`:

```python
from app.modelos import AdminFull

if __name__ == "__main__":
    af = AdminFull("Alice", "alice@corp.com")
    af.activar()  # logs antes y después
    af.enviar_email("Hola", "Bienvenida a la plataforma")
```

---

### ✅ Resultado esperado:

```
[ts] [AdminFull] <alice@corp.com> Activando usuario…
[ts] [AdminFull] <alice@corp.com> Usuario activado
[EMAIL a alice@corp.com] Hola: Bienvenida a la plataforma
```

---

## 🔹 Reto 2 — Cambiar el orden de los mixins

### 🎯 Objetivo:

Visualizar cómo el orden de herencia afecta la ejecución de `super()` y el MRO.

---

### 1. Cambia la definición de `AdminConLogger`:

```python
class AdminConLogger(Admin, LoggerMixin):
    pass
```

---

### 2. En `main.py`, imprime el MRO:

```python
from app.modelos import AdminConLogger

print("MRO:", AdminConLogger.mro())
```

---

### 3. Ejecuta el método `activar()`:

```python
a = AdminConLogger("Root", "root@corp.com")
a.activar()
```

---

### ✅ Resultado esperado:

* El `LoggerMixin.activar()` **no se ejecuta**, porque está después de `Admin` en el MRO.
* El MRO muestra:

  ```
  [<class 'AdminConLogger'>, <class 'Admin'>, <class 'Usuario'>, ..., <class 'LoggerMixin'>, object]
  ```

---

## 🔹 Reto 3 — `AuditoriaMixin` con estado

### 🎯 Objetivo:

Practicar **inicialización cooperativa** y gestión de estado en mixins.

---

### 1. Añade en `app/modelos.py`:

```python
class AuditoriaMixin:
    def __init__(self):
        self._audit = []
        super().__init__()

    def auditar(self, evento: str):
        self._audit.append(evento)

    def mostrar_auditoria(self):
        return self._audit
```

---

### 2. Crea la clase combinada:

```python
class AdminAuditable(AuditoriaMixin, Admin):
    def __init__(self, nombre: str, email: str, activo: bool = True):
        super().__init__(nombre, email, activo=activo)
```

> ⚠️ Importante: `Admin` y `Usuario` también deben llamar a `super().__init__()` si no lo hacían. En `Usuario.__init__`, cambia:

```python
def __init__(...):
    ...
```

por:

```python
def __init__(...):
    super().__init__()
    ...
```

---

### 3. Prueba en `main.py`:

```python
from app.modelos import AdminAuditable

aa = AdminAuditable("Eva", "eva@corp.com")
aa.auditar("Creado")
aa.activar()
aa.auditar("Activado")
print("Auditoría:", aa.mostrar_auditoria())
```

---

### ✅ Resultado esperado:

```
Auditoría: ['Creado', 'Activado']
```