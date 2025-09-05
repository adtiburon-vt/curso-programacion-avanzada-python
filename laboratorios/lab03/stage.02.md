# 🔹 Fase 2: Encapsulación y validación con `@property`

### 🎯 Objetivo

Robustecer el modelo `Usuario` con **encapsulación** y **validaciones**:

* `email` como propiedad validada.
* `rol` con control de valores permitidos.
* Gestión mínima de contraseña privada.
* Constructor alternativo `desde_dict`.

---

## 🧱 Scaffold (partiendo de tu Fase 1)

Edita `app/modelos.py` y sustituye la clase `Usuario` por esta versión ampliada:

```python
# app/modelos.py
from __future__ import annotations

class Usuario:
    contador = 0
    ROLES_VALIDOS = {"usuario", "admin", "invitado"}

    def __init__(self, nombre: str, email: str, rol: str = "usuario", activo: bool = True):
        self.nombre = nombre
        # Encapsulados
        self._email: str | None = None
        self.email = email  # dispara setter (valida y normaliza)
        self._rol: str | None = None
        self.rol = rol      # dispara setter (valida)
        self.activo = activo
        # Privado (name mangling)
        self.__password_hash: str | None = None

        Usuario.contador += 1

    # ------------------ Representación y básicos ------------------
    def presentarse(self) -> str:
        return f"Soy {self.nombre} ({self.email})"

    def activar(self) -> None: self.activo = True
    def desactivar(self) -> None: self.activo = False

    def __str__(self) -> str:
        estado = "activo" if self.activo else "inactivo"
        return f"{self.nombre} <{self.email}> ({self.rol}) [{estado}]"

    def __repr__(self) -> str:
        return (f"Usuario(nombre={self.nombre!r}, email={self.email!r}, "
                f"rol={self.rol!r}, activo={self.activo!r})")

    # ------------------ Email (propiedad) ------------------
    @property
    def email(self) -> str:
        return self._email or ""

    @email.setter
    def email(self, value: str) -> None:
        v = (value or "").strip().lower()
        if "@" not in v or v.startswith("@") or v.endswith("@"):
            raise ValueError(f"Email inválido: {value!r}")
        self._email = v

    # ------------------ Rol (propiedad) ------------------
    @property
    def rol(self) -> str:
        return self._rol or "usuario"

    @rol.setter
    def rol(self, value: str) -> None:
        v = (value or "").strip().lower()
        if v not in self.ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {value!r}. Válidos: {sorted(self.ROLES_VALIDOS)}")
        self._rol = v

    # ------------------ Password (privado simulado) ------------------
    def set_password(self, p: str) -> None:
        if not p or len(p) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        # Simulación: NO uses esto en producción
        self.__password_hash = f"hash::{p}"

    def check_password(self, p: str) -> bool:
        return self.__password_hash == f"hash::{p}"

    # ------------------ Constructores alternativos ------------------
    @classmethod
    def desde_dict(cls, datos: dict) -> "Usuario":
        """
        Espera claves: nombre, email, rol?, activo?
        """
        return cls(
            nombre=datos.get("nombre", ""),
            email=datos.get("email", ""),
            rol=datos.get("rol", "usuario"),
            activo=bool(datos.get("activo", True)),
        )
```

Y actualiza `main.py` para probar las nuevas capacidades:

```python
# main.py
from app.modelos import Usuario

if __name__ == "__main__":
    # Caso feliz
    u = Usuario("Ana", "ANA@Test.com", rol="admin")
    u.set_password("secreta!")
    print(u.presentarse(), u.rol, u.check_password("secreta!"))

    # Email inválido
    try:
        u.email = "sin-arroba"
    except ValueError as e:
        print("Email inválido OK:", e)

    # Rol inválido
    try:
        u.rol = "superuser"
    except ValueError as e:
        print("Rol inválido OK:", e)

    # desde_dict
    datos = {"nombre": "Luis", "email": "luis@test.com", "rol": "invitado", "activo": False}
    u2 = Usuario.desde_dict(datos)
    print(repr(u2))

    # Password mínima
    try:
        u2.set_password("123")
    except ValueError as e:
        print("Password corta OK:", e)
```

---

## 🧭 Pasos

1. **Propiedad `email`**

   * Normaliza a **lower** y **strip**.
   * Valida presencia de `@` (regla simple para el lab).

2. **Propiedad `rol`**

   * Solo acepta valores en `ROLES_VALIDOS`.
   * Normaliza a minúsculas.

3. **Contraseña privada**

   * Guarda un “hash” simulado en `__password_hash`.
   * `set_password` valida longitud mínima.
   * `check_password` compara.

4. **Constructor alternativo**

   * `Usuario.desde_dict(datos)` para facilitar carga desde estructuras.

5. **Pruebas manuales**

   * Ejecuta `python main.py` y verifica los prints y excepciones esperadas.

---

## ✅ Validación (criterios de aceptación)

* `Usuario("Ana", "ANA@Test.com").email == "ana@test.com"`
* `u.rol = "admin"` funciona; `u.rol = "root"` lanza `ValueError`.
* `u.set_password("secreta!")` y `u.check_password("secreta!")` → `True`.
* `Usuario.desde_dict({...})` crea un usuario con los campos normalizados.
* Asignar `u.email = "x@"` o `"@x"` → `ValueError`.

---

## 🔥 Reto (opcional)

1. **Validador de email mejorado (solo lab)**
   Usa una regex pragmática y muévela a un módulo `utils.py` para reutilizar.

2. **`__eq__` por email**
   Dos `Usuario` son iguales si su `email` normalizado coincide. Recuerda también redefinir `__hash__` si quieres usarlos en sets/dicts.

3. **Roles extensibles**
   Permite ampliar `ROLES_VALIDOS` con un `@classmethod add_rol(cls, rol)` que valide formato.

---

## 🧹 Buenas prácticas

* Propiedades (`@property`) para **encapsular y validar** sin cambiar API pública.
* Mantén la **normalización** en el setter (fuente de la verdad).
* No expongas el estado de contraseña; solo **métodos** para set/check.
* Lanza **excepciones específicas** (`ValueError`) con mensajes útiles.