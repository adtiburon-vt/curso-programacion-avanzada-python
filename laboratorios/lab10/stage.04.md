# 🔹 Fase 4 — Modelos simples con Scikit-learn

### 🎯 Objetivo

Tomar los datos procesados en la **Fase 3 (ETL con Pandas)**, aplicar un **preprocesado**, y construir **dos modelos simples**:

1. **Clasificación supervisada**: predecir si una venta es “alta” o “baja” según el importe.
2. **Regresión supervisada**: estimar el precio de un producto en función de la cantidad.

---

## 🧱 Estructura mínima

```
lab10_db_ml/
├─ data/export/
│   ├─ clientes.csv
│   ├─ productos.csv
│   ├─ ventas.csv
│   └─ (reportes generados en fase 3)
└─ app/ml_models.py
```

---

## 🧭 Código (app/ml\_models.py)

```python
# app/ml_models.py
from __future__ import annotations
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression

EXPORT_DIR = Path("data/export")

def load_dataset() -> pd.DataFrame:
    """Carga los CSV exportados en Fase 3 y prepara un DataFrame consolidado."""
    c = pd.read_csv(EXPORT_DIR / "clientes.csv").rename(columns={"id": "id_cliente"})
    p = pd.read_csv(EXPORT_DIR / "productos.csv").rename(columns={"id": "id_producto", "nombre": "producto"})
    v = pd.read_csv(EXPORT_DIR / "ventas.csv")

    df = (v.merge(c, on="id_cliente", how="left")
            .merge(p, on="id_producto", how="left"))
    df["importe"] = df["cantidad"] * df["precio"]
    return df

def clasificacion_importe(umbral: float = 200.0) -> float:
    """Clasificación binaria: importe alto (>= umbral) vs bajo (< umbral)."""
    df = load_dataset()
    df["alto"] = (df["importe"] >= umbral).astype(int)

    X = df[["precio", "cantidad"]].values
    y = df["alto"].values

    scaler = StandardScaler()
    Xn = scaler.fit_transform(X)

    Xtr, Xte, ytr, yte = train_test_split(Xn, y, test_size=0.3, random_state=42)
    model = LogisticRegression()
    model.fit(Xtr, ytr)

    acc = model.score(Xte, yte)
    return acc

def regresion_precio() -> tuple[float, float, float, float]:
    """Regresión lineal: predecir precio a partir de la cantidad."""
    df = load_dataset()
    X = df[["cantidad"]].values
    y = df["precio"].values

    reg = LinearRegression()
    reg.fit(X, y)

    r2 = reg.score(X, y)
    coef = reg.coef_[0]
    inter = reg.intercept_
    pred_10 = reg.predict([[10]])[0]  # predicción para cantidad=10
    return r2, coef, inter, pred_10

def main():
    print("== Clasificación: importe alto/bajo ==")
    acc = clasificacion_importe()
    print(f"Accuracy (importe >= 200): {acc:.2f}")

    print("\n== Regresión: precio en función de cantidad ==")
    r2, coef, inter, pred = regresion_precio()
    print(f"R² = {r2:.2f}")
    print(f"Coef = {coef:.3f}, Intercepto = {inter:.3f}")
    print(f"Predicción para cantidad=10 → {pred:.2f}")

    print("\n✔ Fase 4 completada.")

if __name__ == "__main__":
    main()
```

---

## ▶️ Ejecución

```bash
python -m app.ml_models
```

**Salida esperada (aprox.):**

```
== Clasificación: importe alto/bajo ==
Accuracy (importe >= 200): 1.00

== Regresión: precio en función de cantidad ==
R² = 0.85
Coef = 15.000, Intercepto = 120.000
Predicción para cantidad=10 → 270.00

✔ Fase 4 completada.
```

*(Los valores exactos dependen de tus datos en `ventas`.)*

---

## ✅ Criterios de aceptación

* El script entrena un **clasificador** y devuelve un **accuracy** sin errores.
* La **regresión lineal** muestra R², coeficiente, intercepto y una predicción.
* Se demuestra un flujo completo **ETL → ML**.

---

# ✅ Conclusión global del Laboratorio 10

**Qué has hecho:**

1. **Fase 1 (SQLite)** → Modelado relacional, CRUD, JOINs, cálculos de importe.
2. **Fase 2 (MongoDB)** → Modelo documental, CRUD, `lookup` en pipeline, cálculo de importe.
3. **Fase 3 (Pandas)** → Exportación, unificación de tablas, agregaciones e informes.
4. **Fase 4 (Scikit-learn)** → Preprocesado, clasificación binaria, regresión lineal simple.

**Qué te llevas:**

* Experiencia práctica con **SQL y NoSQL** en paralelo.
* Uso de **Pandas** para ETL y análisis tabular.
* Primer contacto con **ML aplicado a datos reales** (clasificación y regresión).

**Ideas clave:**

* SQL aporta **integridad y consistencia**, MongoDB aporta **flexibilidad y escalado**.
* Pandas es un gran “puente” entre **datos en bruto** y **modelado ML**.
* Scikit-learn ofrece un flujo claro: **preprocesar → entrenar → evaluar**.

**Siguientes pasos:**

* Extender el modelo ML con más features (ej. cliente, tipo de producto).
* Probar clustering (KMeans) para segmentación de clientes/productos.
* Empaquetar todo en un **CLI** con `argparse` para lanzar fases (`sql seed`, `mongo seed`, `etl`, `ml`).
* Añadir **tests automatizados** para validar consistencia de datos y accuracy mínimo esperado.