# 🔹 Fase 3: Herencia múltiple con Mixins (y MRO)

### 🎯 Objetivo

Introducir **mixins** para sumar capacidades transversales sin tocar la jerarquía principal, y comprobar el **MRO** para entender cómo fluye `super()` con herencia múltiple.

---

## 🧱 Scaffold (añade a tu proyecto)

### 1) `app/modelos.py` — crea un `LoggerMixin` y una variante de `Admin` que lo use

```python
# app/modelos.py (añadir al final)
from datetime import datetime
from typing import Any

class LoggerMixin:
    """Mixin de logging simple. Supone que la clase hija tiene .email y .__class__.__name__."""
    def log_evento(self, msg: str, **context: Any) -> None:
        ts = datetime.now().isoformat(timespec="seconds")
        who = getattr(self, "email", "desconocido")
        extra = f" {context}" if context else ""
        print(f"[{ts}] [{self.__class__.__name__}] <{who}> {msg}{extra}")

    # Ejemplo de método que coopera con super() para cadenas MRO
    def activar(self) -> None:
        self.log_evento("Activando usuario…")
        super().activar()  # delega al siguiente en el MRO
        self.log_evento("Usuario activado")

class AdminConLogger(LoggerMixin, Admin):
    """Admin con capacidades de logging vía mixin."""
    # hereda todo; si quieres, puedes extender presentarse/activar usando super()
    def presentarse(self) -> str:
        base = super().presentarse()
        self.log_evento("presentarse() invocado")
        return base
```

> Nota: el **orden** importa. Ponemos `LoggerMixin` **antes** de `Admin` para que sus métodos (como `activar`) se ejecuten antes y luego llamen a `super()`.

### 2) `main.py` — demo rápida y MRO

```python
# main.py
from app.modelos import AdminConLogger, Moderador

if __name__ == "__main__":
    a = AdminConLogger("Root", "root@corp.com")
    print(a.presentarse())           # debería loguear la llamada
    a.activar()                      # logs antes y después gracias al mixin

    m = Moderador("Lucía", "lucia@test.com", nivel=2, activo=False)
    print(m)                         # [MODERADOR-N2] ...
    m.activar()                      # (no loguea, no hereda del mixin)

    print("MRO AdminConLogger:", AdminConLogger.mro())
```

---

## 🧭 Pasos

1. **Define el mixin** `LoggerMixin` con un método utilitario `log_evento`.
2. **Sobrescribe `activar` en el mixin** para **cooperar** con `super()` (patrón cooperativo): log antes y después, y delega al siguiente en MRO.
3. **Crea `AdminConLogger(LoggerMixin, Admin)`** para añadir logging a un Admin sin tocar `Admin`.
4. **Prueba el flujo**: `presentarse()` y `activar()` deberían mostrar logs.
5. **Imprime el MRO** con `AdminConLogger.mro()` y analiza el orden (debe ser `[AdminConLogger, LoggerMixin, Admin, Usuario, BaseUsuario, object]` o similar según tu árbol).

---

## ✅ Criterios de aceptación

* `AdminConLogger("root", "...").presentarse()` produce el texto de `Admin` y loguea la invocación.
* `AdminConLogger(...).activar()` imprime dos logs (antes/después) y deja `activo=True`.
* `Moderador(...).activar()` funciona **sin** logs (no usa el mixin).
* El MRO de `AdminConLogger` muestra al mixin **antes** de `Admin`, confirmando que `super()` en el mixin delega a `Admin.activar()`.


## 🔥 Retos opcionales — Mixins y MRO

---

### 🔹 Reto 1 — Añadir un mixin de notificaciones

Crea un nuevo mixin `NotificadorMixin` con un método:

```python
def enviar_email(self, asunto: str, cuerpo: str) -> None:
    print(f"[EMAIL a {self.email}] {asunto}: {cuerpo}")
```

Luego crea una clase `AdminFull(NotificadorMixin, LoggerMixin, Admin)` que combine ambos mixins.

Prueba que:

* `AdminFull(...).activar()` muestra los logs.
* Puedes llamar a `.enviar_email()` sobre una instancia sin errores.

---

### 🔹 Reto 2 — Cambiar el orden de los mixins y observar qué cambia

Invierte el orden de herencia en `AdminConLogger`:

```python
class AdminConLogger(Admin, LoggerMixin): ...
```

Observa:

* ¿Se siguen mostrando los logs al llamar `activar()`?
* ¿Qué valor tiene `AdminConLogger.mro()` con este nuevo orden?

Explica brevemente por qué ocurre ese cambio.

---

### 🔹 Reto 3 — Auditoría interna cooperativa

Crea un mixin `AuditoriaMixin` que guarde un historial de eventos:

```python
class AuditoriaMixin:
    def __init__(self):
        self._audit = []
        super().__init__()

    def auditar(self, evento: str):
        self._audit.append(evento)
```

Crea una clase `AdminAuditable(AuditoriaMixin, Admin)` y:

* Asegúrate de que `Admin.__init__` se llama correctamente.
* Usa `.auditar("algo")` y comprueba que el historial se guarda en `._audit`.

Este reto requiere usar `super().__init__()` en todos los constructores para que la cadena de inicialización sea completa.


# ✅ Conclusión del Laboratorio 4

**Lo que has construido:**

* **Extensiones** de la jerarquía de usuarios (`Moderador`) con atributos y permisos específicos.
* **Sobrescritura** de métodos reutilizando lógica base mediante **`super()`** (evitando duplicación).
* **Herencia múltiple con mixins** para capacidades transversales (logging), entendiendo el **MRO** y el patrón cooperativo de `super()`.

**Aprendizajes clave:**

* Usa **herencia simple** para **especializar** (nuevos atributos/comportamientos).
* Aplica **`super()`** para extender sin reescribir.
* Emplea **mixins** para **comportamientos ortogonales** (logging, notificaciones, auditoría) sin acoplarlos a la jerarquía principal.
* Comprende el **MRO**: el orden de bases define la cadena de llamadas de `super()`.

