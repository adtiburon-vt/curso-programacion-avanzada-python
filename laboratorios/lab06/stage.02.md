# 🔹 Fase 2 — `unittest` básico: casos y aserciones

### 🎯 Objetivo

Convertir las comprobaciones manuales de `scratch.py` en **tests automatizados** con `unittest`, separados por módulos (`modelos` y `repositorio`), ejecutables con un solo comando.

---

## 🧱 Scaffold de tests

Estructura recomendada (añade la carpeta `tests/`):

```
lab6_testing/
├─ app/
│  ├─ __init__.py
│  ├─ modelos.py
│  ├─ repositorio.py
│  └─ utils.py
└─ tests/
   ├─ __init__.py
   ├─ test_modelos.py
   └─ test_repositorio.py
```

> `tests/__init__.py` puede estar vacío (sirve para que Python lo trate como paquete).

---

## 🧪 tests/test\_modelos.py

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

    def test_password_ok_y_ko(self):
        u = Usuario("Ana", "ana@test.com")
        u.set_password("secreta1")
        self.assertTrue(u.check_password("secreta1"))
        self.assertFalse(u.check_password("otra"))

class TestRoles(unittest.TestCase):
    def test_admin_incluye_borrar(self):
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

---

## 🧪 tests/test\_repositorio.py

```python
import unittest
from app.modelos import Usuario
from app.repositorio import RepositorioUsuarios

class TestRepositorioUsuarios(unittest.TestCase):
    def test_agregar_y_obtener(self):
        repo = RepositorioUsuarios()
        u = Usuario("Ana", "ana@test.com")
        repo.agregar(u)
        self.assertIs(repo.obtener_por_email("ana@test.com"), u)

    def test_bloquea_duplicados_por_email(self):
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

---

## ▶️ Cómo ejecutar

Desde la raíz del proyecto:

```bash
python -m unittest discover -s tests
```

* Para ejecutar un archivo concreto:

  ```bash
  python -m unittest tests/test_modelos.py
  ```
* Para ejecutar un solo test (por nombre):

  ```bash
  python -m unittest -k moderador_nivel2_si_borrar
  ```

---

## ✅ Criterios de aceptación

* Todos los tests pasan en verde.
* Un email inválido **lanza `ValueError`**.
* El repositorio **bloquea duplicados**, **elimina** sin errores y **lista** solo activos.
* Los permisos de `Admin` y `Moderador` coinciden con lo definido (nivel 1 sin “borrar”, nivel 2 con “borrar”).

---

## 🔥 Extensiones sugeridas (opcionales)

1. **Casos borde de email**
   Añade asserts para `"@x"`, `"x@"`, espacios alrededor, mayúsculas → deben normalizarse o fallar según tu `validar_email`.

2. **Normalización en repo**
   Testea `obtener_por_email("  ANA@TEST.COM  ")` → debe encontrar a `ana@test.com`.
   Si falla, lo arreglamos en **Fase 3**.

3. **Contador de instancias**
   Test que `Usuario.contador` aumenta (y quizá se resetea en `tearDown` si lo tocas).