# 🔹 Fase 3: Agregación con `reduce`, `any`, `all`

### 🎯 Objetivo

Calcular indicadores agregados (KPI) del catálogo transformado usando `reduce`, y validar **calidad de datos** con `any`/`all`.

---

### 🧱 Scaffold (amplía `pipeline.py`)

Añade debajo de lo hecho en Fases 1–2:

```python
from functools import reduce

def kpis_catalogo(items):
    """
    items: lista de dicts con al menos: nombre, precio, stock, (opcional) precio_final
    Devuelve un dict con KPIs agregados.
    """
    # total de referencias (tras filtros)
    total_refs = len(items)

    # suma de unidades en stock
    total_unidades = reduce(lambda acc, it: acc + it["stock"], items, 0)

    # valor bruto (precio * stock)
    valor_inventario = reduce(lambda acc, it: acc + it["precio"] * it["stock"], items, 0.0)

    # si hay precio_final, calcula valor con descuento; si no, usa precio
    valor_final = reduce(
        lambda acc, it: acc + (it.get("precio_final", it["precio"])) * it["stock"],
        items,
        0.0
    )

    # media de precio unitario (evita división por cero)
    media_precio = (
        reduce(lambda acc, it: acc + it["precio"], items, 0.0) / total_refs
        if total_refs else 0.0
    )

    return {
        "total_refs": total_refs,
        "total_unidades": total_unidades,
        "valor_inventario": round(valor_inventario, 2),
        "valor_final": round(valor_final, 2),
        "media_precio": round(media_precio, 2),
    }

def calidad_datos(nombres_norm, precios_float, stock):
    """
    Valida condiciones globales con any/all sobre colecciones paralelas.
    """
    # ¿Algún precio <= 0?
    hay_precios_no_validos = any(p <= 0 for p in precios_float)

    # ¿Todos los nombres no vacíos tras normalización?
    nombres_ok = all(n.strip() for n in nombres_norm)

    # ¿Hay algún stock negativo?
    hay_stock_negativo = any(s < 0 for s in stock)

    # ¿Listas sincronizadas?
    longitudes_ok = len(nombres_norm) == len(precios_float) == len(stock)

    return {
        "hay_precios_no_validos": hay_precios_no_validos,
        "nombres_ok": nombres_ok,
        "hay_stock_negativo": hay_stock_negativo,
        "longitudes_ok": longitudes_ok,
    }

if __name__ == "__main__":
    # ---- Fase 1
    print("Original:", PRODUCTOS)
    normalizado = normalizar_lista(PRODUCTOS)
    print("Normalizado:", normalizado)
    capitalizados = list(map(lambda s: s.title(), normalizado))
    print("Capitalizados:", capitalizados)
    resumen = [(p.upper(), len(p)) for p in capitalizados]
    print("Resumen:", resumen)

    # ---- Fase 2
    precios = normalizar_precio_lista(PRECIOS)
    print("Precios:", precios)

    catalogo = combinar_catalogo(normalizado, precios, STOCK)
    print("Catálogo con stock:", catalogo)

    catalogo_desc = aplicar_descuento(catalogo, 10.0)  # 10% dto.
    print("Catálogo con descuento:", catalogo_desc)

    # ---- Fase 3
    kpis = kpis_catalogo(catalogo_desc)
    print("KPIs:", kpis)

    calidad = calidad_datos(normalizado, precios, STOCK)
    print("Calidad de datos:", calidad)
```

---

### 🧭 Pasos

1. **Agrega KPIs con `reduce`**

   * `total_unidades`, `valor_inventario` (`precio*stock`), `valor_final` (si hay descuento), `media_precio`.
2. **Valida calidad con `any`/`all`**

   * `any` para detectar **anomalías** (precio ≤ 0, stock < 0).
   * `all` para exigir condiciones **universales** (nombres no vacíos).
   * Revisa **sincronía** de listas con una comparación de longitudes.
3. **Ejecuta y revisa**

   * Debes ver KPIs coherentes con tus datos y el dict de calidad con banderas lógicas.

---

### ✅ Validación (criterios de aceptación)

* Con los datos por defecto y 10% de descuento:

  * `kpis["total_refs"]` → 4 (excluye el artículo sin stock).
  * `kpis["total_unidades"]` → `10 + 5 + 25 + 3 = 43`.
  * `kpis["valor_inventario"]` → `19.9*10 + 129*5 + 4.99*25 + 7*3 = 968.75`.
  * `kpis["valor_final"]` ≈ `valor_inventario * 0.9` (mismo cómputo pero con `precio_final`).
  * `calidad["longitudes_ok"]` → `True`, `calidad["nombres_ok"]` → `True`, y no debería haber precios ≤ 0 ni stock negativo.

---

### 🔥 Reto (opcional)

1. **KPI por “familia”**
   Si añades una lista paralela `CATEGORIAS`, calcula con `reduce` un dict `{categoria: valor_inventario}`.
   *Tip:* reduce sobre un dict acumulador: `acc | {cat: acc.get(cat, 0) + precio*stock}`.

2. **Indicadores de calidad compuestos**
   Deriva una “puntuación de calidad” `0–100` restando puntos por cada anomalía (`any`) y bonificando `all` cumplidos.

3. **Exportar resultados**
   Escribe un `save_summary(path)` que guarde KPIs y calidad en JSON/CSV (sin librerías externas).

---

## ✅ Conclusión del Laboratorio 2

**Qué has construido (pipeline completo):**

1. **Fase 1 – Normalización**
   Limpiaste y homogeneizaste **nombres** usando **comprehensions** y `lambda`.
2. **Fase 2 – Transformación/Filtrado/Combinación**
   Uniste **nombres + precios + stock** con `zip`, filtraste agotados con `filter`, y creaste precios finales con **`map`**.
3. **Fase 3 – Agregación/Validación global**
   Calculaste **KPIs** con `reduce` y comprobaste **calidad de datos** con `any`/`all`.

**Aprendizajes clave:**

* Cuándo preferir **comprehensions** frente a `map`/`filter`.
* Patrones de **pipelines funcionales**: normalizar → transformar → combinar → agregar.
* Uso de `reduce` para acumular valores y construir **estructuras** (dicts).
* Validación global ágil con `any`/`all`.

**Listo para evolución:**

* Puedes enchufar fuentes reales (CSV/JSON), añadir **categorías**, y exportar a **Parquet/CSV**.
* Encapsula cada sección en funciones puras para testear con `unittest` o `pytest`.