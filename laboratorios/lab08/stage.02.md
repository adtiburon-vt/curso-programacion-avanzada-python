# 🔹 Fase 2: Contador compartido **con `multiprocessing.Lock`**

### 🎯 Objetivo

Eliminar la condición de carrera usando un **`Lock`** para proteger la sección crítica al incrementar el entero compartido. El valor final debe ser **exactamente** el esperado.

---

## 🧱 Qué cambia respecto a Fase 1

* Creamos un **`Lock()`** y lo pasamos a cada proceso.
* En la función de trabajo, envolvemos el incremento con `with lock:`.

---

## 🧭 Código

**app/procesos.py** (amplía la función para usar `lock` si se provee)

```python
# app/procesos.py
from multiprocessing import Value, Lock

def incrementar(contador: Value, n_iter: int = 100_000, lock: Lock | None = None) -> None:
    """
    Incrementa un entero compartido n_iter veces.
    Si se proporciona lock, protege la sección crítica.
    """
    if lock is None:
        # SIN protección (Fase 1)
        for _ in range(n_iter):
            contador.value += 1
    else:
        # CON protección (Fase 2)
        for _ in range(n_iter):
            with lock:
                contador.value += 1
```

**main.py** (añade una función nueva para Fase 2)

```python
# main.py
from multiprocessing import Process, Value, Lock
from app.procesos import incrementar

N_PROCESOS = 4
N_ITER = 100_000

def fase2_contador_con_lock():
    contador = Value('i', 0)
    lock = Lock()

    procesos = [
        Process(target=incrementar, args=(contador, N_ITER, lock))
        for _ in range(N_PROCESOS)
    ]

    for p in procesos: p.start()
    for p in procesos: p.join()

    esperado = N_PROCESOS * N_ITER
    print(f"Fase 2 (con lock) → contador: {contador.value}  (esperado: {esperado})")

if __name__ == "__main__":
    # Puedes ejecutar solo Fase 2, o llamar también a la Fase 1 si la mantienes.
    fase2_contador_con_lock()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida esperada:**

```
Fase 2 (con lock) → contador: 400000  (esperado: 400000)
```

---

## ✅ Criterios de aceptación

* Se crean **N\_PROCESOS** procesos que incrementan el mismo `Value('i', 0)` con **`Lock`** compartido.
* El resultado final **coincide** con `N_PROCESOS * N_ITER` en **todas** las ejecuciones.
* El incremento está protegido con `with lock:` (exclusión mutua real).

---

## 🔥 Retos (opcionales)

1. **Benchmark**: mide el tiempo de Fase 1 vs Fase 2 (`time.perf_counter()`); comenta la diferencia (el lock añade coste, pero garantiza consistencia).
2. **Grano fino**: intenta reducir la sección crítica (p. ej., acumular en una variable local y escribir cada K iteraciones bajo lock) y compara rendimiento.
3. **Stress**: sube a `N_PROCESOS = 16` y `N_ITER = 1_000_000` para observar el impacto en rendimiento y ver que la exactitud se mantiene.