# 🔹 Fase 3: Escritura concurrente en archivo (con y sin `Lock`)

### 🎯 Objetivo

Comparar la **escritura multiproceso** a un mismo fichero **sin protección** vs **protegida con `Lock`**, observando líneas truncadas/mezcladas frente a una salida limpia.

---

## 🧱 Qué vas a añadir

* Dos funciones en `app/procesos.py`:

  * `escribir_log(path, mensaje)` (sin lock)
  * `escribir_log_seguro(path, mensaje, lock)` (con lock)
* Dos “demos” en `main.py` para ver el contraste.

---

## 🧭 Código

**app/procesos.py** (añade estas funciones; deja las de las fases anteriores tal cual)

```python
# app/procesos.py
from multiprocessing import Value, Lock
from pathlib import Path
import os
import time

def incrementar(contador: Value, n_iter: int = 100_000, lock: Lock | None = None) -> None:
    if lock is None:
        for _ in range(n_iter):
            contador.value += 1
    else:
        for _ in range(n_iter):
            with lock:
                contador.value += 1

# --- NUEVO: escritura concurrente ---
def escribir_log(path: str | Path, mensaje: str) -> None:
    """
    Escribe una línea en un archivo compartido SIN sincronización.
    Bajo contención, pueden aparecer líneas mezcladas o truncadas.
    """
    p = Path(path)
    # Simula trabajo para aumentar la probabilidad de intercalado
    time.sleep(0.001)
    with p.open("a", encoding="utf-8") as f:
        f.write(mensaje + "\n")

def escribir_log_seguro(path: str | Path, mensaje: str, lock: Lock) -> None:
    """
    Escribe una línea en un archivo compartido con protección por Lock.
    Garantiza atomicidad a nivel lógico para cada línea.
    """
    p = Path(path)
    time.sleep(0.001)
    with lock:
        with p.open("a", encoding="utf-8") as f:
            f.write(mensaje + "\n")
```

**main.py** (añade demos de Fase 3; puedes conservar lo de Fase 1/2)

```python
# main.py
from multiprocessing import Process, Value, Lock
from pathlib import Path
from app.procesos import (
    incrementar,
    escribir_log,
    escribir_log_seguro,
)

N_PROCESOS = 8
N_LINEAS_POR_PROCESO = 200   # súbelo si quieres forzar más contención

def demo_log_sin_lock():
    path = Path("log_sin_lock.txt")
    if path.exists(): path.unlink()

    procesos = []
    for i in range(N_PROCESOS):
        def worker(idx=i):
            for j in range(N_LINEAS_POR_PROCESO):
                msg = f"[PID?] P{idx:02d} L{j:04d}"
                escribir_log(path, msg)
        procesos.append(Process(target=worker))

    for p in procesos: p.start()
    for p in procesos: p.join()
    print(f"Fase 3A (sin lock) → revisa {path}")

def demo_log_con_lock():
    path = Path("log_con_lock.txt")
    if path.exists(): path.unlink()

    lock = Lock()
    procesos = []
    for i in range(N_PROCESOS):
        def worker(idx=i):
            for j in range(N_LINEAS_POR_PROCESO):
                msg = f"[SEG] P{idx:02d} L{j:04d}"
                escribir_log_seguro(path, msg, lock)
        procesos.append(Process(target=worker))

    for p in procesos: p.start()
    for p in procesos: p.join()
    print(f"Fase 3B (con lock) → revisa {path}")

if __name__ == "__main__":
    # Lanza solo la fase 3 para comparar ficheros
    demo_log_sin_lock()
    demo_log_con_lock()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Qué observar:**

* En `log_sin_lock.txt` (sin lock): con suficiente contención puede haber **líneas mezcladas/truncadas** (depende del SO/FS; si no lo ves, incrementa `N_PROCESOS` o `N_LINEAS_POR_PROCESO`).
* En `log_con_lock.txt` (con lock): **todas las líneas completas y bien formateadas**.

> Tip: también puedes comparar el nº de líneas:
>
> * Esperadas: `N_PROCESOS * N_LINEAS_POR_PROCESO`.
> * Sin lock a veces faltan o se rompen líneas (no siempre reproducible).
> * Con lock siempre coincide.

---

## ✅ Criterios de aceptación

* Se generan **dos archivos**: uno sin lock y otro con lock.
* El fichero “con lock” contiene **exactamente** `N_PROCESOS * N_LINEAS_POR_PROCESO` líneas, cada una completa.
* El fichero “sin lock” puede evidenciar desorden/mezcla bajo alta contención.

---

## 🔥 Retos (opcionales)

1. **Verificación automática:** escribe un script que valide que cada proceso generó exactamente sus `L0000…L(N-1)` líneas en “con lock” y detecte huecos/errores en “sin lock”.
2. **Benchmark:** mide tiempo total de ambos modos para cuantificar el coste del lock.
3. **Queue en lugar de Lock:** envía mensajes a un proceso escritor único mediante `multiprocessing.Queue` y compáralo con el enfoque de Lock.

---

# ✅ Conclusión del Laboratorio 8

**Qué te llevas:**

* Has reproducido una **condición de carrera** (Fase 1) y la has eliminado con **`multiprocessing.Lock`** (Fase 2).
* Has comprobado que la **E/S a fichero** es un **recurso compartido** que **también** requiere sincronización (Fase 3).

**Ideas clave:**

* Los **locks** garantizan **exclusión mutua**; úsalos en secciones críticas **lo más cortas posible**.
* No todo debe sincronizarse: cuando la lógica lo permita, **prefiere `Queue`** para desacoplar productores y un escritor único.
* Sincronización ≠ gratis: **mide** y decide el grano de bloqueo adecuado (por lote, por línea, por registro…).