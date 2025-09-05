# 🧭 Laboratorio 7 — Procesamiento concurrente de archivos

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 7 (Concurrencia con hilos en Python)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

Implementar un sistema que procese múltiples archivos de texto en paralelo usando **hilos**, proteja el acceso a recursos compartidos con **Locks**, y reflexionar sobre la gestión de **deadlocks**.

---

## 📁 Estructura del proyecto

```
lab7_threads/
├─ app/
│  ├─ __init__.py
│  └─ procesador.py     # funciones para procesamiento concurrente
├─ data/
│  ├─ archivo1.txt
│  ├─ archivo2.txt
│  └─ archivo3.txt
└─ main.py              # punto de entrada
```

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1: Lectura concurrente de archivos

* Crear un hilo por archivo en `data/`.
* Cada hilo debe contar el número de líneas en su archivo y mostrar el resultado.
* Usar `threading.Thread`.

---

### 🔹 Fase 2: Consolidación con Lock

* Guardar los resultados en un diccionario global `resultados = {archivo: n_lineas}`.
* Proteger el acceso a `resultados` con un **`threading.Lock`** para evitar condiciones de carrera.
* Imprimir el diccionario consolidado al final.

---

### 🔹 Fase 3: Simulación y prevención de deadlock

* Crear dos locks (`lock1`, `lock2`) y dos hilos que intenten usarlos en orden distinto → provocar **deadlock**.
* Solucionar el problema aplicando una estrategia:

  * Adquirir siempre los locks en el mismo orden, **o**
  * Usar `acquire(timeout=…)` y manejar el fallo.

---

## 🧠 Reflexión final

* ¿Qué mejora aporta el uso de **hilos** respecto a procesar archivos de manera secuencial?
* ¿Qué problemas aparecen si no se protege el acceso a estructuras compartidas?
* ¿Qué es más grave: una condición de carrera silenciosa o un deadlock evidente?
* ¿Cómo trasladarías este mismo patrón a un escenario de **descarga de ficheros** o **procesamiento de logs**?

---

## 📁 Archivos utilizados

* `data/archivo1.txt`, `data/archivo2.txt`, `data/archivo3.txt` (pueden ser generados con texto de ejemplo).
* `app/procesador.py`: funciones de lectura y consolidación.
* `main.py`: arranca los hilos y muestra resultados.

---

## ✅ Comprobación de conocimientos

1. ¿Qué diferencia hay entre una condición de carrera y un deadlock?
2. ¿Cómo usarías `with lock:` para simplificar el código frente a `lock.acquire()` / `release()` manual?
3. ¿Qué ventaja aporta `ThreadPoolExecutor` frente a crear hilos manualmente?

---

## 🔥 Retos opcionales

1. **Contar palabras en lugar de líneas** en paralelo.
2. **Exportar resultados a JSON** tras consolidar.
3. **Usar ThreadPoolExecutor** en lugar de `threading.Thread`.
4. Implementar una **barra de progreso** que muestre cuántos archivos han sido procesados hasta ahora.