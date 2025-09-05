# 🧭 Laboratorio 9 — Organizar ficheros + conversión entre formatos

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 9 (Ficheros y serialización en Python)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

Aplicar la manipulación de ficheros (lectura/escritura, `os`, `shutil`) junto con serialización (Pickle, JSON, XML) para:

1. **Organizar** ficheros en carpetas según su tipo y fecha.
2. **Convertir** datos entre distintos formatos de serialización.

---

## 📁 Estructura sugerida del proyecto

```
lab9_files_serialization/
├─ data/
│  ├─ entrada/          # ficheros desordenados
│  ├─ organizado/       # salida ordenada por tipo/fecha
│  └─ datasets/         # ficheros de datos (json/xml/pickle)
├─ app/
│  ├─ __init__.py
│  ├─ organizador.py    # funciones de clasificación y movimiento
│  └─ conversion.py     # funciones de serialización
└─ main.py              # menú principal para ejecutar fases
```

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1 — Organizar ficheros por tipo (extensión)

* Escanear la carpeta `data/entrada/`.
* Crear subcarpetas dentro de `data/organizado/` según extensión (`.txt`, `.csv`, `.jpg`, …).
* Mover cada archivo a su carpeta correspondiente usando `shutil.move`.

---

### 🔹 Fase 2 — Organizar ficheros por fecha de modificación

* Dentro de cada carpeta de tipo, crear subcarpetas por **año-mes** (`2025-09/`).
* Usar `os.path.getmtime()` o `Path.stat().st_mtime` para obtener la fecha.
* Mover cada archivo a su subcarpeta de fecha correspondiente.

---

### 🔹 Fase 3 — Conversión entre formatos (Pickle, JSON, XML)

* Crear un diccionario de ejemplo con varios registros (usuarios, productos…).
* Guardar el dataset en:

  * `usuarios.json`
  * `usuarios.pkl`
  * `usuarios.xml`
* Implementar funciones que conviertan **JSON ⇄ XML** y **JSON ⇄ Pickle**.
* Validar que los datos se mantienen equivalentes tras cada conversión.

---

## 🧭 Implementación sugerida

**app/organizador.py**

```python
from pathlib import Path
import shutil
import os
from datetime import datetime

def organizar_por_tipo(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    for archivo in src.iterdir():
        if archivo.is_file():
            ext = archivo.suffix.lstrip(".").lower() or "otros"
            carpeta = dst / ext
            carpeta.mkdir(parents=True, exist_ok=True)
            shutil.move(str(archivo), carpeta / archivo.name)

def organizar_por_fecha(base: Path):
    for carpeta_tipo in base.iterdir():
        if carpeta_tipo.is_dir():
            for archivo in carpeta_tipo.iterdir():
                ts = archivo.stat().st_mtime
                fecha = datetime.fromtimestamp(ts).strftime("%Y-%m")
                carpeta_fecha = carpeta_tipo / fecha
                carpeta_fecha.mkdir(parents=True, exist_ok=True)
                shutil.move(str(archivo), carpeta_fecha / archivo.name)
```

**app/conversion.py**

```python
import json, pickle
import xml.etree.ElementTree as ET
from pathlib import Path

def guardar_json(datos, path: Path):
    with path.open("w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def cargar_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def guardar_pickle(datos, path: Path):
    with path.open("wb") as f:
        pickle.dump(datos, f)

def cargar_pickle(path: Path):
    with path.open("rb") as f:
        return pickle.load(f)

def guardar_xml(datos: list[dict], path: Path):
    root = ET.Element("usuarios")
    for d in datos:
        u = ET.SubElement(root, "usuario")
        for k, v in d.items():
            ET.SubElement(u, k).text = str(v)
    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)

def cargar_xml(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    return [{c.tag: c.text for c in u} for u in root.findall("usuario")]
```

**main.py**

```python
from pathlib import Path
from app.organizador import organizar_por_tipo, organizar_por_fecha
from app.conversion import guardar_json, guardar_pickle, guardar_xml, cargar_json, cargar_pickle, cargar_xml

def main():
    entrada = Path("data/entrada")
    salida = Path("data/organizado")

    print("== Fase 1: organizar por tipo ==")
    organizar_por_tipo(entrada, salida)

    print("== Fase 2: organizar por fecha ==")
    organizar_por_fecha(salida)

    print("== Fase 3: conversión de formatos ==")
    usuarios = [
        {"nombre": "Ana", "edad": 30},
        {"nombre": "Luis", "edad": 25},
    ]

    guardar_json(usuarios, Path("data/datasets/usuarios.json"))
    guardar_pickle(usuarios, Path("data/datasets/usuarios.pkl"))
    guardar_xml(usuarios, Path("data/datasets/usuarios.xml"))

    print("JSON →", cargar_json(Path("data/datasets/usuarios.json")))
    print("Pickle →", cargar_pickle(Path("data/datasets/usuarios.pkl")))
    print("XML →", cargar_xml(Path("data/datasets/usuarios.xml")))

if __name__ == "__main__":
    main()
```

---

## ✅ Criterios de aceptación

* Archivos en `data/entrada/` terminan organizados en `data/organizado/{tipo}/{YYYY-MM}/`.
* Los tres formatos (`.json`, `.pkl`, `.xml`) contienen los mismos datos de ejemplo.
* Las funciones de carga devuelven estructuras equivalentes al original.

---

## 🧠 Reflexión final

* ¿Qué ventajas ofrece organizar por **tipo** y **fecha** frente a tener todo en una carpeta plana?
* ¿Qué riesgos tiene usar Pickle frente a JSON/XML?
* ¿Qué formatos elegirías para **backup local** vs **intercambio con otras aplicaciones**?

---

## 🔥 Retos opcionales

1. Implementa la opción de **CSV** además de JSON/XML/Pickle.
2. Haz que `organizar_por_tipo` ignore archivos ocultos (`.gitignore`, `.DS_Store`).
3. Añade un **menú interactivo en CLI** (argparse) para elegir fase.
4. Escribe un test `unittest` que valide que los datos tras JSON ⇄ XML son equivalentes.
