# 🔹 Fase 3: Decoradores y funciones anidadas aplicados a validaciones

### 🎯 Objetivo

Añadir **comportamientos transversales** a las validaciones y al procesado de formularios sin tocar su lógica interna: **logging**, **cronometraje**, **conteo de llamadas**, **memoización simple**, y **políticas** (p. ej., campos obligatorios).

---

### 🧱 Scaffold (nuevo archivo)

Crea `decoradores.py` que reutiliza lo hecho en `validaciones.py` y `funciones.py`:

```python
# decoradores.py
from functools import wraps
import time
from typing import Any, Callable, Dict, Tuple

# ---------- Decoradores genéricos ----------
def log_calls(func: Callable):
    """Log simple: nombre y argumentos."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} args={args} kwargs={kwargs}")
        res = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} -> {res}")
        return res
    return wrapper

def cronometro(func: Callable):
    """Cronometra la ejecución (ms)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            dt = (time.time() - t0) * 1000
            print(f"[TIMER] {func.__name__} tardó {dt:.2f} ms")
    return wrapper

def contador(func: Callable):
    """Cuenta cuántas veces se llamó a la función (atributo ._count)."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper._count = getattr(wrapper, "_count", 0) + 1  # type: ignore[attr-defined]
        return func(*args, **kwargs)
    wrapper._count = 0  # type: ignore[attr-defined]
    return wrapper

def memoize(func: Callable):
    """Cachea resultados por (args, kwargs) — útil en validaciones costosas."""
    cache: Dict[Tuple[Any, Tuple[Tuple[str, Any], ...]], Any] = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            return cache[key]
        res = func(*args, **kwargs)
        cache[key] = res
        return res
    return wrapper

def requiere_campos(*campos_obligatorios: str):
    """Decorador con parámetros: exige que existan claves en el dict de entrada."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Se asume primer arg es un dict de valores normalizados (ver uso más abajo)
            if not args:
                return func(*args, **kwargs)
            valores = args[0]
            faltan = [c for c in campos_obligatorios if not str(valores.get(c, "")).strip()]
            if faltan:
                raise ValueError(f"Faltan campos obligatorios: {', '.join(faltan)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ---------- Integración con nuestras funciones ----------
# Opción A: envolver validadores concretos
from validaciones import validar_email, validar_telefono_es, validar_password
from funciones import procesar_formulario, REGLAS_BASE, check_email_telefono, check_pwd_fuerte

# Decorar validadores (ejemplo; puedes elegir solo algunos)
validar_email_logged = log_calls(validar_email)
validar_telefono_es_timed = cronometro(validar_telefono_es)
validar_password_counted = contador(validar_password)  # ahora acumula ._count

# Opción B: envolver el pipeline del formulario completo
@log_calls
@cronometro
def procesar_formulario_observado(*checks, **kwargs):
    """Wrapper que añade log + timer al pipeline completo."""
    return procesar_formulario(*checks, **kwargs)

# Opción C: checks globales que usan closures (funciones anidadas)
def check_longitud_minima_factory(campo: str, n_min: int):
    """Closure que crea un check global parametrizable."""
    def check(valores: Dict[str, Any]):
        v = str(valores.get(campo, "") or "")
        return (len(v) >= n_min, f"El campo '{campo}' debe tener al menos {n_min} caracteres")
    return check

# Opción D: política de campos obligatorios usando decorador parametrizado
@requiere_campos("email", "password")
def politica_basica(valores: Dict[str, Any]):
    """Check global que simplemente retorna OK (si pasa el decorador)."""
    return True, ""

if __name__ == "__main__":
    # 1) Probar validadores decorados
    print("email ok:", validar_email_logged("user@test.com"))
    print("tel ok:", validar_telefono_es_timed("612345678"))
    print("pwd ok:", validar_password_counted("Python123!"))
    print("pwd calls:", validar_password_counted._count)  # type: ignore[attr-defined]

    # 2) Pipeline observado (log + timer) con checks
    salida = procesar_formulario_observado(
        check_email_telefono,
        check_pwd_fuerte,
        check_longitud_minima_factory("password", 8),
        reglas=REGLAS_BASE,
        email="Admin@Empresa.com",
        telefono="612 345 678",
        password="Python123!"
    )
    print("SALIDA OBSERVADA:", salida)

    # 3) Demostración de requiere_campos
    try:
        ok, msg = politica_basica({"email": "x@y.com", "password": ""})
        print(ok, msg)
    except ValueError as e:
        print("POLÍTICA:", e)
```

---

### 🧭 Pasos

1. **Implementa decoradores genéricos**: `log_calls`, `cronometro`, `contador`, `memoize`.
2. **Crea un decorador con parámetros** `requiere_campos(*campos)` para políticas básicas.
3. **Envuelve validadores seleccionados** (p. ej., log en `validar_email`, timer en `validar_telefono_es`, contador en `validar_password`).
4. **Envuelve el pipeline completo** con `procesar_formulario_observado = log_calls(cronometro(procesar_formulario))` (aquí con sintaxis `@` en una función wrapper).
5. **Usa closures** con `check_longitud_minima_factory` para crear checks globales parametrizables por campo.
6. **Ejecuta `decoradores.py`** y revisa:

   * Logs de entrada/salida.
   * Tiempos reportados.
   * Contador de llamadas en validadores.
   * Errores por política (`requiere_campos`).

---

### 🔥 Reto (opcional)

1. **`retry` con backoff**
   `@retry(n=3, backoff=0.1)` que reintente funciones de red con espera exponencial.

2. **`rate_limit`**
   `@rate_limit(calls=5, per=1.0)` que limite llamadas por ventana temporal.

3. **`cache_ttl`**
   `@cache_ttl(segundos=10)` para invalidar entradas de memoización tras X segundos.

---

### ✅ Validación (criterios de aceptación)

* `validar_email_logged("user@test.com")` muestra log y devuelve `True`.
* `validar_telefono_es_timed("612345678")` imprime el tiempo y devuelve `True`.
* Varias llamadas a `validar_password_counted(...)` incrementan `._count`.
* `procesar_formulario_observado(...)` imprime log + timer y devuelve un dict con `ok=True` para datos válidos.
* `politica_basica({"email":"x@y.com","password":""})` lanza `ValueError` → “Faltan campos obligatorios: password”.

---

## ✅ Conclusión del Laboratorio 1

**Lo que has construido:**

* Un módulo de **validaciones** con regex y normalizadores (`validaciones.py`).
* Un motor **reutilizable** de procesado de formularios con `*args` (checks globales) y `**kwargs` (campos flexibles) (`funciones.py`).
* Un conjunto de **decoradores y closures** para añadir **observabilidad** (log, tiempo, contador), **rendimiento** (memoize) y **políticas** (campos requeridos) **sin tocar** la lógica de negocio (`decoradores.py`).

**Aprendizajes clave:**

* **`re`** para validación/extracción con patrones anclados y grupos.
* **`*args` / `**kwargs`** para APIs flexibles y composición de reglas.
* **Decoradores** para aspectos transversales (logging, timing, políticas) y **closures** para generar reglas parametrizadas.

**Listo para producción**:

* El retorno estructurado de `procesar_formulario` (`ok`, `errores`, `valores`) facilita testeo e integración con UI.
* Los decoradores permiten instrumentar sin acoplar código.
* Las reglas se parametrizan sin reescribir funciones.