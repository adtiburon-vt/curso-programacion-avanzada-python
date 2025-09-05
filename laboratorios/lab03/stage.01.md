# 🔹 Fase 1: Clase `Usuario` (atributos, métodos y constructores)

### 🎯 Objetivo

Modelar la entidad base **`Usuario`** con datos y comportamiento fundamentales: constructor, atributos y métodos de instancia; además de métodos especiales (`__str__`, `__repr__`) y un **contador de instancias**.

---

### 🧱 Scaffold (estructura mínima)

Crea el directorio y archivos:

```
lab3_sistema_usuarios/
├─ app/
│  ├─ __init__.py
│  └─ modelos.py
└─ main.py
```

**app/**init**.py**

```python
# vacío (permite tratar 'app' como paquete)
```

**app/modelos.py (plantilla inicial)**

```python
class Usuario:
    # atributo de clase (contador de instancias)
    contador = 0

    def __init__(self, nombre: str, email: str, activo: bool = True):
        # TODO: asignar atributos, incrementar contador
        self.nombre = nombre
        self.email = email
        self.activo = activo
        Usuario.contador += 1

    def presentarse(self) -> str:
        # TODO: devolver "Soy {nombre} ({email})"
        return f"Soy {self.nombre} ({self.email})"

    def activar(self) -> None:
        self.activo = True

    def desactivar(self) -> None:
        self.activo = False

    def __str__(self) -> str:
        # TODO: legible para humanos
        estado = "activo" if self.activo else "inactivo"
        return f"{self.nombre} <{self.email}> [{estado}]"

    def __repr__(self) -> str:
        # TODO: representación para debugging
        return (f"Usuario(nombre={self.nombre!r}, email={self.email!r}, "
                f"activo={self.activo!r})")
```

**main.py (pruebas manuales)**

```python
from app.modelos import Usuario

if __name__ == "__main__":
    u1 = Usuario("Ana", "ana@test.com")
    u2 = Usuario("Luis", "luis@test.com", activo=False)
    u3 = Usuario("Eva", "eva@test.com")

    print("Presentaciones:")
    print(u1.presentarse())
    print(u2.presentarse())
    print(u3.presentarse())

    print("\nEstados:")
    print(str(u1))
    print(str(u2))

    print("\nActivar/Desactivar:")
    u2.activar()
    print(str(u2))
    u1.desactivar()
    print(str(u1))

    print("\nContador de instancias:", Usuario.contador)

    print("\nrepr para debugging:")
    print(repr(u3))
```

---

### 🧭 Pasos

1. **Constructor y atributos**

   * Implementa `__init__(self, nombre, email, activo=True)` asignando a `self.nombre`, `self.email`, `self.activo`.
   * Incrementa `Usuario.contador` **cada vez** que se instancia.

2. **Métodos de instancia**

   * `presentarse()` → devuelve `f"Soy {self.nombre} ({self.email})"`.
   * `activar()` / `desactivar()` → cambian `self.activo`.

3. **Métodos especiales**

   * `__str__` con formato legible: `"{nombre} <{email}> [activo|inactivo]"`.
   * `__repr__` orientado a debugging con todos los campos.

4. **Pruebas manuales**

   * Ejecuta `python main.py` y revisa salidas.
   * Crea 2–3 usuarios, cambia estados, verifica `Usuario.contador`.

---

### ✅ Validación (criterios de aceptación)

* **Presentación:**
  `Usuario("Ana","ana@test.com").presentarse()` → `"Soy Ana (ana@test.com)"`.

* **Estados y **str**:**
  Con `activo=True` → `"[activo]"` en `str(u)`.
  Tras `desactivar()` → `"[inactivo]"`.

* **Contador:**
  Crear `u1, u2, u3` debe dejar `Usuario.contador == 3`.

* **repr:**
  `repr(u)` devuelve una cadena tipo
  `"Usuario(nombre='Ana', email='ana@test.com', activo=True)"`.

---

### 🔥 Reto (opcional)

1. **Inmutabilidad parcial del email (F1+)**

   * Añade un método `cambiar_email(nuevo_email)` y **no** permitas asignación directa `u.email = ...` (solo usa el método).
   * *Tip:* empieza a preparar encapsulación para la Fase 2 (propiedades).

2. **Igualdad por email**

   * Implementa `__eq__` comparando por `email` en minúsculas y sin espacios.
   * *Tip:* `return self.email.strip().lower() == other.email.strip().lower()`.

3. **Factory simple**

   * Añade `@classmethod def desde_tupla(cls, t):` que reciba `(nombre, email, activo)`.

---

### 🧹 Buenas prácticas

* **`__str__` ≠ `__repr__`**: el primero, humano; el segundo, debugging.
* No mezcles **lógica de presentación** con **lógica de dominio** (usa `presentarse()` para frases, `__str__` para una vista rápida).
* Evita efectos colaterales en `__repr__`/`__str__` (solo leer, no cambiar estado).
* Mantén el constructor **simple**; las validaciones y encapsulación llegan en la **Fase 2**.