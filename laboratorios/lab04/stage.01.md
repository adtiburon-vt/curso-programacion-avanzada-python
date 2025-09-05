# 🔹 Fase 1: Subclase `Moderador` (herencia simple)

### 🎯 Objetivo

Crear una subclase `Moderador` que herede de `Usuario`, añadiendo un atributo extra `nivel` y especializando el método `permisos()` en función de ese nivel. Practicaremos **herencia simple** y el uso de **`super()`**.

---

### 🧱 Scaffold

Edita `app/modelos.py` (basado en el Lab 3) y añade al final:

```python
# app/modelos.py
from .modelos import Usuario  # si estás en varios archivos, si no omite esta línea

class Moderador(Usuario):
    def __init__(self, nombre: str, email: str, nivel: int = 1, activo: bool = True):
        # Llama al constructor de Usuario
        super().__init__(nombre, email, rol="moderador", activo=activo)
        self.nivel = nivel

    def permisos(self) -> list[str]:
        """
        Nivel 1: puede 'ver' y 'editar'
        Nivel 2 o superior: puede 'ver', 'editar' y 'borrar'
        """
        base = ["ver", "editar"]
        if self.nivel >= 2:
            base.append("borrar")
        return base

    def __str__(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"[MODERADOR-N{self.nivel}] {self.nombre} <{self.email}> [{estado}]"
```

Y en `main.py` prueba la nueva clase:

```python
# main.py
from app.modelos import Moderador

if __name__ == "__main__":
    m1 = Moderador("Lucía", "lucia@test.com")          # nivel 1 por defecto
    m2 = Moderador("Carlos", "carlos@test.com", nivel=2)

    print(m1)
    print("Permisos:", m1.permisos())

    print(m2)
    print("Permisos:", m2.permisos())
```

---

### 🧭 Pasos

1. **Definir `Moderador` como subclase de `Usuario`.**
2. Usar `super().__init__()` para inicializar nombre, email, rol y activo.

   * Forzar `rol="moderador"` al llamar a la superclase.
3. Añadir un atributo nuevo `nivel` con valor por defecto `1`.
4. Especializar `permisos()`:

   * Nivel 1 → `"ver", "editar"`.
   * Nivel ≥2 → añade `"borrar"`.
5. Redefinir `__str__` para que muestre el rol y nivel del moderador.
6. Probar en `main.py` creando instancias con distintos niveles.

---

### ✅ Validación

* `Moderador("Lucía","lucia@test.com").permisos()` → `["ver", "editar"]`.
* `Moderador("Carlos","carlos@test.com", nivel=2).permisos()` → `["ver", "editar", "borrar"]`.
* `print(m1)` muestra:

  ```
  [MODERADOR-N1] Lucía <lucia@test.com> [activo]
  ```

---

### 🔥 Reto (opcional)

1. Haz que el nivel se valide: solo acepte enteros `>=1`, de lo contrario lanza `ValueError`.
2. Añade un método `ascender()` que incremente el nivel en 1 y devuelva los nuevos permisos.
3. Crea un método de clase `Moderador.basico(nombre,email)` que cree un moderador de nivel 1 preconfigurado.
