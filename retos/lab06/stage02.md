# ✅ Reto 1 — Escribe tus primeros tests con `assertEqual` y `assertIn`

---

### 🎯 Objetivo

Transformar una comprobación con `print()` en un **test automatizado básico** que use `assertEqual()` y `assertIn()`.

---

### 🧠 ¿Qué quiero comprobar?

1. Que cuando creo un usuario, el método `.presentarse()` devuelve el texto correcto.
2. Que un admin tiene el permiso `"borrar"`.

Ya lo había hecho así en `scratch.py`:

```python
print(u.presentarse())  # Esperado: "Soy Ana (ana@test.com)"
print("borrar" in a.permisos())  # Esperado: True
```

---

### 🛠 Paso a paso

1. Creo el archivo `tests/test_modelos.py`.
2. Importo `unittest` y mis clases:

```python
import unittest
from app.modelos import Usuario, Admin
```

3. Escribo mi primera clase de test:

```python
class TestUsuario(unittest.TestCase):
    def test_presentarse(self):
        u = Usuario("Ana", "ana@test.com")
        self.assertEqual(u.presentarse(), "Soy Ana (ana@test.com)")
```

4. Añado el test del admin:

```python
class TestRoles(unittest.TestCase):
    def test_admin_tiene_permiso_borrar(self):
        a = Admin("Root", "root@corp.com")
        self.assertIn("borrar", a.permisos())
```

---

### ✅ Qué confirmo

* Que los métodos funcionan como espero.
* Que ya no dependo de `print()` para comprobar cosas.
* Que `unittest` puede comparar strings (`assertEqual`) y listas (`assertIn`).

---

### ▶️ Ejecución

```bash
python -m unittest tests/test_modelos.py
```

✔️ Veo que los tests pasan en verde.

---

# ✅ Reto 2 — Comprueba que se lanzan errores esperados

---

### 🎯 Objetivo

Escribir **tests negativos**: comprobar que ciertos errores se lanzan como deben.

---

### 🧠 ¿Qué errores quiero probar?

1. Crear un usuario con un email inválido (`"sin-arroba"`).
2. Crear un moderador con nivel inválido (`nivel=0`).

Esto ya lo probé manualmente en la Fase 1:

```python
try:
    Usuario("Luis", "sin-arroba")
except ValueError:
    ...
```

Ahora lo quiero transformar en `unittest`.

---

### 🛠 Paso a paso

1. En `tests/test_modelos.py`, añado un nuevo método a `TestUsuario`:

```python
def test_email_invalido_lanza_error(self):
    with self.assertRaises(ValueError):
        Usuario("Luis", "sin-arroba")
```

2. En `TestRoles`, añado:

```python
def test_moderador_con_nivel_0_lanza_error(self):
    from app.modelos import Moderador
    with self.assertRaises(ValueError):
        Moderador("Lucía", "lucia@test.com", nivel=0)
```

---

### ✅ Qué confirmo

* Que estoy manejando correctamente **comportamientos inválidos**.
* Que no se rompe el programa cuando algo falla: el error se captura y el test pasa.
* Que `assertRaises()` sirve para confirmar que la lógica defensiva está funcionando.

---

### ▶️ Ejecución

```bash
python -m unittest tests/test_modelos.py
```

✔️ Todos los tests siguen pasando.

---

# ✅ Reto 3 — Comprueba las operaciones básicas del repositorio

---

### 🎯 Objetivo

Probar que puedo usar el repositorio para **guardar y recuperar** un usuario.

---

### 🧠 ¿Qué me interesa validar?

Ya hice esto en `scratch.py`:

```python
repo = RepositorioUsuarios()
repo.agregar(u)
repo.obtener_por_email("ana@test.com")  # Devuelve u
```

Quiero convertirlo en un test que use `assertIs()` para comprobar que es **el mismo objeto**.

---

### 🛠 Paso a paso

1. Creo el archivo `tests/test_repositorio.py`.
2. Importo lo necesario:

```python
import unittest
from app.modelos import Usuario
from app.repositorio import RepositorioUsuarios
```

3. Escribo el test:

```python
class TestRepositorioUsuarios(unittest.TestCase):
    def test_agregar_y_obtener_usuario(self):
        repo = RepositorioUsuarios()
        u = Usuario("Ana", "ana@test.com")
        repo.agregar(u)
        self.assertIs(repo.obtener_por_email("ana@test.com"), u)
```

✔️ `assertIs()` sirve aquí porque quiero asegurarme de que el objeto devuelto **es el mismo que agregué**, no solo que “se parece”.

---

### ✅ Qué confirmo

* Que el repositorio almacena correctamente los usuarios.
* Que la función `obtener_por_email()` recupera lo esperado.
* Que usar `assertIs()` me permite verificar identidad real de objetos.

---

### ▶️ Ejecución

```bash
python -m unittest tests/test_repositorio.py
```

✔️ Test verde, todo correcto.

---

## ✅ Conclusión final de la Fase 2

He aprendido a:

* Escribir **tests unitarios con `unittest`** usando `assertEqual`, `assertIn`, `assertIs`, `assertRaises`.
* **Organizar mis tests por archivo y clase**.
* Ejecutarlos de forma controlada desde consola.
* Convertir comprobaciones manuales en aserciones automatizadas.