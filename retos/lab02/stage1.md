# 🔹 Reto 1 — Diccionario `{producto_normalizado: longitud}`

### ✅ Explicación

1. Partimos de la lista **ya normalizada** (todo minúsculas, sin espacios extra).
2. Usamos un **dict comprehension** para asociar cada producto con su longitud.

### 📝 Código

```python
def productos_a_diccionario(datos):
    normalizados = [p.strip().lower() for p in datos]
    return {p: len(p) for p in normalizados}
```

### 🔍 Ejemplo de uso

```python
print(productos_a_diccionario(PRODUCTOS))
# {'teclado usb': 11, 'ratón inalámbrico': 18, 'monitor 24''': 12, 'cable hdmi': 10, 'alfombrilla': 11}
```

---

# 🔹 Reto 2 — Eliminar duplicados con set comprehension

### ✅ Explicación

1. Convertimos la lista normalizada en un **set**, que elimina duplicados automáticamente.
2. Si lo queremos como lista otra vez, podemos envolverlo en `list()`.

### 📝 Código

```python
def quitar_duplicados(datos):
    normalizados = [p.strip().lower() for p in datos]
    return {p for p in normalizados}  # devuelve un set
```

### 🔍 Ejemplo de uso

```python
print(quitar_duplicados(PRODUCTOS))
# {'teclado usb', 'ratón inalámbrico', "monitor 24''", 'cable hdmi', 'alfombrilla'}
```

---

# 🔹 Reto 3 — Buscar productos por letra inicial

### ✅ Explicación

1. Normalizamos todos los productos.
2. Usamos una **list comprehension** con condición (`if`).
3. Filtramos solo los que empiezan por la letra indicada.

### 📝 Código

```python
def buscar_productos(datos, letra):
    normalizados = [p.strip().lower() for p in datos]
    return [p for p in normalizados if p.startswith(letra.lower())]
```

### 🔍 Ejemplo de uso

```python
print(buscar_productos(PRODUCTOS, "c"))
# ['cable hdmi']
print(buscar_productos(PRODUCTOS, "a"))
# ['alfombrilla']
```