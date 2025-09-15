# 🩹 Parche — Nueva subclase `Moderador`

**En `app/modelos.py`**, al final del archivo (debajo de `Invitado`):

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

    def __str__(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"[MODERADOR-N{self.nivel}] {self.nombre} <{self.email}> [{estado}]"
```

---

# 🧪 Checks exprés

**En `main.py`** añade al bloque de pruebas:

```python
from app.modelos import Moderador

m1 = Moderador("Lucía", "lucia@test.com")
m2 = Moderador("Carlos", "carlos@test.com", nivel=2)

print(m1)                       # [MODERADOR-N1] Lucía <lucia@test.com> [activo]
print("Permisos:", m1.permisos())  # ['ver', 'editar']

print(m2)                       # [MODERADOR-N2] Carlos <carlos@test.com> [activo]
print("Permisos:", m2.permisos())  # ['ver', 'editar', 'borrar']
```

---

# 🔥 Retos opcionales (sencillos)

1. **Validar nivel**
   Dentro de `__init__`, antes de `self.nivel = nivel`:

   ```python
   if not isinstance(nivel, int) or nivel < 1:
       raise ValueError("El nivel de moderador debe ser un entero >= 1")
   ```

2. **Método `ascender`**

   ```python
   def ascender(self) -> list[str]:
       self.nivel += 1
       return self.permisos()
   ```

3. **Factory de conveniencia**

   ```python
   @classmethod
   def basico(cls, nombre: str, email: str) -> "Moderador":
       return cls(nombre, email, nivel=1)
   ```