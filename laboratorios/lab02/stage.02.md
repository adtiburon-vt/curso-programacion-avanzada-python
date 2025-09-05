# 🔹 Fase 2: Filtros y combinaciones con `map`, `filter`, `zip`

### 🎯 Objetivo

Aplicar `map`, `filter` y `zip` para transformar, filtrar y **combinar** colecciones relacionadas (p. ej., nombres, precios y stock) dentro del mismo pipeline.

---

### 🧱 Scaffold (amplía `pipeline.py`)

Añade debajo de lo hecho en Fase 1:

```python
# Datos “paralelos” (mismo orden que PRODUCTOS)
PRECIOS = [" 19.90 ", "9,50", "129.00", " 4.99", "7.00"]
STOCK   = [10, 0, 5, 25, 3]  # unidades

def to_float(s: str) -> float:
    return float(s.strip().replace(",", "."))

def normalizar_precio_lista(precios):
    # TODO: map -> float limpio
    pass

def combinar_catalogo(nombres_norm, precios_float, stock):
    """
    Devuelve una lista de tuplas/dicts uniendo nombre-precio-stock,
    filtrando los artículos sin stock (>0).
    """
    # TODO: zip + filter (stock > 0)
    pass

def aplicar_descuento(items, porcentaje: float):
    """Devuelve items con un precio_final tras aplicar % descuento."""
    # TODO: map con dict actualizado
    pass

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
```

---

### 🧭 Pasos

1. **Normaliza precios con `map`**
   Convierte `PRECIOS` a `float`:

   ```python
   def normalizar_precio_lista(precios):
       return list(map(to_float, precios))
   ```

2. **Combina con `zip` y filtra con `filter`**
   Une `nombre`, `precio`, `stock` y descarta `stock == 0`:

   ```python
   def combinar_catalogo(nombres_norm, precios_float, stock):
       combinado = zip(nombres_norm, precios_float, stock)
       con_stock = filter(lambda t: t[2] > 0, combinado)
       # Devuelve dicts legibles
       return [{"nombre": n, "precio": p, "stock": s} for (n, p, s) in con_stock]
   ```

3. **Aplica un descuento con `map`**
   Genera un nuevo catálogo con `precio_final`:

   ```python
   def aplicar_descuento(items, porcentaje: float):
       factor = (100.0 - porcentaje) / 100.0
       return list(map(lambda it: {**it, "precio_final": round(it["precio"] * factor, 2)}, items))
   ```

4. **Ejecuta y revisa**

   ```bash
   python pipeline.py
   ```

   Comprueba que se imprimen: precios normalizados, catálogo sin agotados, y catálogo con precio final.

---

### 🔥 Reto (opcional)

1. **Varios descuentos encadenados**
   Crea `aplicar_descuentos(items, *porcentajes)` que aplique secuencialmente varios % (p. ej. 10, 5).
   *Tip:* convierte `porcentajes` a un factor acumulado con un bucle o `functools.reduce`.

2. **Top-N por valor en inventario**
   Añade `top_n(items, n=2)` que ordene por `precio * stock` y devuelva los `n` más valiosos.

3. **Validación de integridad con `zip` “seguro”**
   Si las listas no tienen la misma longitud, trátalo (p. ej., trunca con `zip`, o usa `itertools.zip_longest` y descarta incompletos).

---

### ✅ Validación (criterios de aceptación)

* **Normalización de precios:**
  `[" 19.90 ", "9,50", "129.00", " 4.99", "7.00"] → [19.9, 9.5, 129.0, 4.99, 7.0]`

* **Catálogo con stock:**
  Con `PRODUCTOS` normalizados de Fase 1 y `STOCK = [10, 0, 5, 25, 3]`, el catálogo debe **excluir** el artículo con stock 0 (el 2º, “ratón inalámbrico”).
  Ejemplo esperado (orden y redondeos pueden variar):

  ```python
  [
    {"nombre": "teclado usb", "precio": 19.9, "stock": 10},
    {"nombre": "monitor 24''", "precio": 129.0, "stock": 5},
    {"nombre": "cable hdmi", "precio": 4.99, "stock": 25},
    {"nombre": "alfombrilla", "precio": 7.0, "stock": 3}
  ]
  ```

* **Catálogo con descuento 10%:**
  Añade `precio_final` = `precio * 0.90` redondeado a 2 decimales.

---

### 🧹 Buenas prácticas

* Con `zip`, todas las listas deben tener **mismo orden**; documenta la fuente de datos.
* Prefiere **comprehensions** para colecciones nuevas si son más legibles que `map`/`filter`.
* Evita mutaciones: devuelve **nuevos dicts** con `{**it, ...}` (facilita tests).
* Separa pasos en funciones pequeñas para poder **testear** cada transformación.