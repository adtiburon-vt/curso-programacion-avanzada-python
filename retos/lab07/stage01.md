
# 🔥 Reto 1 — Añadir el nombre del hilo en la impresión

---

### 🎯 Objetivo

Ver en pantalla qué hilo está procesando qué archivo, para observar mejor la concurrencia.

---

### 🧠 ¿Qué necesito?

* Cada hilo ya tiene un nombre: `name=f"hilo-{a.stem}"` al crearlos en `main.py`.
* En la función `tarea_contar()`, puedo acceder al hilo actual con:

```python
import threading
threading.current_thread().name
```

---

### 🛠 Paso a paso

1. Voy a `app/procesador.py`.
2. En la función `tarea_contar()`, añado la obtención del nombre del hilo:

```python
from pathlib import Path
import threading

def tarea_contar(archivo: str | Path) -> None:
    n = contar_lineas(archivo)
    hilo = threading.current_thread().name
    print(f"[{hilo}] [{Path(archivo).name}] líneas: {n}")
```

---

### ▶️ Ejecuto

```bash
python main.py
```

### ✅ Resultado esperado:

```
[hilo-archivo2] [archivo2.txt] líneas: 18
[hilo-archivo1] [archivo1.txt] líneas: 25
[hilo-archivo3] [archivo3.txt] líneas: 9
✔ Procesamiento concurrente finalizado
```

---

### ✔ Confirmación

* Puedo ver qué hilo está activo en cada `print`.
* No he modificado la lógica de procesamiento, solo la salida.
* Muy útil para visualizar la concurrencia sin herramientas externas.

---

# 🔥 Reto 2 — Medir el tiempo total de ejecución

---

### 🎯 Objetivo

Medir cuánto tarda el programa completo en procesar todos los archivos.

---

### 🧠 ¿Qué necesito?

* Marcar el tiempo al inicio y al final de `main()`.
* Usar `time.time()` (o `time.perf_counter()` si quiero más precisión).
* Restar los dos y mostrar el resultado.

---

### 🛠 Paso a paso

1. En `main.py`, importo `time`:

```python
import time
```

2. En la función `main()`, añado:

```python
start = time.time()
# ... código de hilos ...
end = time.time()
print(f"⏱️ Duración total: {end - start:.2f} segundos")
```

---

### ▶️ Ejecuto

```bash
python main.py
```

### ✅ Resultado esperado (por ejemplo):

```
[hilo-archivo2] [archivo2.txt] líneas: 18
[hilo-archivo3] [archivo3.txt] líneas: 9
[hilo-archivo1] [archivo1.txt] líneas: 25
✔ Procesamiento concurrente finalizado
⏱️ Duración total: 0.01 segundos
```

---

### ✔ Confirmación

* Mido todo el tiempo desde antes de lanzar los hilos hasta después del `join()`.
* Es útil para comparar luego con una versión secuencial.

---

# 🔥 Reto 3 — Cambiar conteo de líneas por conteo de palabras

---

### 🎯 Objetivo

Modificar la lógica de procesamiento para contar **palabras** en lugar de líneas.

---

### 🧠 ¿Qué cambio?

* En lugar de hacer `sum(1 for _ in f)`, quiero hacer:

```python
sum(len(line.split()) for line in f)
```

---

### 🛠 Paso a paso

1. Voy a `app/procesador.py`.
2. En la función `contar_lineas()`, renombro la función a `contar_palabras()` (opcional).
3. Cambio la implementación:

```python
def contar_palabras(path: str | Path) -> int:
    p = Path(path)
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        return sum(len(line.split()) for line in f)
```

4. Actualizo `tarea_contar()` para que llame a `contar_palabras()`:

```python
def tarea_contar(archivo: str | Path) -> None:
    n = contar_palabras(archivo)
    hilo = threading.current_thread().name
    print(f"[{hilo}] [{Path(archivo).name}] palabras: {n}")
```

---

### ▶️ Ejecuto

```bash
python main.py
```

### ✅ Resultado esperado:

```
[hilo-archivo2] [archivo2.txt] palabras: 234
[hilo-archivo3] [archivo3.txt] palabras: 112
[hilo-archivo1] [archivo1.txt] palabras: 341
✔ Procesamiento concurrente finalizado
⏱️ Duración total: 0.01 segundos
```

---

### ✔ Confirmación

* He cambiado solo **la lógica de cálculo**, manteniendo intacta la estructura de hilos.
* La salida refleja correctamente el nuevo objetivo.

---

## ✅ Conclusión

Con solo **3 modificaciones mínimas**, he:

* Visualizado mejor la ejecución concurrente (`current_thread().name`).
* Medido el rendimiento global con `time`.
* Adaptado el procesamiento a una métrica diferente (palabras).

Todo ello sin romper la arquitectura ni complicar el código.