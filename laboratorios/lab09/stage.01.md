# 🔹 Fase 1 — Organizar ficheros por tipo

### 🎯 Objetivo

Mover los archivos desde la carpeta `data/entrada/` a subcarpetas en `data/organizado/` según su **extensión** (`.txt`, `.csv`, `.jpg`, etc.).

---

## 🧱 Scaffold inicial

```
lab9_files_serialization/
├─ data/
│  ├─ entrada/
│  │   ├─ informe.txt
│  │   ├─ ventas.csv
│  │   ├─ foto.jpg
│  │   └─ script.py
│  └─ organizado/       # aquí se crearán subcarpetas
└─ app/
   ├─ __init__.py
   └─ organizador.py
```

---

## 🧭 Código

**app/organizador.py**

```python
from pathlib import Path
import shutil

def organizar_por_tipo(src: Path, dst: Path) -> None:
    """
    Organiza archivos de src en carpetas según su extensión dentro de dst.
    """
    dst.mkdir(parents=True, exist_ok=True)

    for archivo in src.iterdir():
        if archivo.is_file():
            # obtener extensión sin el punto
            ext = archivo.suffix.lstrip(".").lower() or "otros"
            carpeta_destino = dst / ext
            carpeta_destino.mkdir(parents=True, exist_ok=True)

            # mover archivo
            shutil.move(str(archivo), carpeta_destino / archivo.name)
            print(f"Movido: {archivo.name} → {carpeta_destino}/")
```

**main.py**

```python
from pathlib import Path
from app.organizador import organizar_por_tipo

def fase1():
    entrada = Path("data/entrada")
    salida = Path("data/organizado")

    print("== Fase 1: organizar por tipo ==")
    organizar_por_tipo(entrada, salida)
    print("✔ Archivos organizados por extensión")

if __name__ == "__main__":
    fase1()
```

---

## ▶️ Ejecución

```bash
python main.py
```

**Salida esperada (ejemplo):**

```
== Fase 1: organizar por tipo ==
Movido: informe.txt → data/organizado/txt/
Movido: ventas.csv → data/organizado/csv/
Movido: foto.jpg → data/organizado/jpg/
Movido: script.py → data/organizado/py/
✔ Archivos organizados por extensión
```

---

## ✅ Resultado esperado en disco

```
data/organizado/
├─ txt/
│  └─ informe.txt
├─ csv/
│  └─ ventas.csv
├─ jpg/
│  └─ foto.jpg
└─ py/
   └─ script.py
```

---

## 🔥 Retos opcionales

1. Crear una carpeta **otros/** para archivos sin extensión.
2. Hacer que ignore archivos ocultos (los que empiezan por `.`).
3. Convertir el script en una función CLI con `argparse` que reciba rutas `--src` y `--dst`.