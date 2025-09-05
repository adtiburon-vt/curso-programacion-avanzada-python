# 🔹 Fase 2: Consolidación de resultados con `Lock`

### 🎯 Objetivo

Mantener un **diccionario compartido** `resultados = {archivo: n_lineas}` y **proteger su acceso** con `threading.Lock` para evitar **condiciones de carrera**.

---

## 🧱 Qué vas a modificar

* Reutiliza tu estructura de la Fase 1.
* Amplía `app/procesador.py` para aceptar un **diccionario compartido** y un **lock**.
* Ajusta `main.py` para crear el lock y pasarlo a cada hilo.

---

## 🧭 Código

**app/procesador.py** (añade nuevas funciones, mantén las anteriores)

```python
# app/procesador.py
from __future__ import annotations
from pathlib import Path
from typing import MutableMapping
import threading

def contar_lineas(path: str | Path) -> int:
    p = Path(path)
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        return sum(1 for _ in f)

def tarea_contar(archivo: str | Path) -> None:
    n = contar_lineas(archivo)
    print(f"[{Path(archivo).name}] líneas: {n}")

# --- NUEVO EN FASE 2 ---
def tarea_contar_guardando(
    archivo: str | Path,
    resultados: MutableMapping[str, int],
    lock: threading.Lock,
) -> None:
    """
    Cuenta líneas y guarda el resultado en `resultados[basename] = n`.
    Usa `lock` para proteger la sección crítica.
    """
    nombre = Path(archivo).name
    n = contar_lineas(archivo)
    # sección crítica: escribir en el dict compartido
    with lock:
        resultados[nombre] = n
    # Log informativo (fuera o dentro del lock; aquí fuera para minimizar tiempo retenido)
    print(f"[{nombre}] líneas: {n} (guardado)")
```

**main.py** (actualiza para usar lock + resultados)

```python
# main.py
import threading
from pathlib import Path
from typing import Dict
from app.procesador import tarea_contar_guardando

def descubrir_archivos(carpeta: str | Path) -> list[Path]:
    data_dir = Path(carpeta)
    return sorted([p for p in data_dir.iterdir() if p.is_file() and p.suffix == ".txt"])

def main():
    archivos = descubrir_archivos("data")
    if not archivos:
        print("No se encontraron .txt en ./data")
        return

    resultados: Dict[str, int] = {}
    lock = threading.Lock()

    hilos: list[threading.Thread] = []
    for a in archivos:
        t = threading.Thread(
            target=tarea_contar_guardando,
            args=(a, resultados, lock),
            name=f"hilo-{a.stem}",
        )
        t.start()
        hilos.append(t)

    for t in hilos:
        t.join()

    print("✔ Procesamiento concurrente finalizado")
    print("Resultados consolidados (archivo -> líneas):")
    # Ordenado por nombre de archivo para una salida estable
    for nombre in sorted(resultados):
        print(f"  - {nombre}: {resultados[nombre]}")

if __name__ == "__main__":
    main()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida esperada (orden de logs variable; consolidado estable):**

```
[archivo2.txt] líneas: 18 (guardado)
[archivo1.txt] líneas: 25 (guardado)
[archivo3.txt] líneas: 9 (guardado)
✔ Procesamiento concurrente finalizado
Resultados consolidados (archivo -> líneas):
  - archivo1.txt: 25
  - archivo2.txt: 18
  - archivo3.txt: 9
```

---

## ✅ Criterios de aceptación

* Los hilos **no pisan** el diccionario compartido (sin errores de Key/Value inconsistentes).
* El programa imprime un **mapa completo** `archivo -> líneas` tras el `join()`.
* El acceso a `resultados` está **protegido con `with lock:`**.

---

## 🔥 Retos (opcionales)

1. **Contador global de archivos procesados**
   Añade `contador = {"ok": 0}` y protégelo con el mismo lock para incrementar `ok` tras cada guardado.
2. **ThreadPoolExecutor**
   Reescribe el lanzamiento usando `concurrent.futures.ThreadPoolExecutor` y `as_completed`, guardando en `resultados` bajo lock.
3. **Errores controlados**
   Simula un archivo ilegible (permisos) y guarda `-1` como líneas, sin romper el resto. (Tip: `try/except` alrededor de `contar_lineas`.)