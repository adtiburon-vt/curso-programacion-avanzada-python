## 🔹 Reto 1 — Proteger el script con `if __name__ == "__main__"`

### 🎯 Objetivo:

Evitar que el código del script se ejecute automáticamente cuando el archivo se importa como módulo.

---

### 1. Asegúrate de que todo el código principal esté dentro de una función `main()`:

```python
# main.py

def main():
    print("Demo iniciada")
    # Aquí va toda la lógica de prueba (crear repo, usuarios, etc.)
```

---

### 2. Al final del archivo, añade esta línea:

```python
if __name__ == "__main__":
    main()
```

---

### ✅ Resultado esperado:

* Si ejecutas directamente:

  ```bash
  python main.py
  ```

  → Se imprime: `Demo iniciada`.

* Si lo importas:

  ```bash
  python -c "import main"
  ```

  → **No imprime nada**.

---

## 🔹 Reto 2 — Comprobar que `main.py` no se ejecuta al importar

### 🎯 Objetivo:

Validar que `main()` **no se ejecuta automáticamente** al hacer un `import`.

---

### 1. Ya tienes `print("Demo iniciada")` dentro de `main()`.

### 2. Desde terminal o consola interactiva, haz la prueba:

```bash
python -c "import main"
```

* Si está bien protegido con `if __name__ == "__main__"` → no debe imprimirse nada.

---

### 3. También puedes hacer esta prueba desde otro archivo, por ejemplo:

```python
# test_import.py
import main
```

Y ejecutas:

```bash
python test_import.py
```

→ No se debe imprimir nada.

---

## 🔹 Reto 3 — Mostrar el valor de `__name__`

### 🎯 Objetivo:

Entender qué valor tiene `__name__` dependiendo de cómo se ejecuta el script.

---

### 1. Dentro de la función `main()`, añade:

```python
def main():
    print("[main()] __name__ =", __name__)
```

---

### 2. Fuera de la función, justo antes del bloque `if`, añade:

```python
print("[fuera de main()] __name__ =", __name__)
```

---

### 3. Ejecuta directamente:

```bash
python main.py
```

🟢 Resultado:

```
[fuera de main()] __name__ = __main__
[main()] __name__ = __main__
```

---

### 4. Importa desde consola:

```bash
python -c "import main"
```

🔵 Resultado:

```
[fuera de main()] __name__ = main
```

(no se ejecuta `main()`)

---

# ✅ Conclusión


* Comprender y **visualizar el comportamiento real de `__name__`**.
* Aprender a **proteger scripts correctamente**.
* Ver el efecto real de **importar vs. ejecutar directamente**.
