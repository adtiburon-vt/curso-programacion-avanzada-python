# 🧭 Laboratorio 8 — Evitar condiciones de carrera con Lock

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 8 (Multiprocesamiento en Python)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

Aprender a identificar y resolver **condiciones de carrera** en programas multiproceso de Python usando **`multiprocessing.Lock`**, protegiendo tanto **memoria compartida** como **archivos compartidos**.

---

## 📁 Estructura sugerida

```
lab8_multiprocessing/
├─ app/
│  ├─ __init__.py
│  └─ procesos.py     # funciones de prueba y ejemplos
└─ main.py            # punto de entrada para lanzar fases
```

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1: Contador sin Lock

* Crear un `multiprocessing.Value` compartido (entero inicializado a 0).
* Lanzar 4 procesos que incrementen ese valor en bucles grandes (`100000` iteraciones cada uno).
* Mostrar el resultado.

👉 **Esperado**: el valor final suele ser **menor al teórico** (400000) → condición de carrera.

---

### 🔹 Fase 2: Contador con Lock

* Añadir un `multiprocessing.Lock`.
* Modificar la función de incremento para envolver el acceso con `with lock:`.
* Repetir el experimento.

👉 **Esperado**: ahora el valor es **exactamente 400000**.

---

### 🔹 Fase 3: Escritura concurrente en archivo con Lock

* Crear un archivo de log `log.txt`.
* Lanzar varios procesos que escriban mensajes en él.
* Comparar los resultados **sin Lock** (líneas mezcladas o incompletas) frente a **con Lock** (salida limpia).

---

## 🧭 Implementación sugerida

**app/procesos.py**

```python
from multiprocessing import Process, Value, Lock
from pathlib import Path
import time

def incrementar(contador, n_iter=100000, lock=None):
    for _ in range(n_iter):
        if lock:
            with lock:
                contador.value += 1
        else:
            contador.value += 1

def escribir_log(path: str, mensaje: str, lock=None):
    if lock:
        with lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(mensaje + "\n")
    else:
        with open(path, "a", encoding="utf-8") as f:
            f.write(mensaje + "\n")
```

**main.py**

```python
from multiprocessing import Process, Value, Lock
from app.procesos import incrementar, escribir_log
from pathlib import Path

def fase1_contador_sin_lock():
    contador = Value('i', 0)
    procesos = [Process(target=incrementar, args=(contador,)) for _ in range(4)]
    for p in procesos: p.start()
    for p in procesos: p.join()
    print("Fase 1 (sin lock) → contador:", contador.value)

def fase2_contador_con_lock():
    lock = Lock()
    contador = Value('i', 0)
    procesos = [Process(target=incrementar, args=(contador, 100000, lock)) for _ in range(4)]
    for p in procesos: p.start()
    for p in procesos: p.join()
    print("Fase 2 (con lock) → contador:", contador.value)

def fase3_log_concurrente():
    path = Path("log.txt")
    if path.exists():
        path.unlink()
    lock = Lock()
    procesos = [
        Process(target=escribir_log, args=(path, f"Mensaje {i}", lock))
        for i in range(5)
    ]
    for p in procesos: p.start()
    for p in procesos: p.join()
    print(f"Fase 3 → revisar {path} para comprobar la salida")

if __name__ == "__main__":
    fase1_contador_sin_lock()
    fase2_contador_con_lock()
    fase3_log_concurrente()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida esperada:**

```
Fase 1 (sin lock) → contador: 271893   # varía, siempre < 400000
Fase 2 (con lock) → contador: 400000
Fase 3 → revisar log.txt para comprobar la salida
```

En `log.txt` deberías ver 5 líneas correctas y completas, sin solapamientos.

---

## 🧠 Reflexión final

* ¿Por qué el contador sin lock nunca alcanza el valor esperado?
* ¿Qué coste introduce el uso de `Lock` en términos de rendimiento?
* ¿Cuándo preferirías usar `Queue` en vez de memoria compartida con `Lock`?
* ¿Qué diferencia hay entre condiciones de carrera en hilos vs procesos en Python?

---

## ✅ Comprobación de conocimientos

1. ¿Qué tipo de recurso compartido usaste en la Fase 1?
2. ¿Cómo garantiza `with lock:` la exclusión mutua?
3. ¿Qué efecto tendría eliminar el `lock` en la escritura concurrente a archivo?
4. ¿Por qué un archivo también es considerado recurso compartido?

---

## 🔥 Retos opcionales

1. **Array compartido:** usa `multiprocessing.Array('i', [0,0,0])` para que cada proceso incremente un índice distinto.
2. **Stress test:** lanza 20 procesos de incremento y compara rendimiento con y sin lock.
3. **Logging avanzado:** implementa un logger multiproceso que escriba timestamp + PID en cada línea.
4. **Deadlock simulado:** crea dos locks y dos procesos que intenten adquirirlos en orden distinto → analiza qué ocurre.