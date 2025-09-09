# Reto 1 — Password “aún más estricta”

### Opción 1 (recomendada): **mínimo 12** y **todas las 4 clases**

(mayúscula, minúscula, dígito y símbolo)

```python
# Password ultra: ≥12 y debe tener A-Z, a-z, 0-9 y símbolo
PASSWORD_ULTRA_ALL4_RE = re.compile(
    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{12,}$'
)

def validar_password_ultra_all4(valor: str) -> bool:
    return PASSWORD_ULTRA_ALL4_RE.match(valor or "") is not None
```

> Cumple exactamente la idea de “más estricta”: largo + 4 clases.

---

### Opción 2 (alternativa): **mínimo 12** y **al menos 3 de 4 clases**

(sirve si prefieres flexibilidad; es más permisiva que la anterior)

```python
# ≥12 y al menos 3 de estas 4: A-Z, a-z, 0-9, símbolo
PASSWORD_ULTRA_3OF4_RE = re.compile(
    r'^(?=.{12,}$)(?:'
    r'(?=(?:.*[A-Z]))(?=(?:.*[a-z]))(?=(?:.*\d))|'
    r'(?=(?:.*[A-Z]))(?=(?:.*[a-z]))(?=(?:.*[@#$%^&+=!]))|'
    r'(?=(?:.*[A-Z]))(?=(?:.*\d))(?=(?:.*[@#$%^&+=!]))|'
    r'(?=(?:.*[a-z]))(?=(?:.*\d))(?=(?:.*[@#$%^&+=!]))'
    r').*$'
)

def validar_password_ultra_3of4(valor: str) -> bool:
    return PASSWORD_ULTRA_3OF4_RE.match(valor or "") is not None
```

---

# Reto 2 — Códigos postales ES (5 dígitos; dos primeros 01–52)

```python
CP_ES_RE = re.compile(r'^\d{5}$')

def validar_cp_es(valor: str) -> bool:
    s = valor or ""
    if CP_ES_RE.match(s) is None:
        return False
    prov = int(s[:2])  # '01'->1 ... '52'->52
    return 1 <= prov <= 52
```

> Nota: 01–52 cubre provincias (incluye Ceuta=51 y Melilla=52).

---

# Reto 3 — Email con TLDs largos (2–24 letras)

```python
# Acepta TLDs de 2 a 24 letras (p.ej., .international)
EMAIL_TLD24_RE = re.compile(
    r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,24}$'
)

def validar_email_tld_largo(valor: str) -> bool:
    return EMAIL_TLD24_RE.match(valor or "") is not None
```

> Mantiene un patrón robusto y simple; si necesitas validar reglas
> de dominio más estrictas (p. ej., guiones no al inicio/fin de cada
> etiqueta), dímelo y te paso una variante más canónica.

---

## (Opcional) Pequeños helpers útiles

```python
def solo_digitos(s: str) -> str:
    return re.sub(r'\D+', '', s or '')
```