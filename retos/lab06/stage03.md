# 🔥 Reto 1 — Usuario con email `None`

---

### 🎯 Objetivo

Confirmar que **no se permite crear un usuario sin email** (por ejemplo, `None`) y que se lanza `ValueError`.

---

### 🧠 Proceso mental

El email es un campo obligatorio, así que pasar `None` debería lanzar error.

Me pregunto: ¿mi función `validar_email()` lo está manejando? ¿Y el setter del email?

---

### 🧪 Paso 1 — Escribo el test (esperando que falle)

En `tests/test_modelos.py`, añado:

```python
def test_email_none_lanza_error(self):
    with self.assertRaises(ValueError):
        Usuario("SinEmail", None)
```

---

### ▶️ Ejecuto los tests

```bash
python -m unittest tests/test_modelos.py
```

### ❌ Resultado (esperado):

```
TypeError: argument of type 'NoneType' is not iterable
```

🧠 Eso quiere decir que `validar_email()` está intentando usar `.strip()` o `"@" in ...` sobre `None`, y explota.

---

### 🛠️ Paso 2 — Arreglo en `validar_email()`

Voy a `app/utils.py` y refuerzo la función para aceptar `None` como entrada:

```python
def validar_email(email: str) -> bool:
    e = (email or "").strip().lower()
    if "@" not in e or e.startswith("@") or e.endswith("@"):
        return False
    local, _, domain = e.partition("@")
    if "." not in domain:
        return False
    return True
```

Ya que uso `(email or "")`, el código no lanza `TypeError`.

---

### 🛠️ Paso 3 — Confirmo que el setter lo usa

Verifico que en `Usuario.email` se llama a `validar_email()` antes de guardar:

```python
@property
def email(self):
    return self._email

@email.setter
def email(self, valor: str):
    if not validar_email(valor):
        raise ValueError(f"Email inválido: {valor}")
    self._email = valor.strip().lower()
```

🧠 Todo correcto: si el email no es válido, lanza `ValueError`.

---

### ✅ Vuelvo a ejecutar los tests

```bash
python -m unittest tests/test_modelos.py
```

✔️ Test en verde. He validado y corregido un caso borde clásico.

---

# 🔥 Reto 2 — Eliminar a un usuario dos veces

---

### 🎯 Objetivo

Confirmar que **eliminar dos veces el mismo email no lanza error** (comportamiento idempotente).

---

### 🧠 Proceso mental

La primera eliminación debería borrar el usuario.
La segunda no debería lanzar error: simplemente no hacer nada.

---

### 🧪 Paso 1 — Escribo el test

En `tests/test_repositorio.py`, añado:

```python
def test_eliminar_dos_veces_no_lanza(self):
    repo = RepositorioUsuarios()
    repo.agregar(Usuario("Ana", "ana@test.com"))
    repo.eliminar("ana@test.com")
    try:
        repo.eliminar("ana@test.com")  # Segunda vez
    except Exception as e:
        self.fail(f"eliminar dos veces no debería lanzar error: {e!r}")
```

---

### ▶️ Ejecuto los tests

```bash
python -m unittest tests/test_repositorio.py
```

### ❌ Resultado posible si falla:

```
KeyError: 'ana@test.com'
```

---

### 🛠️ Paso 2 — Arreglo en `RepositorioUsuarios.eliminar()`

Voy a `app/repositorio.py` y aseguro que `.pop()` no lance error:

```python
def eliminar(self, email: str):
    self._por_email.pop(_norm(email), None)  # ← devuelve None si no existe
```

🧠 Esto hace que la eliminación sea **idempotente**: no importa si el email está o no.

---

### ✅ Vuelvo a ejecutar los tests

```bash
python -m unittest tests/test_repositorio.py
```

✔️ Verde. Eliminar dos veces ahora es seguro.

---

# 🔥 Reto 3 — Emails con mayúsculas al crear

---

### 🎯 Objetivo

Verificar que **el sistema normaliza emails con mayúsculas** al guardar y buscar usuarios.

---

### 🧠 Proceso mental

Ya normalicé el email en el repositorio, pero... ¿lo hago también cuando creo el usuario?

Si guardo `"ANA@TEST.COM"` pero luego busco `"ana@test.com"`, ¿funciona?

---

### 🧪 Paso 1 — Escribo el test

En `tests/test_repositorio.py`, añado:

```python
def test_agregar_email_mayuscula_y_buscar_minuscula(self):
    repo = RepositorioUsuarios()
    repo.agregar(Usuario("Ana", "ANA@TEST.COM"))
    self.assertIsNotNone(repo.obtener_por_email("ana@test.com"))
```

---

### ▶️ Ejecuto los tests

```bash
python -m unittest tests/test_repositorio.py
```

### ❌ Posible fallo:

```
AssertionError: unexpectedly None
```

🧠 Significa que **al guardar el usuario, el email no se normalizó**.

---

### 🛠️ Paso 2 — Arreglo en el setter de `Usuario.email`

Voy a `modelos.py` y actualizo el setter para normalizar siempre:

```python
@email.setter
def email(self, valor: str):
    if not validar_email(valor):
        raise ValueError(f"Email inválido: {valor}")
    self._email = valor.strip().lower()
```

🧠 Esto garantiza que **todos los emails guardados están normalizados**.

---

### ✅ Vuelvo a ejecutar los tests

```bash
python -m unittest tests/test_repositorio.py
```

✔️ Verde. La búsqueda por email ahora funciona sin importar las mayúsculas.

---

## ✅ Conclusión

En estos tres retos he:

* Identificado errores o inconsistencias reales.
* Escrito un test que los hace fallar.
* Corregido el código hasta que todo pasa en verde.
* Practicado el ciclo completo **Red → Green** de forma segura.

🧠 Lo más valioso: ahora sé que si toco algo... los tests me avisan.
Estoy listo para seguir ampliando la aplicación **sin miedo a romper nada**.