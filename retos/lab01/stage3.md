## `decoradores.py` (base completo)

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
    """Decorador con parámetros: exige que existan claves no vacías en el dict de entrada."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Se asume primer arg es un dict de valores (p. ej., valores normalizados del formulario)
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
# Puedes decorar validadores concretos o el pipeline completo del formulario
from validaciones import validar_email, validar_telefono_es, validar_password
from funciones import procesar_formulario, REGLAS_BASE, check_email_telefono, check_pwd_fuerte

# A) Decorar validadores (ejemplo; usa los que quieras)
validar_email_logged = log_calls(validar_email)
validar_telefono_es_timed = cronometro(validar_telefono_es)
validar_password_counted = contador(validar_password)  # acumula ._count

# B) Envolver el pipeline del formulario completo (observabilidad transversal)
@log_calls
@cronometro
def procesar_formulario_observado(*checks, **kwargs):
    """Wrapper que añade log + timer al pipeline completo."""
    return procesar_formulario(*checks, **kwargs)

# C) Checks globales con closures (funciones anidadas parametrizables)
def check_longitud_minima_factory(campo: str, n_min: int):
    """Closure que crea un check global parametrizable por campo y longitud."""
    def check(valores: Dict[str, Any]):
        v = str(valores.get(campo, "") or "")
        ok = len(v) >= n_min
        msg = f"El campo '{campo}' debe tener al menos {n_min} caracteres"
        return ok, ("" if ok else msg)
    return check

# D) Política de campos obligatorios usando decorador parametrizado
@requiere_campos("email", "password")
def politica_basica(valores: Dict[str, Any]):
    """Check global que retorna OK si pasa el decorador (si no, lanza ValueError)."""
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

## 🔥 Retos opcionales (cada uno por separado)

### 1) `@retry(n=3, backoff=0.1)`

Reintenta la función ante excepción, con backoff exponencial.

```python
def retry(n: int = 3, backoff: float = 0.1, exceptions: Tuple[type, ...] = (Exception,)):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = backoff
            intento = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    intento += 1
                    if intento >= n:
                        raise
                    time.sleep(delay)
                    delay *= 2  # exponencial
        return wrapper
    return decorator
```

**Uso:**

```python
@retry(n=3, backoff=0.2)
def llamada_red():
    ...
```

---

### 2) `@rate_limit(calls=5, per=1.0)`

Limita número de llamadas por ventana temporal.

```python
from collections import deque

def rate_limit(calls: int, per: float):
    """
    Permite 'calls' invocaciones cada 'per' segundos.
    Sencillo y best-effort (no thread-safe).
    """
    def decorator(func: Callable):
        ventana = deque()  # timestamps
        @wraps(func)
        def wrapper(*args, **kwargs):
            ahora = time.time()
            # retirar llamadas fuera de ventana
            while ventana and ahora - ventana[0] > per:
                ventana.popleft()
            if len(ventana) >= calls:
                esperar = per - (ahora - ventana[0])
                if esperar > 0:
                    time.sleep(esperar)
                # limpiar de nuevo por si el tiempo ya pasó
                ahora = time.time()
                while ventana and ahora - ventana[0] > per:
                    ventana.popleft()
            ventana.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

**Uso:**

```python
@rate_limit(calls=5, per=1.0)
def consulta_api(...):
    ...
```

---

### 3) `@cache_ttl(segundos=10)`

Memoización con caducidad (TTL).

```python
def cache_ttl(segundos: float = 10.0):
    """
    Cachea por clave (args, kwargs) con expiración.
    """
    def decorator(func: Callable):
        cache: Dict[Any, Tuple[float, Any]] = {}  # key -> (ts_guardado, valor)
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            ahora = time.time()
            if key in cache:
                ts, val = cache[key]
                if ahora - ts < segundos:
                    return val
            res = func(*args, **kwargs)
            cache[key] = (ahora, res)
            return res
        return wrapper
    return decorator
```

**Uso:**

```python
@cache_ttl(segundos=15)
def validar_caro(...):
    ...
```