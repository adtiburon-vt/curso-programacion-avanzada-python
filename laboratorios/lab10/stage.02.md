# 🔹 Fase 2 — CRUD en MongoDB con `pymongo`

### 🎯 Objetivo

Crear y poblar colecciones `clientes`, `productos`, `ventas`; realizar **CRUD** y una **consulta agregada** con `lookup` (equivalente a JOIN) y cálculo de `importe`.

---

## 🧱 Estructura mínima

```
lab10_db_ml/
├─ app/
│  ├─ sql_demo.py
│  └─ mongo_demo.py
└─ data/
   └─ sqlite/usuarios.db
```

> Requisito: tener un MongoDB accesible (local: `mongodb://localhost:27017` o Atlas).

---

## 🧭 Código (app/mongo\_demo.py)

```python
# app/mongo_demo.py
from __future__ import annotations
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Tuple

MONGO_URI = "mongodb://localhost:27017"
DB_NAME   = "lab10"

def get_collections() -> Tuple[Collection, Collection, Collection]:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    clientes  = db["clientes"]
    productos = db["productos"]
    ventas    = db["ventas"]
    return clientes, productos, ventas

def seed():
    clientes, productos, ventas = get_collections()
    # Limpieza
    clientes.delete_many({})
    productos.delete_many({})
    ventas.delete_many({})

    # Semillas (usamos _id explícito para facilitar lookups)
    clientes.insert_many([
        {"_id": 1, "nombre": "Ana",   "email": "ana@test.com"},
        {"_id": 2, "nombre": "Luis",  "email": "luis@test.com"},
        {"_id": 3, "nombre": "Marta", "email": "marta@test.com"},
    ])
    productos.insert_many([
        {"_id": 1, "nombre": "Portátil", "precio": 900.0},
        {"_id": 2, "nombre": "Monitor",  "precio": 180.0},
        {"_id": 3, "nombre": "Teclado",  "precio": 25.0},
    ])
    ventas.insert_many([
        {"id_cliente": 1, "id_producto": 1, "cantidad": 1},
        {"id_cliente": 1, "id_producto": 2, "cantidad": 1},
        {"id_cliente": 2, "id_producto": 3, "cantidad": 2},
        {"id_cliente": 3, "id_producto": 2, "cantidad": 1},
    ])

def demo_crud():
    clientes, productos, ventas = get_collections()

    # CREATE
    print("→ CREATE: añadir cliente 'Carlos'")
    clientes.insert_one({"_id": 4, "nombre": "Carlos", "email": "carlos@test.com"})

    # READ simple
    print("\n→ READ: listar clientes (solo nombre/email)")
    for doc in clientes.find({}, {"_id": 0, "nombre": 1, "email": 1}).sort("nombre", 1):
        print("   ", doc)

    # UPDATE
    print("\n→ UPDATE: actualizar precio de 'Monitor' a 190.0")
    productos.update_one({"nombre": "Monitor"}, {"$set": {"precio": 190.0}})

    # DELETE
    print("\n→ DELETE: eliminar cliente 'Carlos'")
    clientes.delete_one({"_id": 4})

def ventas_detalle_pipeline():
    _, _, ventas = get_collections()
    pipeline = [
        {"$lookup": {
            "from": "clientes",
            "localField": "id_cliente",
            "foreignField": "_id",
            "as": "cliente"
        }},
        {"$lookup": {
            "from": "productos",
            "localField": "id_producto",
            "foreignField": "_id",
            "as": "producto"
        }},
        {"$unwind": "$cliente"},
        {"$unwind": "$producto"},
        {"$addFields": {"importe": {"$multiply": ["$cantidad", "$producto.precio"]}}},
        {"$project": {
            "_id": 0,
            "cliente": "$cliente.nombre",
            "producto": "$producto.nombre",
            "cantidad": 1,
            "precio": "$producto.precio",
            "importe": 1
        }},
        {"$sort": {"cliente": 1, "producto": 1}}
    ]
    print("\n→ Ventas (aggregation + lookup):")
    for doc in ventas.aggregate(pipeline):
        print("   ", doc)

if __name__ == "__main__":
    seed()
    demo_crud()
    ventas_detalle_pipeline()
    print("\n✔ Fase 2 completada.")
```

---

## ▶️ Cómo ejecutar

Desde la raíz del proyecto:

```bash
python -m app.mongo_demo
```

**Salida esperada (aprox.):**

```
→ CREATE: añadir cliente 'Carlos'

→ READ: listar clientes (solo nombre/email)
    {'nombre': 'Ana', 'email': 'ana@test.com'}
    {'nombre': 'Luis', 'email': 'luis@test.com'}
    {'nombre': 'Marta', 'email': 'marta@test.com'}
    {'nombre': 'Carlos', 'email': 'carlos@test.com'}

→ UPDATE: actualizar precio de 'Monitor' a 190.0

→ DELETE: eliminar cliente 'Carlos'

→ Ventas (aggregation + lookup):
    {'cliente': 'Ana', 'producto': 'Monitor', 'cantidad': 1, 'precio': 180.0, 'importe': 180.0}
    {'cliente': 'Ana', 'producto': 'Portátil', 'cantidad': 1, 'precio': 900.0, 'importe': 900.0}
    {'cliente': 'Luis', 'producto': 'Teclado', 'cantidad': 2, 'precio': 25.0, 'importe': 50.0}
    {'cliente': 'Marta', 'producto': 'Monitor', 'cantidad': 1, 'precio': 190.0, 'importe': 190.0}

✔ Fase 2 completada.
```

*(El precio de “Monitor” en el último registro refleja el `update` a 190.0.)*

---

## ✅ Criterios de aceptación

* Colecciones `clientes`, `productos`, `ventas` creadas y pobladas.
* CRUD ejecutado: **insert**, **find** con proyección/orden, **update**, **delete**.
* Pipeline con **`$lookup`** y **`$addFields`** produce `cliente, producto, cantidad, precio, importe` ordenado por cliente.

---

## 🔧 Notas y buenas prácticas

* Si usas **MongoDB Atlas**, cambia `MONGO_URI` por tu cadena de conexión.
* Para **índices**, podrías añadir:

  ```python
  ventas.create_index([("id_cliente", 1)])
  ventas.create_index([("id_producto", 1)])
  clientes.create_index("email", unique=True)
  ```
* Para tests reproducibles, `seed()` siempre limpia y repuebla.