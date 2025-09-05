# 🔹 Fase 1: Validación con expresiones regulares

### 🎯 Objetivo

Implementar validadores para **email**, **teléfono** (9 dígitos ES) y **password** (mín. 8, 1 mayúscula, 1 dígito; opcional: 1 carácter especial), usando `re`, con funciones reutilizables y tests rápidos.

---

### 🧱 Scaffold (estructura inicial)

Crea el archivo `validaciones.py`:

```python
import re

# Patrones compilados (reutilizables y performantes)
EMAIL_RE = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$')
TEL_ES_RE = re.compile(r'^\d{9}$')
PASSWORD_RE = re.compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')
PASSWORD_STRICT_RE = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$')

def validar_email(valor: str) -> bool:
    return EMAIL_RE.match(valor or "") is not None

def validar_telefono_es(valor: str) -> bool:
    return TEL_ES_RE.match(valor or "") is not None

def validar_password(valor: str, *, strict: bool = False) -> bool:
    patron = PASSWORD_STRICT_RE if strict else PASSWORD_RE
    return patron.match(valor or "") is not None

# Helpers genéricos
def normalizar_espacios(s: str) -> str:
    """Colapsa espacios múltiples a uno y recorta extremos."""
    return re.sub(r'\s+', ' ', (s or '').strip())

def solo_digitos(s: str) -> str:
    """Extrae solo dígitos (útil para normalizar teléfonos)."""
    return re.sub(r'\D+', '', s or '')

if __name__ == "__main__":
    # Pruebas rápidas manuales
    print("email ok:", validar_email("usuario@test.com"))
    print("tel ok:", validar_telefono_es("612345678"))
    print("pwd ok:", validar_password("Python123!"))
    print("pwd strict ok:", validar_password("Python123!", strict=True))
```

---

### 🧭 Pasos

1. **Crear patrones y funciones de validación**

   * Compila los patrones (`EMAIL_RE`, `TEL_ES_RE`, `PASSWORD_RE`, `PASSWORD_STRICT_RE`).
   * Implementa `validar_email`, `validar_telefono_es`, `validar_password`.

2. **Añadir normalizadores (opcional pero recomendado)**

   * `normalizar_espacios`: para limpiar entradas de formularios.
   * `solo_digitos`: para permitir teléfonos tipeados con espacios o guiones y validarlos tras limpiar.
   * Ejemplo de uso:

     ```python
     tel_raw = "612 345 678"
     tel_norm = solo_digitos(tel_raw)
     ok = validar_telefono_es(tel_norm)
     ```

3. **Pruebas rápidas (CLI)**

   * Ejecuta:

     ```bash
     python validaciones.py
     ```
   * Debes ver `True` en todos los casos “ok”.

4. **(Opcional) Modo “demo” con entradas**
   Añade al final:

   ```python
   # Demo simple
   ejemplos = {
       "email": ["a@b.com", "mal@com", "user.name@mail.co", "x@y"],
       "tel": ["612345678", "612 345 678", "12345", "612-345-678"],
       "pwd": ["python123", "Python123", "Python123!", "Short1!"]
   }

   for e in ejemplos["email"]:
       print(e, "->", validar_email(e))
   for t in ejemplos["tel"]:
       print(t, "->", validar_telefono_es(solo_digitos(t)))
   for p in ejemplos["pwd"]:
       print(p, "->", validar_password(p), "(strict)", validar_password(p, strict=True))
   ```

---

### 🔥 Reto (opcional)

1. **Password aún más estricta**: mínimo 12 chars y **dos** clases especiales (mayúscula, minúscula, dígito, símbolo).
   *Tip:* usa lookaheads adicionales y `{12,}`.
2. **Códigos postales ES** (5 dígitos; los dos primeros 01–52): valida con regex + rango posterior en Python.
3. **Email con TLDs largos**: admite TLD de 2–24 caracteres alfabéticos.

---

### ✅ Validación (criterios de aceptación)

* `validar_email("usuario@test.com")` → `True`; `validar_email("mal@com")` → `False`.
* `validar_telefono_es("612345678")` → `True`; `validar_telefono_es("12345678")` → `False`.
* `validar_password("python123")` → `False` (no mayúscula).
* `validar_password("Python123")` → `True`.
* `validar_password("Python123!", strict=True)` → `True`; `validar_password("Python123", strict=True)` → `False`.

---

### 🧹 Buenas prácticas

* Compila patrones reutilizados (`re.compile`).
* Ancla validaciones (`^...$`) cuando deba coincidir **toda** la cadena.
* Usa `re.escape` si interpolas contenido del usuario dentro de un patrón.
* Evita `.*` “codicioso”; usa cuantificadores específicos o `?` (lazy) cuando aplique.

---

### ➕ Extensiones (para la siguiente fase)

* Exporta estas funciones desde `validaciones.py` para usarlas en `funciones.py` (Fase 2).
* Prepara un pequeño diccionario de “formulario” que luego pasarás a una función genérica con `**kwargs`.

