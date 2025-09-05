# 🔹 Fase 2 — Organizar ficheros por **fecha** (YYYY-MM) dentro de cada tipo

### 🎯 Objetivo

Tomar lo ya organizado por **extensión** en `data/organizado/` y, **dentro de cada carpeta de tipo**, mover los archivos a subcarpetas por **año-mes** (`2025-09/`) usando la fecha de **modificación** del fichero.

---

## 🧭 Código

**app/organizador.py** (añade esta función debajo de `organizar_por_tipo`)

```python
from pathlib import Path
import shutil
from datetime import datetime

def organizar_por_fecha(base: Path) -> None:
    """
    Dentro de cada carpeta de tipo en `base`, mueve los archivos a subcarpetas YYYY-MM
    según su fecha de modificación (mtime).
    """
    if not base.exists():
        return

    for carpeta_tipo in base.iterdir():
        if not carpeta_tipo.is_dir():
            continue

        for archivo in list(carpeta_tipo.iterdir()):
            if not archivo.is_file():
                continue

            ts = archivo.stat().st_mtime
            yyyymm = datetime.fromtimestamp(ts).strftime("%Y-%m")
            destino = carpeta_tipo / yyyymm
            destino.mkdir(parents=True, exist_ok=True)

            shutil.move(str(archivo), destino / archivo.name)
            print(f"Movido por fecha: {archivo.name} → {destino}/")
```

**main.py** (amplía para llamar a Fase 2 después de Fase 1)

```python
from pathlib import Path
from app.organizador import organizar_por_tipo, organizar_por_fecha

def fase1():
    entrada = Path("data/entrada")
    salida = Path("data/organizado")
    print("== Fase 1: organizar por tipo ==")
    organizar_por_tipo(entrada, salida)
    print("✔ Archivos organizados por extensión")

def fase2():
    salida = Path("data/organizado")
    print("== Fase 2: organizar por fecha (YYYY-MM) ==")
    organizar_por_fecha(salida)
    print("✔ Archivos organizados por fecha dentro de cada tipo")

if __name__ == "__main__":
    # Ejecuta Fase 1 y luego Fase 2 (o solo Fase 2 si ya hiciste la 1)
    fase1()
    fase2()
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
...
✔ Archivos organizados por extensión
== Fase 2: organizar por fecha (YYYY-MM) ==
Movido por fecha: informe.txt → data/organizado/txt/2025-09/
...
✔ Archivos organizados por fecha dentro de cada tipo
```

---

## ✅ Resultado esperado en disco

```
data/organizado/
├─ txt/
│  └─ 2025-09/
│      └─ informe.txt
├─ csv/
│  └─ 2024-12/
│      └─ ventas.csv
└─ jpg/
   └─ 2023-07/
       └─ foto.jpg
```

---

## 🔧 Notas y buenas prácticas

* Usamos **mtime** (fecha de modificación). Si prefieres **ctime**/creación, adapta `stat()`.
* Para **fechas forzadas** en pruebas, puedes tocar mtime con `os.utime(path, (atime, mtime))`.
* Si una carpeta de tipo queda **vacía** tras mover, puedes limpiarla con `carpeta_tipo.rmdir()` (opcional).

---

## 🔥 Retos opcionales

1. **Cierre de mes**: añade subcarpetas por **día** (`YYYY-MM/DD`).
2. **Limpieza**: borra carpetas de tipo vacías tras la operación.
3. **CLI**: añade flags `--by day|month` y `--dry-run` para simular sin mover realmente (imprimiría qué haría).