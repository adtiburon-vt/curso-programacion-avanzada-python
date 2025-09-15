# ✅ Solución — Decoradores genéricos

## 1) `log_calls`

**Idea:** imprimir antes y después, devolver el resultado.

```python
from functools import wraps

def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} args={args} kwargs={kwargs}")
        res = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} -> {res}")
        return res
    return wrapper
```

---

## 2) `cronometro`

**Idea:** medir con `time.time()` y asegurar el print con `finally`.

```python
import time
from functools import wraps

def cronometro(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            dt = (time.time() - t0) * 1000
            print(f"[TIMER] {func.__name__} tardó {dt:.2f} ms")
    return wrapper
```

---

## 3) `contador`

**Idea:** usar un atributo en el `wrapper`.

```python
from functools import wraps

def contador(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper._count = getattr(wrapper, "_count", 0) + 1
        return func(*args, **kwargs)
    wrapper._count = 0
    return wrapper
```

---

## 4) `memoize`

**Idea:** cache por `(args, kwargs ordenados)`.

```python
from functools import wraps
from typing import Any, Dict, Tuple

def memoize(func):
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
```

---

## 5) `requiere_campos(*campos)`

**Idea:** validar campos presentes y no vacíos en el **primer arg** (dict).

```python
from functools import wraps

def requiere_campos(*campos_obligatorios: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not args:
                return func(*args, **kwargs)
            valores = args[0]
            faltan = [c for c in campos_obligatorios if not str(valores.get(c, "")).strip()]
            if faltan:
                raise ValueError(f"Faltan campos obligatorios: {', '.join(faltan)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

---

# ✅ Solución — Closures (funciones anidadas)

## `check_longitud_minima_factory`

**Idea:** devolver un check `(ok, msg)` parametrizado por campo y mínimo.

```python
from typing import Any, Dict

def check_longitud_minima_factory(campo: str, n_min: int):
    def check(valores: Dict[str, Any]):
        v = str(valores.get(campo, "") or "")
        return (len(v) >= n_min, f"El campo '{campo}' debe tener al menos {n_min} caracteres")
    return check
```

---

# 🔗 Ejemplos de integración mínima

> Solo para comprobar que tus decoradores se aplican bien a funciones existentes.

```python
# Supón que ya existen:
# from validaciones import validar_email, validar_telefono_es, validar_password

validar_email_logged = log_calls(validar_email)
validar_telefono_es_timed = cronometro(validar_telefono_es)
validar_password_counted = contador(validar_password)

@requiere_campos("email", "password")
def politica_basica(valores: Dict[str, Any]):
    return True, ""
```

---

# 🧪 Checks rápidos (esperados)

```python
assert validar_email_logged("user@test.com") is True
assert validar_telefono_es_timed("612345678") is True

_ = validar_password_counted("Python123!")
_ = validar_password_counted("Python123!")
assert getattr(validar_password_counted, "_count", 0) == 2

ok, msg = politica_basica({"email": "a@b.com", "password": "xx"})
assert ok is True

try:
    politica_basica({"email": "a@b.com", "password": ""})
    raise AssertionError("Debió lanzar ValueError")
except ValueError as e:
    assert "Faltan campos obligatorios" in str(e)

check8 = check_longitud_minima_factory("password", 8)
assert check8({"password": "Python123"})[0] is True
assert check8({"password": "abc"})[0] is False
```

---

# 🌶️ Retos opcionales (soluciones simples)

## 1) `@retry(n=3, backoff=0.1)`

```python
import time
from functools import wraps

def retry(n=3, backoff=0.1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            intento = 0
            delay = backoff
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    intento += 1
                    if intento >= n:
                        raise
                    time.sleep(delay)
                    delay *= 2
        return wrapper
    return decorator
```

## 2) `@rate_limit(calls=5, per=1.0)`

```python
import time
from collections import deque
from functools import wraps

def rate_limit(calls: int, per: float):
    def decorator(func):
        eventos = deque()
        @wraps(func)
        def wrapper(*args, **kwargs):
            ahora = time.time()
            while eventos and (ahora - eventos[0]) > per:
                eventos.popleft()
            if len(eventos) >= calls:
                espera = per - (ahora - eventos[0])
                time.sleep(max(0, espera))
            eventos.append(time.time())
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## 3) `@cache_ttl(segundos=10)`

```python
import time
from functools import wraps
from typing import Any, Dict, Tuple

def cache_ttl(segundos: float = 10.0):
    def decorator(func):
        cache: Dict[Tuple[Any, Tuple[Tuple[str, Any], ...]], Tuple[float, Any]] = {}
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            ahora = time.time()
            if key in cache:
                ts, val = cache[key]
                if (ahora - ts) <= segundos:
                    return val
            res = func(*args, **kwargs)
            cache[key] = (ahora, res)
            return res
        return wrapper
    return decorator
```

---

## 🧠 Puntos de aprendizaje que deben reconocer al comparar

* El patrón `@wraps` se repite para **conservar metadatos** de la función.
* Los decoradores **no tocan la lógica** original; añaden comportamiento alrededor.
* Las **closures** (factories) generan validadores **parametrizados** sin duplicar código.
* `memoize`/`cache_ttl` muestran **trade-offs**: claves hashables y funciones “puras”.