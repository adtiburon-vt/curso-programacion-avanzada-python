# ✅ Implementaciones básicas (map, filter, zip)

### 1) Normalizar precios con `map`

```python
def normalizar_precio_lista(precios):
    # Convierte cada string a float (quita espacios y cambia coma por punto)
    return list(map(to_float, precios))
```

### 2) Combinar con `zip` y filtrar sin stock

```python
def combinar_catalogo(nombres_norm, precios_float, stock):
    """
    Une nombre-precio-stock y filtra items con stock > 0.
    Devuelve una lista de dicts legibles.
    """
    combinado = zip(nombres_norm, precios_float, stock)
    con_stock = filter(lambda t: t[2] > 0, combinado)
    return [{"nombre": n, "precio": p, "stock": s} for (n, p, s) in con_stock]
```

### 3) Aplicar un descuento con `map`

```python
def aplicar_descuento(items, porcentaje: float):
    """
    Añade clave precio_final = precio * (1 - porcentaje/100)
    Redondeado a 2 decimales.
    """
    factor = (100.0 - porcentaje) / 100.0
    return list(map(lambda it: {**it, "precio_final": round(it["precio"] * factor, 2)}, items))
```

---

# 🔥 Retos (soluciones sencillas)

## Reto 1 — Varios descuentos encadenados (`*porcentajes`)

### Explicación breve

* Convertimos cada porcentaje en su **factor** (`(100-p)/100`).
* Multiplicamos todos los factores (composición de descuentos).
* Aplicamos el factor total a cada item.

```python
from functools import reduce

def aplicar_descuentos(items, *porcentajes):
    """
    Aplica secuencialmente varios % de descuento (p.ej., 10, 5).
    Equivale a multiplicar factores: 0.90 * 0.95, etc.
    """
    if not porcentajes:
        return items  # sin cambios
    factor_total = reduce(lambda acc, p: acc * ((100.0 - p) / 100.0), porcentajes, 1.0)
    return [{**it, "precio_final": round(it["precio"] * factor_total, 2)} for it in items]
```

---

## Reto 2 — Top-N por **valor de inventario** (`precio * stock`)

### Explicación breve

* Calculamos `valor = precio * stock`.
* Ordenamos descendente por ese valor.
* Devolvemos los `n` primeros.

```python
def top_n(items, n=2):
    """
    Ordena por valor de inventario (precio * stock) desc y devuelve los n más altos.
    """
    ordenados = sorted(items, key=lambda it: it["precio"] * it["stock"], reverse=True)
    return ordenados[:max(0, n)]
```

---

## Reto 3 — `zip` “seguro” (listas de distinta longitud)

### Opción A (simple): truncar con `zip` (ya trunca por defecto)

```python
def combinar_catalogo_trunc(nombres_norm, precios_float, stock):
    """
    Variante explícita: usa zip que trunca al mínimo largo.
    """
    return combinar_catalogo(nombres_norm, precios_float, stock)  # zip ya trunca
```

### Opción B (completa): usar `zip_longest` y descartar incompletos

```python
from itertools import zip_longest

def combinar_catalogo_seguro(nombres_norm, precios_float, stock):
    """
    Usa zip_longest y descarta tuplas con valores None (incompletos).
    """
    combinado = zip_longest(nombres_norm, precios_float, stock, fillvalue=None)
    completos = filter(lambda t: None not in t, combinado)
    con_stock = filter(lambda t: t[2] > 0, completos)
    return [{"nombre": n, "precio": p, "stock": s} for (n, p, s) in con_stock]
```

---

# 🧪 Mini-pruebas rápidas (puedes dejarlas en el `__main__`)

```python
if __name__ == "__main__":
    # ---- Fase 1 (ya la tenías)
    print("Original:", PRODUCTOS)
    normalizado = normalizar_lista(PRODUCTOS)
    print("Normalizado:", normalizado)
    capitalizados = list(map(lambda s: s.title(), normalizado))
    print("Capitalizados:", capitalizados)
    resumen = [(p.upper(), len(p)) for p in capitalizados]
    print("Resumen:", resumen)

    # ---- Fase 2
    precios = normalizar_precio_lista(PRECIOS)
    print("Precios:", precios)  # [19.9, 9.5, 129.0, 4.99, 7.0]

    catalogo = combinar_catalogo(normalizado, precios, STOCK)
    print("Catálogo con stock:", catalogo)

    catalogo_10 = aplicar_descuento(catalogo, 10.0)
    print("Catálogo -10%:", catalogo_10)

    catalogo_10_5 = aplicar_descuentos(catalogo, 10, 5)  # 10% y luego 5%
    print("Catálogo -10% y -5%:", catalogo_10_5)

    print("Top 2 por valor inventario:", top_n(catalogo))
```

---

# 🧹 Buenas prácticas (recordatorio corto)

* `zip` **asume mismo orden** entre listas (documenta el origen de datos).
* Prefiere **nuevos dicts** con `{**it, ...}` a mutar in-place (más fácil de testear).
* Si hay riesgo de longitudes distintas, usa la versión **segura** o valida antes.


