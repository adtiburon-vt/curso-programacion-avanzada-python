# 🔹 Fase 1: Lectura concurrente de archivos (sin Locks)

### 🎯 Objetivo

Crear un **hilo por archivo** para contar líneas en paralelo usando `threading.Thread`. En esta fase **no** consolidamos resultados compartidos (eso llega en Fase 2 con `Lock`).

---

## 🧱 Scaffold

Estructura mínima:

```
lab7_threads/
├─ app/
│  ├─ __init__.py
│  └─ procesador.py
├─ data/
│  ├─ archivo1.txt
│  ├─ archivo2.txt
│  └─ archivo3.txt
└─ main.py
```

> Si aún no tienes los `.txt`, crea tres ficheros con algunas líneas cada uno.

---

## 🧭 Código

**app/procesador.py**

```python
# app/procesador.py
from __future__ import annotations
from pathlib import Path

def contar_lineas(path: str | Path) -> int:
    """Cuenta las líneas de un archivo de texto (modo eficiente)."""
    p = Path(path)
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        # sum(1 for _ in f) es perezoso y consume poca memoria
        return sum(1 for _ in f)

def tarea_contar(archivo: str | Path) -> None:
    """Tarea para ejecutar en un hilo: cuenta e imprime el resultado."""
    n = contar_lineas(archivo)
    print(f"[{Path(archivo).name}] líneas: {n}")
```

**main.py**

```python
# main.py
import threading
from pathlib import Path
from app.procesador import tarea_contar

def descubrir_archivos(carpeta: str | Path) -> list[Path]:
    data_dir = Path(carpeta)
    return sorted([p for p in data_dir.iterdir() if p.is_file() and p.suffix == ".txt"])

def main():
    archivos = descubrir_archivos("data")
    if not archivos:
        print("No se encontraron .txt en ./data")
        return

    hilos: list[threading.Thread] = []
    for a in archivos:
        t = threading.Thread(target=tarea_contar, args=(a,), name=f"hilo-{a.stem}")
        t.start()
        hilos.append(t)

    # Espera a que todos terminen
    for t in hilos:
        t.join()

    print("✔ Procesamiento concurrente finalizado")

if __name__ == "__main__":
    main()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida esperada (orden puede variar por concurrencia):**

```
[archivo2.txt] líneas: 18
[archivo1.txt] líneas: 25
[archivo3.txt] líneas: 9
✔ Procesamiento concurrente finalizado
```

---

## ✅ Criterios de aceptación

* Se lanza **un hilo por archivo** `.txt` dentro de `./data`.
* Cada hilo **imprime** el nombre del archivo y su **conteo de líneas**.
* El programa **espera** a todos los hilos (`join`) y termina con un mensaje de éxito.

---

## 🔥 Reto (opcional)

1. Añade un **prefijo con el nombre del hilo** en la impresión (usa `threading.current_thread().name`).
2. Mide el **tiempo total**: imprime duración en segundos (import `time`).
3. Cambia el conteo de líneas por **conteo de palabras** del archivo (suma de `len(line.split())`).