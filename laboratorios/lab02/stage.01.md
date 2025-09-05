# 🔹 Fase 1: Normalización de datos con `lambda` y list comprehensions

### 🎯 Objetivo

Practicar el uso de **funciones `lambda`** y **list comprehensions** para limpiar y transformar un dataset inicial de cadenas de texto (ejemplo: lista de productos).

---

### 🧱 Scaffold (estructura inicial)

Crea un archivo `pipeline.py` con la siguiente base:

```python
# pipeline.py

# Dataset inicial de ejemplo (simula datos desordenados de un CSV)
PRODUCTOS = [
    "   Teclado USB   ",
    "RATÓN inalámbrico",
    " monitor 24'' ",
    "CABLE HDMI ",
    " alfombrilla  "
]

def normalizar_lista(datos):
    # TODO: limpiar espacios y pasar a minúsculas
    pass

if __name__ == "__main__":
    print("Original:", PRODUCTOS)
    print("Normalizado:", normalizar_lista(PRODUCTOS))
```

---

### 🧭 Pasos

1. **Eliminar espacios y homogenizar a minúsculas**

   * Implementa `normalizar_lista` usando **list comprehension** y `str.strip()`, `str.lower()`.

   ```python
   def normalizar_lista(datos):
       return [item.strip().lower() for item in datos]
   ```

2. **Transformación extra con `lambda`**

   * Usa `map` + `lambda` para poner la primera letra de cada palabra en mayúscula.

   ```python
   normalizado = normalizar_lista(PRODUCTOS)
   capitalizados = list(map(lambda s: s.title(), normalizado))
   print("Capitalizados:", capitalizados)
   ```

3. **Encadenar comprehensions**

   * Genera una nueva lista con los nombres en mayúsculas y su longitud:

   ```python
   resumen = [(p.upper(), len(p)) for p in capitalizados]
   print("Resumen:", resumen)
   ```

4. **Ejecuta y revisa**

   ```bash
   python pipeline.py
   ```

   * Comprueba que la salida muestre la lista original, la normalizada, la capitalizada y el resumen con longitudes.

---

### 🔥 Reto (opcional)

1. A partir de `PRODUCTOS`, genera un diccionario `{producto_normalizado: longitud}` usando **dict comprehension**.
2. Quita duplicados de la lista usando un **set comprehension**.
3. Escribe una función `buscar_productos(letra)` que devuelva una lista de los productos cuyo nombre empieza por esa letra.

---

### ✅ Validación

* **Entrada:**
  `["   Teclado USB   ", "RATÓN inalámbrico", " monitor 24'' ", "CABLE HDMI ", " alfombrilla  "]`

* **Salida esperada tras normalización:**
  `["teclado usb", "ratón inalámbrico", "monitor 24''", "cable hdmi", "alfombrilla"]`

* **Capitalizados:**
  `["Teclado Usb", "Ratón Inalámbrico", "Monitor 24''", "Cable Hdmi", "Alfombrilla"]`

* **Resumen:**
  `[("TECLADO USB", 11), ("RATÓN INALÁMBRICO", 18), ("MONITOR 24''", 12), ("CABLE HDMI", 10), ("ALFOMBRILLA", 11)]`

---

### 🧹 Buenas prácticas

* Usa comprehensions cuando la transformación sea **simple y legible**.
* Prefiere `map` con `lambda` para pasos cortos, pero si la expresión crece, usa una función normal.
* Devuelve siempre una **nueva lista** en vez de mutar la original (facilita testeo y depuración).