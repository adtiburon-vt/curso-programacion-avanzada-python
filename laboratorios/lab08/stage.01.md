# 🔹 Fase 1: Contador compartido **sin Lock** (reproduce la condición de carrera)

### 🎯 Objetivo

Demostrar una **condición de carrera** usando varios procesos que incrementan un **entero compartido** sin sincronización. El valor final **será menor** que el esperado.

---

## 🧱 Scaffold

```
lab8_multiprocessing/
├─ app/
│  ├─ __init__.py
│  └─ procesos.py
└─ main.py
```

---

## 🧭 Código

**app/procesos.py**

```python
# app/procesos.py
from multiprocessing import Value

def incrementar(contador: Value, n_iter: int = 100_000, lock=None) -> None:
    """
    Incrementa un entero compartido n_iter veces.
    En Fase 1 ignoramos 'lock' para forzar condición de carrera.
    """
    for _ in range(n_iter):
        # ¡SIN protección! (esto provoca race condition)
        contador.value += 1
```

**main.py**

```python
# main.py
from multiprocessing import Process, Value

def fase1_contador_sin_lock():
    # entero compartido con tipo 'i' (int)
    contador = Value('i', 0)
    procesos = [Process(target=incrementar_sin_lock, args=(contador,)) for _ in range(4)]

    for p in procesos: p.start()
    for p in procesos: p.join()

    esperado = 4 * 100_000
    print(f"Fase 1 (sin lock) → contador: {contador.value}  (esperado: {esperado})")

def incrementar_sin_lock(contador):
    # función wrapper para importar menos en el ejemplo
    from app.procesos import incrementar
    incrementar(contador, 100_000, lock=None)

if __name__ == "__main__":
    fase1_contador_sin_lock()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida típica (varía por carrera):**

```
Fase 1 (sin lock) → contador: 271893  (esperado: 400000)
```

> Lo normal es que el valor sea **menor que 400000**, evidenciando la **condición de carrera**.

---

## ✅ Criterios de aceptación

* Se crean **4 procesos** que incrementan el **mismo `Value('i', 0)`**.
* El resultado final es **inferior** al esperado (`400000`) en la mayoría de ejecuciones.
* No se usa ningún `Lock` ni mecanismo de sincronización.

---

## 🔥 Reto (opcional)

1. **Aumenta la contención:** sube `n_iter` a `1_000_000` o lanza **8 procesos** para hacer el fallo más evidente.
2. **Tiempos:** mide el tiempo total de ejecución (con `time.perf_counter()`) para comparar luego con la Fase 2.
3. **Tipos:** prueba con `Value('l', 0)` (long) y observa que el problema sigue existiendo.