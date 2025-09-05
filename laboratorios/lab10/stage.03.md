¡Perfecto! Aquí tienes la **Fase 3** del **Lab 10 — ETL con Pandas** y la **conclusión** del laboratorio.

---

# 🔹 Fase 3 — ETL con Pandas (lectura, joins, agregaciones)

### 🎯 Objetivo

Exportar tablas desde **SQLite** y/o leer desde **MongoDB**, combinarlas en **Pandas** y generar métricas básicas (importe por cliente, unidades por producto).

---

## 🧱 Estructura mínima

```
lab10_db_ml/
├─ data/
│  ├─ export/                  # CSVs generados aquí
│  └─ sqlite/usuarios.db       # creado en Fase 1
└─ app/
   ├─ sql_demo.py
   ├─ mongo_demo.py
   └─ etl_pandas.py
```

---

## 🧭 Código (app/etl\_pandas.py)

```python
# app/etl_pandas.py
from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("data/sqlite/usuarios.db")
EXPORT_DIR = Path("data/export")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def export_sqlite_to_csv() -> None:
    """Exporta las tres tablas de SQLite a CSV para trazabilidad."""
    con = sqlite3.connect(DB_PATH)
    try:
        clientes  = pd.read_sql_query("SELECT * FROM clientes", con)
        productos = pd.read_sql_query("SELECT * FROM productos", con)
        ventas    = pd.read_sql_query("SELECT * FROM ventas",    con)
    finally:
        con.close()

    clientes.to_csv(EXPORT_DIR / "clientes.csv",  index=False)
    productos.to_csv(EXPORT_DIR / "productos.csv", index=False)
    ventas.to_csv(EXPORT_DIR / "ventas.csv",    index=False)

def cargar_y_unir() -> pd.DataFrame:
    """Carga CSVs exportados y realiza los 'joins' en Pandas."""
    c = pd.read_csv(EXPORT_DIR / "clientes.csv")   .rename(columns={"id": "id_cliente"})
    p = pd.read_csv(EXPORT_DIR / "productos.csv")  .rename(columns={"id": "id_producto", "nombre": "producto"})
    v = pd.read_csv(EXPORT_DIR / "ventas.csv")

    df = (v.merge(c, on="id_cliente", how="left")
            .merge(p, on="id_producto", how="left"))
    df["importe"] = df["cantidad"] * df["precio"]
    return df[["id_cliente", "nombre", "email", "producto", "cantidad", "precio", "importe"]]

def informes(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Genera reportes: importe por cliente y unidades por producto."""
    por_cliente  = (df.groupby(["id_cliente", "nombre"], as_index=False)["importe"]
                      .sum().sort_values("importe", ascending=False))
    por_producto = (df.groupby("producto", as_index=False)["cantidad"]
                      .sum().rename(columns={"cantidad": "uds"})
                      .sort_values("uds", ascending=False))
    return por_cliente, por_producto

def main():
    print("== ETL: exportando desde SQLite a CSV ==")
    export_sqlite_to_csv()
    print("   ✓ CSVs: clientes.csv, productos.csv, ventas.csv")

    print("== ETL: uniendo en Pandas (ventas ↔ clientes ↔ productos) ==")
    df = cargar_y_unir()
    print(df.head())

    print("== Informes ==")
    rc, rp = informes(df)
    print("\nImporte total por cliente:\n", rc.to_string(index=False))
    print("\nUnidades por producto:\n",   rp.to_string(index=False))

    # Exportar informes
    rc.to_csv(EXPORT_DIR / "reporte_importe_por_cliente.csv", index=False)
    rp.to_csv(EXPORT_DIR / "reporte_unidades_por_producto.csv", index=False)
    print("\n✓ Reportes guardados en data/export/")

if __name__ == "__main__":
    main()
```

> **Opcional (extra)**: si quieres traer datos **directo de MongoDB**, puedes usar `pandas.DataFrame(list(collection.find()))` y luego hacer merges por `id_cliente`/`id_producto`. Mantén una clave coherente (`_id` ↔ `id_*`).

---

## ▶️ Ejecución

```bash
python -m app.etl_pandas
```

**Salida esperada (resumen):**

```
== ETL: exportando desde SQLite a CSV ==
   ✓ CSVs: clientes.csv, productos.csv, ventas.csv
== ETL: uniendo en Pandas (ventas ↔ clientes ↔ productos) ==
   ... (primeras filas del detalle) ...
== Informes ==
Importe total por cliente:
 id_cliente nombre  importe
          1    Ana   1080.0
          3  Marta    180.0
          2   Luis     50.0

Unidades por producto:
 producto  uds
 Monitor    2
 Portátil   1
 Teclado    2

✓ Reportes guardados en data/export/
```

---

## ✅ Criterios de aceptación

* Se crean **tres CSVs** (`clientes.csv`, `productos.csv`, `ventas.csv`) en `data/export/`.
* El DataFrame final contiene las columnas: `nombre` (cliente), `producto`, `cantidad`, `precio`, `importe`.
* Se generan **dos reportes** CSV: `reporte_importe_por_cliente.csv` y `reporte_unidades_por_producto.csv`.

