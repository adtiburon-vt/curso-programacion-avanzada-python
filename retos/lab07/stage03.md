## 🧩 Reto 1 — Alerta visual si se evita el deadlock

🎯 *Quiero saber claramente cuándo un hilo evita un posible deadlock gracias a `acquire(timeout)`.*

---

### 🧭 Paso a paso

1. Abro `app/procesador.py`.

2. Localizo la función `resolver_con_timeout`.

3. Dentro de esta función, busco el siguiente bloque:

```python
if not acquired2:
    print(f"[{who}] no pudo tomar lock2, desistiendo para evitar deadlock")
    return
```

4. Justo después, **añado un mensaje más claro y visual**:

```python
print(f"[{who}] 💡 Deadlock evitado: liberando lock1 y abortando")
```

5. El bloque completo me queda así:

```python
if not acquired2:
    print(f"[{who}] no pudo tomar lock2, desistiendo para evitar deadlock")
    print(f"[{who}] 💡 Deadlock evitado: liberando lock1 y abortando")
    return
```

---

### ✅ Qué consigo

* El mensaje me confirma que **el hilo no se bloqueó**.
* Es una **forma visible de validar que el timeout está funcionando** como prevención.

---

## 🧩 Reto 2 — Nombres distintos para los locks

🎯 *Quiero ver en los logs qué hilo intenta tomar qué lock. Así entiendo el orden y la causa del deadlock.*

---

### 🧭 Paso a paso

1. Voy a la función `resolver_con_timeout`.

2. Modifico su definición para aceptar dos nombres de locks como strings:

```python
def resolver_con_timeout(lock1: threading.Lock, lock2: threading.Lock, who: str,
                         nombre_lock1: str = "L1", nombre_lock2: str = "L2"):
```

3. Luego, añado este log después de adquirir `lock1`:

```python
print(f"[{who}] tomó {nombre_lock1}, intentando {nombre_lock2} con timeout…")
```

4. En `deadlock_demo.py`, actualizo la llamada a los hilos:

```python
t1 = threading.Thread(
    target=resolver_con_timeout,
    args=(L1, L2, "X", "L1", "L2")
)
t2 = threading.Thread(
    target=resolver_con_timeout,
    args=(L2, L1, "Y", "L2", "L1")
)
```

---

### ✅ Qué consigo

* Ahora veo claramente **el orden de adquisición de locks por cada hilo**.
* Me ayuda a **entender la raíz del interbloqueo**.

---

## 🧩 Reto 3 — Detectar deadlock solo si ambos hilos siguen vivos

🎯 *Quiero asegurarme de que solo se considera deadlock si los dos hilos siguen atascados.*

---

### 🧭 Paso a paso

1. En `simular_deadlock()`, voy al final, justo después del `join(timeout=2.0)`.

2. Reemplazo el bloque actual:

```python
stuck = h1.is_alive() or h2.is_alive()
if stuck:
    print("⚠️  Deadlock detectado: hilos no finalizaron a tiempo")
else:
    print("✔ Sin deadlock (esta vez)")
```

Por esta nueva versión más precisa:

```python
if h1.is_alive() and h2.is_alive():
    print("⚠️  DEADLOCK confirmado: ambos hilos están bloqueados")
elif h1.is_alive() or h2.is_alive():
    print("⚠️  Un hilo sigue vivo, pero no es deadlock mutuo")
else:
    print("✔ No hubo deadlock (esta vez)")
```

---

### ✅ Qué consigo

* **Solo se considera un deadlock real si ambos hilos están vivos** y esperando.
* Aprendo a **detectar interbloqueos con `is_alive()`** de forma precisa.

---

## 🎉 Resultado final

Después de aplicar estos tres cambios:

* Entiendo **cómo y cuándo ocurre un deadlock**.
* Puedo **ver claramente cómo lo he evitado con `timeout` o con orden global**.
* Mis logs son ahora una **herramienta de aprendizaje visual y de diagnóstico**.