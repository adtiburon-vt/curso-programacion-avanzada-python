# 🔥 Reto 1 — Contador global de archivos procesados

---

### 🎯 Objetivo

Llevar la cuenta de cuántos archivos han sido procesados correctamente, de forma segura (protegido con `lock`).

---

### 🔍 Valoramos

* Ya existe un diccionario compartido (`resultados`) protegido con `lock`.
* Queremos aprovechar el mismo `lock` para proteger un segundo recurso: un contador tipo `{"ok": 0}`.
* Así evitamos condiciones de carrera al incrementar.

---

### 🛠 Paso a paso

1. En `main.py`, declaro el contador:

```python
contador = {"ok": 0}
```

2. Paso el contador a cada hilo:

```python
t = threading.Thread(
    target=tarea_contar_guardando,
    args=(a, resultados, lock, contador),
    name=f"hilo-{a.stem}",
)
```

3. En `app/procesador.py`, actualizo la firma de la función:

```python
def tarea_contar_guardando(
    archivo: str | Path,
    resultados: MutableMapping[str, int],
    lock: threading.Lock,
    contador: MutableMapping[str, int],
) -> None:
```

4. Dentro del `with lock:`, incremento el contador:

```python
with lock:
    resultados[nombre] = n
    contador["ok"] += 1
```

5. En `main.py`, al final:

```python
print(f"✔ Archivos procesados: {contador['ok']} de {len(archivos)}")
```

---

### ▶️ Ejecución

```bash
python main.py
```

✔️ La salida incluye:

```
✔ Archivos procesados: 3 de 3
```

---

# 🔥 Reto 2 — Control de errores: archivo ilegible

---

### 🎯 Objetivo

Manejar errores al leer archivos sin detener el resto de hilos. En lugar de romper, guardar `-1` como valor.

---

### 🔍 Valoramos

* En un entorno concurrente, si un hilo falla, no debe afectar a los demás.
* Podemos capturar excepciones alrededor de `contar_lineas()` y marcar el error con `-1` en el diccionario de resultados.
* Imprimiremos un mensaje informativo sin romper el flujo.

---

### 🛠 Paso a paso

1. En `tarea_contar_guardando()`, uso un `try/except`:

```python
try:
    n = contar_lineas(archivo)
except Exception as e:
    n = -1
    print(f"[{nombre}] ERROR al contar líneas: {e}")
```

2. El resto queda igual, guardando `n` y actualizando el contador bajo `lock`.

---

### ▶️ Ejecución

* Simulo un fallo renombrando un archivo o quitándole permisos.
* El programa no se rompe; imprime:

```
[archivoX.txt] ERROR al contar líneas: ...
```

✔️ Resultado consolidado muestra `archivoX.txt: -1`.

---

# 🔥 Reto 3 — Mostrar progreso: “X de Y archivos procesados”

---

### 🎯 Objetivo

Desde cada hilo, mostrar cuántos archivos han sido procesados hasta ese momento.

---

### 🔍 Valoramos

* Ya tenemos un contador `contador["ok"]`, actualizado bajo `lock`.
* Si también pasamos el número total de archivos (`total`), podemos imprimir el progreso en cada hilo.
* Esto ayuda a visualizar el avance del procesamiento concurrente de forma clara.

---

### 🛠 Paso a paso

1. En `main.py`, calculo el total:

```python
total = len(archivos)
```

2. Paso `total` a cada hilo:

```python
args=(a, resultados, lock, contador, total)
```

3. En `tarea_contar_guardando()`, añado el parámetro:

```python
def tarea_contar_guardando(..., total: int) -> None:
```

4. Dentro del `with lock:`, después de incrementar:

```python
progreso = contador["ok"]
print(f"[{nombre}] líneas: {n} (guardado) — Progreso: {progreso} de {total}")
```

---

### ▶️ Ejecución

```bash
python main.py
```

✔️ Salida ejemplo:

```
[archivo2.txt] líneas: 15 (guardado) — Progreso: 1 de 3
[archivo3.txt] líneas: 9 (guardado) — Progreso: 2 de 3
[archivo1.txt] líneas: 27 (guardado) — Progreso: 3 de 3
```

---

## ✅ Conclusión

Con estos tres retos he reforzado los principios clave de esta fase:

* ✅ Protección de **múltiples recursos compartidos** con un solo `Lock`.
* ✅ Manejo robusto de errores por hilo.
* ✅ Visualización segura del **progreso concurrente**.