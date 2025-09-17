# 🔹 Fase 3 — Detección y corrección de errores (red→green)

## 1) Normalización de email en el repositorio

**Síntoma**: `obtener_por_email("  ANA@TEST.COM  ")` no encuentra a `ana@test.com`.

### 🧪 Test que debe fallar (añade a `tests/test_repositorio.py`)

```python
def test_obtener_normaliza_email_busqueda(self):
    repo = RepositorioUsuarios()
    repo.agregar(Usuario("Ana", "ana@test.com"))
    self.assertIsNotNone(repo.obtener_por_email("  ANA@TEST.COM  "))
```

### ✅ Arreglo en `app/repositorio.py`

```python
def _norm(email: str) -> str:
    return (email or "").strip().lower()

class RepositorioUsuarios:
    def __init__(self):
        self._por_email: dict[str, Usuario] = {}

    def agregar(self, u: Usuario):
        k = _norm(u.email)
        if k in self._por_email:
            raise ValueError(f"Ya existe usuario con email {k}")
        self._por_email[k] = u

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        return self._por_email.get(_norm(email))

    def listar_activos(self) -> list[Usuario]:
        return [u for u in self._por_email.values() if u.activo]

    def eliminar(self, email: str):
        self._por_email.pop(_norm(email), None)

    def buscar(self, predicado: Callable[[Usuario], bool]) -> list[Usuario]:
        return [u for u in self._por_email.values() if predicado(u)]
```

---

## 2) Validación de `nivel` en `Moderador`

**Síntoma**: permite `nivel=0` o valores no enteros.

### 🧪 Test que debe fallar (añade a `tests/test_modelos.py`)

```python
def test_moderador_valida_nivel(self):
    with self.assertRaises(ValueError):
        Moderador("X", "x@x.com", nivel=0)
    with self.assertRaises(ValueError):
        Moderador("Y", "y@y.com", nivel="2")  # tipo incorrecto
```

### ✅ Arreglo en `app/modelos.py` (constructor o property)

```python
class Moderador(Usuario):
    def __init__(self, nombre: str, email: str, nivel: int = 1, activo: bool = True):
        super().__init__(nombre, email, rol="moderador", activo=activo)
        self.nivel = nivel  # usa setter

    @property
    def nivel(self) -> int:
        return self._nivel

    @nivel.setter
    def nivel(self, value: int):
        if not isinstance(value, int) or value < 1:
            raise ValueError("nivel debe ser int >= 1")
        self._nivel = value
```

*(Si ya tenías la validación en `__init__`, conviértelo a propiedad para evitar futuros valores inválidos.)*

---

## 3) Validación de email más estricta

**Síntoma**: se aceptan casos borde como `"@x"` o `"x@"`.

### 🧪 Test que debe fallar (añade a `tests/test_modelos.py`)

```python
def test_email_casos_borde_invalidos(self):
    with self.assertRaises(ValueError): Usuario("Z", "@x")
    with self.assertRaises(ValueError): Usuario("Z", "x@")
    with self.assertRaises(ValueError): Usuario("Z", "  @  ")
```

### ✅ Arreglo en `app/utils.py` y uso en `Usuario.email`

```python
# app/utils.py
def validar_email(email: str) -> bool:
    e = (email or "").strip().lower()
    if "@" not in e or e.startswith("@") or e.endswith("@"):
        return False
    local, _, domain = e.partition("@")
    if "." not in domain:
        return False
    return True
```

(Asegúrate de que el setter de `Usuario.email` llama a `validar_email` y normaliza a `lower().strip()`.)

---

## 4) Idempotencia en `eliminar`

**Síntoma**: `eliminar` lanza si el email no existe.

### 🧪 Test (si no lo tenías ya)

```python
def test_eliminar_idempotente(self):
    repo = RepositorioUsuarios()
    # No añade nada; eliminar no debe lanzar
    try:
        repo.eliminar("no@existe.com")
    except Exception as e:
        self.fail(f"eliminar debe ser idempotente, lanzó {e!r}")
```

### ✅ Arreglo

Ya incluido arriba: `pop(_norm(email), None)` evita excepciones.

---

## 5) (Opcional) Igualdad por email y uso en sets

**Mejora**: considerar `Usuario` igual si comparte email normalizado.

### 🧪 Test opcional

```python
def test_usuario_eq_por_email(self):
    u1 = Usuario("Ana", "ANA@test.com")
    u2 = Usuario("Ana2", "ana@test.com")
    self.assertEqual(u1, u2)
    self.assertEqual(len({u1, u2}), 1)
```

### ✅ Arreglo en `app/modelos.py`

```python
class Usuario(BaseUsuario):
    # ...
    def _email_norm(self) -> str:
        return (self.email or "").strip().lower()

    def __eq__(self, other):
        if not isinstance(other, Usuario):
            return NotImplemented
        return self._email_norm() == other._email_norm()

    def __hash__(self):
        return hash(self._email_norm())
```

---

## ▶️ Ejecuta la batería completa

```bash
python -m unittest discover -s tests
```

Debes pasar a **verde**. Si alguno cae en rojo, revisa el **mensaje del assert** y ajusta el código o el test.

---

## ✅ Checklist de cierre

* [ ] `obtener_por_email` encuentra usuarios con mayúsculas/espacios.
* [ ] `Moderador.nivel` validado (int ≥ 1) como **propiedad**.
* [ ] Emails borde (`"@x"`, `"x@"`, `"@@"`) **rechazados**.
* [ ] `eliminar` es **idempotente**.
* [ ] (Opcional) `Usuario` tiene **igualdad por email** consistente con `__hash__`.

---

Perfecto, gracias por la precisión.

Entonces, resumiendo:

* Lo que planteaste **no son retos**, sino el **núcleo del laboratorio (Fase 3)**, con scaffold y tests **obligatorios**, que el alumno debe copiar, ejecutar y corregir en modo *red → green*.
* Los **retos verdaderos** son los que aparecerían como “🔥 Extra (si te apetece)” o similares.
* Me pediste que limite a **3 retos por stage**, que sean:

  * **muy simples**
  * **iterativos**
  * **centrados en lo tratado** (en este caso: detección y corrección mediante tests automatizados).

---

## ✅ Retos


### 🔥 Reto 1 — ¿Y si el email viene con `None`?

**Objetivo**: proteger el sistema contra entradas nulas accidentales.

🔧 Qué probar:

```python
with self.assertRaises(ValueError):
    Usuario("SinEmail", None)
```

🛠️ Posible arreglo:

* Asegúrate de que `Usuario.email` y `validar_email()` manejan `None` correctamente.
* El helper `_norm()` también debería tolerarlo (`email or ""`).

---

### 🔥 Reto 2 — Eliminar a un usuario dos veces seguidas

**Objetivo**: confirmar que `.eliminar()` es realmente idempotente.

🔧 Qué probar:

```python
repo = RepositorioUsuarios()
repo.agregar(Usuario("Ana", "ana@test.com"))
repo.eliminar("ana@test.com")
repo.eliminar("ana@test.com")  # Esto no debe lanzar error
```

✔️ Ya está arreglado en `.pop(..., None)`, pero el alumno lo valida con el test.

---

### 🔥 Reto 3 — Emails con mayúsculas al crear usuario

**Objetivo**: confirmar que el sistema funciona correctamente incluso si el email original tiene mayúsculas.

🔧 Qué probar:

```python
repo = RepositorioUsuarios()
repo.agregar(Usuario("Ana", "ANA@TEST.COM"))
self.assertIsNotNone(repo.obtener_por_email("ana@test.com"))
```

🛠️ Esto verifica que:

* El email se normaliza al guardar.
* La búsqueda también se normaliza.
* ⚠️ Requiere que `Usuario.email` haga `lower().strip()` en el setter.



---

# ✅ Conclusión del Laboratorio 6 — Escribir tests + detección de errores

**Lo que has hecho en este laboratorio:**

* Partiste de **tests manuales** con `print` (Fase 1) para validar comportamientos básicos.
* Los convertiste en **tests automatizados** con `unittest` (Fase 2), separando `modelos` y `repositorio`.
* Usaste los tests como **herramienta de detección de errores** (Fase 3):

  * Normalización de emails en repositorio.
  * Validación estricta de `nivel` en `Moderador`.
  * Validación más robusta de emails (`@x`, `x@`, etc.).
  * Hiciste `eliminar()` **idempotente**.
  * (Opcional) Añadiste igualdad por email (`__eq__` / `__hash__`).

**Aprendizajes clave:**

* Los tests son más que una comprobación: son un **contrato vivo** del comportamiento esperado.
* **Red → Green**: primero escribir un test que falle, luego corregir el código hasta que pase.
* **Cobertura de errores**: no solo probar casos correctos, también los fallos previstos (`ValueError`, etc.).
* **Mantenibilidad**: con una suite de tests, puedes refactorizar con confianza.

**Preparado para continuar:**

* Ampliar tests a escenarios más amplios (**concurrencia**, **persistencia**).
* Integrar los tests en **CI/CD** (GitHub Actions, GitLab CI).
* Medir **cobertura** (`coverage`) y mejorarla iterativamente.
* Probar otros frameworks como **pytest** para parametrización y fixtures.
