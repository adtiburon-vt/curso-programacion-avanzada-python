# 🧭 Laboratorio 6 — Escribir tests + detección de errores

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 6 (Testing profesional: manuales vs automatizados; `unittest`, `assert`, buenas prácticas)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

Pasar de **pruebas manuales** a **tests automatizados** con `unittest`, detectar y corregir errores reales del proyecto (modelo de usuarios y repositorio), y dejar una **base de testing** repetible.

---

## 📁 Estructura sugerida

```
lab6_testing/
├─ app/                  # reutiliza tu app de Labs 3–5
│  ├─ __init__.py
│  ├─ modelos.py
│  ├─ repositorio.py
│  └─ utils.py
├─ tests/
│  ├─ __init__.py
│  ├─ test_modelos.py
│  └─ test_repositorio.py
└─ README.md
```

> Copia/usa tu paquete `app/` ya creado (Lab 5). Este lab solo añade `tests/`.

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1 — Tests manuales (punto de partida rápido)

**Objetivo:** confirmar comportamiento con ejecuciones manuales para identificar qué debe convertirse en tests.

**Acciones**

* Crea un script `scratch.py` (temporal) con prints:

```python
from app.modelos import Usuario, Admin, Moderador
from app.repositorio import RepositorioUsuarios

u = Usuario("Ana", "ana@test.com")
print(u.presentarse())

a = Admin("Root", "root@corp.com")
print("borrar" in a.permisos())

m = Moderador("Lucía", "lucia@test.com", nivel=1)
print("borrar" in m.permisos())  # debería ser False
```

**Validación**

* Visualiza salidas correctas/incorrectas. Anota supuestos → se transformarán en asserts.

---

### 🔹 Fase 2 — `unittest` básico: casos y aserciones

**Objetivo:** reemplazar pruebas manuales por tests automatizados en `tests/`.

**`tests/test_modelos.py`**

```python
import unittest
from app.modelos import Usuario, Admin, Moderador

class TestUsuario(unittest.TestCase):
    def test_presentarse(self):
        u = Usuario("Ana", "ana@test.com")
        self.assertEqual(u.presentarse(), "Soy Ana (ana@test.com)")

    def test_email_invalido(self):
        with self.assertRaises(ValueError):
            Usuario("Luis", "sin-arroba")

    def test_password(self):
        u = Usuario("Ana", "ana@test.com")
        u.set_password("secreta1")
        self.assertTrue(u.check_password("secreta1"))
        self.assertFalse(u.check_password("otra"))

class TestRoles(unittest.TestCase):
    def test_admin_tiene_borrar(self):
        a = Admin("Root", "root@corp.com")
        self.assertIn("borrar", a.permisos())

    def test_moderador_nivel1_no_borrar(self):
        m = Moderador("Lucía", "lucia@test.com", nivel=1)
        self.assertNotIn("borrar", m.permisos())

    def test_moderador_nivel2_si_borrar(self):
        m = Moderador("Carlos", "carlos@test.com", nivel=2)
        self.assertIn("borrar", m.permisos())

if __name__ == "__main__":
    unittest.main()
```

**`tests/test_repositorio.py`**

```python
import unittest
from app.modelos import Usuario
from app.repositorio import RepositorioUsuarios

class TestRepositorio(unittest.TestCase):
    def test_agregar_obtener(self):
        repo = RepositorioUsuarios()
        u = Usuario("Ana", "ana@test.com")
        repo.agregar(u)
        self.assertIs(repo.obtener_por_email("ana@test.com"), u)

    def test_duplicado_lanza(self):
        repo = RepositorioUsuarios()
        repo.agregar(Usuario("Ana", "ana@test.com"))
        with self.assertRaises(ValueError):
            repo.agregar(Usuario("Ana2", "ana@test.com"))

    def test_eliminar(self):
        repo = RepositorioUsuarios()
        repo.agregar(Usuario("Ana", "ana@test.com"))
        repo.eliminar("ana@test.com")
        self.assertIsNone(repo.obtener_por_email("ana@test.com"))

    def test_listar_activos(self):
        repo = RepositorioUsuarios()
        u1 = Usuario("A", "a@x.com", activo=True)
        u2 = Usuario("B", "b@x.com", activo=False)
        repo.agregar(u1); repo.agregar(u2)
        self.assertEqual([u.email for u in repo.listar_activos()], ["a@x.com"])

if __name__ == "__main__":
    unittest.main()
```

**Ejecución**

```bash
python -m unittest discover -s tests
```

**Criterios de aceptación**

* Todos los tests pasan (verde).
* Errores levantan `ValueError` cuando corresponde.

---

### 🔹 Fase 3 — Detección y corrección de errores (debugging guiado por tests)

**Objetivo:** usar tests para **descubrir** y **arreglar** defectos reales (TDD inverso).

**Propuestas de “bugs” a cazar**

1. **Normalización de email en el repositorio**

   * Si `obtener_por_email(" ANA@TEST.COM ")` no encuentra a `ana@test.com`, corrige el repositorio: normaliza email de entrada (`strip().lower()`).

2. **Validación de `nivel` en `Moderador`**

   * Si permite `nivel=0` o no entero, añade setter o validación en `__init__` y prueba:

   ```python
   with self.assertRaises(ValueError):
       Moderador("X", "x@x.com", nivel=0)
   ```

3. **Setter de email demasiado laxo**

   * Fortalece `validar_email` (al menos `@` y `.` y no empezar/terminar por `@`). Añade un test que garantice que `"@x"` y `"x@"` fallan.

4. **Borrado idempotente**

   * Asegura que `eliminar(email)` **no** lanza si no existe (y el test lo comprueba).

**Flujo recomendado**

* Escribe el test que falla (rojo) → corrige el código → vuelve a ejecutar (verde).

---

## 🧠 Reflexión final

* ¿Qué ventajas observaste al transformar comprobaciones manuales en tests automatizados?
* ¿Qué parte del diseño se volvió más fácil de cambiar gracias a tener una suite de tests?
* ¿Qué criterios usaste para decidir qué casos “negativos” (errores) cubrir?

---

## ✅ Comprobación de conocimientos

1. Ejecuta `python -m unittest -k presentarse` y filtra solo ese test.
2. Añade un test de **igualdad por email** si implementas `__eq__` en `Usuario`.
3. Escribe un test de **integración**: crea `Admin`+`Moderador`, guárdalos en repo y confirma que el filtrado por activos/rol funciona (puedes añadir un método auxiliar en repo para filtrar por rol).



* **Parametrización (pytest)**: migra `tests/test_modelos.py` a `pytest` con `@pytest.mark.parametrize`.

* **CI/CD**: añade un workflow (GitHub Actions/GitLab CI) que ejecute los tests en cada push.
