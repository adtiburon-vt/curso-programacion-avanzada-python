# 🧭 Laboratorio 10 — CRUD en SQLite/MongoDB + análisis y modelos simples

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 10 (Bases de datos y ciencia de datos)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

1. Practicar **CRUD** en **SQLite** (SQL) y **MongoDB** (NoSQL).
2. Hacer un pequeño **ETL** a **Pandas** y realizar **joins/aggregaciones**.
3. Entrenar **modelos simples** con **Scikit-learn** (clasificación/regresión).

---

## ⚙️ Requisitos

```txt
python>=3.10
pandas
scikit-learn
pymongo
```

Opcional: `sqlalchemy` (si quieres ORM).

> Asegúrate de tener un MongoDB accesible (local `mongodb://localhost:27017` o Atlas).

---

## 📁 Estructura sugerida

```
lab10_db_ml/
├─ data/
│  ├─ export/                 # CSV/JSON de salida
│  └─ sqlite/usuarios.db      # se crea en la Fase 1
├─ app/
│  ├─ __init__.py
│  ├─ sql_demo.py             # SQLite (CRUD)
│  ├─ mongo_demo.py           # MongoDB (CRUD)
│  ├─ etl_pandas.py           # Lectura/joins/aggregaciones
│  └─ ml_models.py            # Scikit-learn
└─ main.py                    # menú/driver opcional
```

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1 — CRUD en **SQLite** (módulo estándar `sqlite3`)

**Objetivo:** crear tablas `clientes`, `productos`, `ventas` y practicar CRUD + un par de consultas útiles.

**app/sql\_demo.py**

```python
import sqlite3
from pathlib import Path

DB_PATH = Path("data/sqlite/usuarios.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DDL = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS clientes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS productos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  precio REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS ventas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente INTEGER NOT NULL,
  id_producto INTEGER NOT NULL,
  cantidad INTEGER NOT NULL CHECK (cantidad > 0),
  FOREIGN KEY(id_cliente) REFERENCES clientes(id),
  FOREIGN KEY(id_producto) REFERENCES productos(id)
);
"""

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = connect()
    cur = conn.cursor()
    for stmt in DDL.strip().split(";"):
        s = stmt.strip()
        if s:
            cur.execute(s)
    conn.commit()
    conn.close()

def seed():
    conn = connect(); cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO clientes(nombre,email) VALUES(?,?)",
        [("Ana","ana@test.com"),("Luis","luis@test.com"),("Marta","marta@test.com")])
    cur.executemany("INSERT OR IGNORE INTO productos(nombre,precio) VALUES(?,?)",
        [("Portátil",900.0),("Monitor",180.0),("Teclado",25.0)])
    # ventas sample
    cur.executemany("INSERT INTO ventas(id_cliente,id_producto,cantidad) VALUES(?,?,?)",
        [(1,1,1),(1,2,1),(2,3,2),(3,2,1)])
    conn.commit(); conn.close()

def demo_crud():
    conn = connect(); cur = conn.cursor()
    # CREATE
    cur.execute("INSERT INTO clientes(nombre,email) VALUES(?,?)", ("Carlos","carlos@test.com"))
    conn.commit()
    # READ (join ventas→clientes/productos)
    cur.execute("""
        SELECT c.nombre AS cliente, p.nombre AS producto, v.cantidad, p.precio, (v.cantidad*p.precio) AS importe
        FROM ventas v
        JOIN clientes c ON c.id=v.id_cliente
        JOIN productos p ON p.id=v.id_producto
        ORDER BY cliente
    """)
    print("Ventas:")
    for row in cur.fetchall(): print(row)
    # UPDATE
    cur.execute("UPDATE productos SET precio=? WHERE nombre=?", (190.0, "Monitor")); conn.commit()
    # DELETE
    cur.execute("DELETE FROM clientes WHERE email=?", ("carlos@test.com",)); conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed()
    demo_crud()
```

**Validación:**

* DB creada en `data/sqlite/usuarios.db`.
* `Ventas:` se imprime con filas (cliente, producto, cantidad, precio, importe).
* Cambia el precio de “Monitor” a 190 y borra “Carlos”.

---

### 🔹 Fase 2 — CRUD en **MongoDB** (`pymongo`)

**Objetivo:** insertar documentos equivalentes y practicar consultas/updates.

**app/mongo\_demo.py**

```python
from pymongo import MongoClient

def get_collections(uri="mongodb://localhost:27017", dbname="lab10"):
    client = MongoClient(uri)
    db = client[dbname]
    return db["clientes"], db["productos"], db["ventas"]

def seed():
    clientes, productos, ventas = get_collections()
    clientes.delete_many({}); productos.delete_many({}); ventas.delete_many({})

    c = clientes.insert_many([
        {"_id": 1, "nombre":"Ana", "email":"ana@test.com"},
        {"_id": 2, "nombre":"Luis","email":"luis@test.com"},
        {"_id": 3, "nombre":"Marta","email":"marta@test.com"},
    ])
    p = productos.insert_many([
        {"_id": 1, "nombre":"Portátil","precio":900.0},
        {"_id": 2, "nombre":"Monitor","precio":180.0},
        {"_id": 3, "nombre":"Teclado","precio":25.0},
    ])
    ventas.insert_many([
        {"id_cliente":1, "id_producto":1, "cantidad":1},
        {"id_cliente":1, "id_producto":2, "cantidad":1},
        {"id_cliente":2, "id_producto":3, "cantidad":2},
        {"id_cliente":3, "id_producto":2, "cantidad":1},
    ])

def demo_crud():
    clientes, productos, ventas = get_collections()
    # CREATE
    clientes.insert_one({"_id": 4, "nombre":"Carlos", "email":"carlos@test.com"})
    # READ (lookup estilo join con aggregation pipeline)
    pipeline = [
        {"$lookup": {"from":"clientes", "localField":"id_cliente", "foreignField":"_id", "as":"c"}},
        {"$lookup": {"from":"productos","localField":"id_producto","foreignField":"_id","as":"p"}},
        {"$unwind":"$c"}, {"$unwind":"$p"},
        {"$addFields":{"importe":{"$multiply":["$cantidad","$p.precio"]}}},
        {"$project":{"_id":0,"cliente":"$c.nombre","producto":"$p.nombre","cantidad":1,"precio":"$p.precio","importe":1}},
        {"$sort":{"cliente":1}}
    ]
    print("Ventas (pipeline):")
    for doc in ventas.aggregate(pipeline):
        print(doc)
    # UPDATE
    productos.update_one({"nombre":"Monitor"}, {"$set":{"precio":190.0}})
    # DELETE
    clientes.delete_one({"_id":4})

if __name__ == "__main__":
    seed()
    demo_crud()
```

**Validación:**

* Se listan ventas con `lookup` (join lógico).
* Precio de “Monitor” actualizado a 190.
* “Carlos” eliminado.

---

### 🔹 Fase 3 — **ETL con Pandas** (lectura/joins/aggregaciones)

**Objetivo:** exportar desde SQLite a CSV, cargar en **Pandas** y crear un informe.

**app/etl\_pandas.py**

```python
import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/sqlite/usuarios.db")
EXPORT = Path("data/export"); EXPORT.mkdir(parents=True, exist_ok=True)

def export_sqlite_to_csv():
    conn = sqlite3.connect(DB_PATH)
    clientes = pd.read_sql_query("SELECT * FROM clientes", conn)
    productos = pd.read_sql_query("SELECT * FROM productos", conn)
    ventas    = pd.read_sql_query("SELECT * FROM ventas", conn)
    clientes.to_csv(EXPORT/"clientes.csv", index=False)
    productos.to_csv(EXPORT/"productos.csv", index=False)
    ventas.to_csv(EXPORT/"ventas.csv", index=False)
    conn.close()

def informe_pandas():
    c = pd.read_csv(EXPORT/"clientes.csv")
    p = pd.read_csv(EXPORT/"productos.csv")
    v = pd.read_csv(EXPORT/"ventas.csv")

    df = (v.merge(c, left_on="id_cliente", right_on="id", suffixes=("","_c"))
            .merge(p, left_on="id_producto", right_on="id", suffixes=("","_p")))
    df["importe"] = df["cantidad"] * df["precio"]

    resumen_cliente = df.groupby("nombre")["importe"].sum().reset_index().sort_values("importe", ascending=False)
    resumen_producto = df.groupby("nombre_p")["cantidad"].sum().reset_index().rename(columns={"nombre_p":"producto","cantidad":"uds"})
    return df, resumen_cliente, resumen_producto

if __name__ == "__main__":
    export_sqlite_to_csv()
    df, rc, rp = informe_pandas()
    print("Detalle ventas:\n", df.head(), "\n")
    print("Importe por cliente:\n", rc, "\n")
    print("Unidades por producto:\n", rp, "\n")
```

**Validación:**

* En `data/export/` se crean `clientes.csv`, `productos.csv`, `ventas.csv`.
* Se imprime **importe total por cliente** y **unidades por producto**.

---

### 🔹 Fase 4 — **Modelos simples** con Scikit-learn

**Objetivo:** crear dos miniejercicios: 1) **clasificar** ventas “altas” vs “bajas”; 2) **predecir** precio desde cantidad (regresión).

**app/ml\_models.py**

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression
from pathlib import Path

EXPORT = Path("data/export")

def load_dataset():
    df = pd.read_csv(EXPORT/"ventas.csv")
    c  = pd.read_csv(EXPORT/"clientes.csv").rename(columns={"id":"id_cliente"})
    p  = pd.read_csv(EXPORT/"productos.csv").rename(columns={"id":"id_producto"})
    df = df.merge(c, on="id_cliente").merge(p, on="id_producto", suffixes=("","_p"))
    df["importe"] = df["cantidad"] * df["precio"]
    return df

def clasificacion_importe_alto(umbral=200.0):
    df = load_dataset()
    df["alto"] = (df["importe"] >= umbral).astype(int)
    X = df[["precio","cantidad"]].values
    y = df["alto"].values

    scaler = StandardScaler()
    Xn = scaler.fit_transform(X)

    Xtr, Xte, ytr, yte = train_test_split(Xn, y, test_size=0.3, random_state=42)
    clf = LogisticRegression().fit(Xtr, ytr)
    acc = clf.score(Xte, yte)
    return acc

def regresion_precio_desde_cantidad():
    df = load_dataset()
    X = df[["cantidad"]].values
    y = df["precio"].values
    reg = LinearRegression().fit(X, y)
    r2 = reg.score(X, y)
    pred_10 = reg.predict([[10]])[0]
    return r2, reg.coef_[0], reg.intercept_, pred_10

if __name__ == "__main__":
    acc = clasificacion_importe_alto()
    r2, coef, inter, pred = regresion_precio_desde_cantidad()
    print(f"Accuracy clasificación (importe alto): {acc:.2f}")
    print(f"Regresión precio~cantidad: R2={r2:.2f}, coef={coef:.3f}, inter={inter:.3f}, pred(10)={pred:.2f}")
```

**Validación:**

* Se imprime **accuracy** de la clasificación y métricas de la **regresión** (R², coeficiente, intercepto, predicción).

---

## ▶️ Ejecución recomendada

1. **SQLite**

   ```bash
   python -m app.sql_demo
   ```
2. **MongoDB**

   ```bash
   python -m app.mongo_demo
   ```
3. **ETL + Pandas**

   ```bash
   python -m app.etl_pandas
   ```
4. **Modelos ML**

   ```bash
   python -m app.ml_models
   ```

---

## ✅ Criterios de aceptación

* **SQLite**: DB creada, tablas con datos, CRUD y join funcionales.
* **MongoDB**: colecciones pobladas, pipeline con `lookup`, updates y deletes aplicados.
* **Pandas**: CSVs exportados, merges correctos y agregaciones calculadas.
* **Scikit-learn**: se obtiene un **accuracy** (clasificación) y **métricas** de regresión sin errores.

---

## 🧠 Reflexión final

* ¿Qué ventajas/inconvenientes has visto entre **SQL** y **MongoDB** para este caso?
* ¿Cómo cambia el **modelo de datos** al pasar de tablas a documentos?
* ¿Qué transformaciones realizaste en Pandas que serían más costosas en puro SQL?
* ¿Qué **features** añadirías para mejorar la clasificación (p. ej., *importe unitario*, *cliente*, *producto*)?

---

## 🔥 Retos opcionales

1. **Persistencia cruzada**: exporta desde Mongo a JSON y vuelve a cargarlo en SQLite.
2. **ORM**: rehaz la Fase 1 con **SQLAlchemy** y relaciones declarativas.
3. **Validación de ML**: usa **KFold** y compara modelos (LogReg vs Árbol de decisión).
4. **CLI**: crea un `main.py` con subcomandos (`sql seed`, `mongo seed`, `etl`, `ml`) usando `argparse`.