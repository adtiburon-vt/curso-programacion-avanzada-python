# Reto 1 — **Campos dinámicos con alias**

Mapea sinónimos (`tel`, `phone` → `telefono`) antes de procesar reglas.

```python
# --- Alias de campos ---
ALIAS = {
    "tel": "telefono",
    "phone": "telefono",
    "movil": "telefono",
    "mail": "email",
    "correo": "email",
    "pwd": "password",
    "pass": "password",
}

def _normalizar_claves(**campos) -> dict:
    """
    Devuelve un nuevo dict con claves normalizadas via ALIAS (case-insensitive).
    Las claves sin alias permanecen igual.
    """
    out = {}
    for k, v in campos.items():
        key = ALIAS.get(k.lower(), k)
        out[key] = v
    return out

def procesar_formulario_aliases(*checks_globales,
                                reglas: dict = None,
                                **campos) -> dict:
    """
    Variante con soporte de alias de campos.
    """
    # 0) Normalizar claves
    campos = _normalizar_claves(**campos)

    # Reutiliza tu lógica original a partir de aquí:
    reglas = reglas or REGLAS_BASE
    errores, valores_norm = {}, {}

    for campo, spec in reglas.items():
        req = spec.get("requerido", False)
        norms = spec.get("normalizadores", [])
        vals  = spec.get("validadores", [])

        bruto = campos.get(campo, "")
        valor = aplicar_normalizadores(bruto, norms)

        if req and (valor is None or str(valor).strip() == ""):
            errores.setdefault(campo, []).append("Campo requerido")
            valores_norm[campo] = valor
            continue

        ok, errs, val_out = validar_valor(valor, vals)
        if not ok:
            errores.setdefault(campo, []).extend(errs)
        valores_norm[campo] = val_out

    global_errs = []
    for chk in checks_globales or []:
        ok, msg = chk(valores_norm)
        if not ok and msg:
            global_errs.append(msg)
    if global_errs:
        errores["_global"] = global_errs

    return {"ok": not errores, "errores": errores, "valores": valores_norm}
```

---

# Reto 2 — **Errores por prioridad (warning | error)**

Permite que cada validador declare severidad. El `ok` global solo falla si hay **errors** (warnings no bloquean).

```python
from typing import Literal, Tuple, List, Any, Callable, Dict
Nivel = Literal["warning", "error"]
ValidadorConNivel = Tuple[Callable[[Any], bool], str, Nivel]
ResultadoCampoDet = Tuple[bool, List[str], List[str], Any]  # ok, errores, avisos, valor

def validar_valor_con_nivel(valor: Any, validadores: List[ValidadorConNivel]) -> ResultadoCampoDet:
    errores: List[str] = []
    avisos:  List[str] = []
    ok = True
    for val_fn, msg, nivel in validadores or []:
        passed = val_fn(valor)
        if not passed:
            if nivel == "error":
                ok = False
                errores.append(msg)
            else:
                avisos.append(msg)
    return ok, errores, avisos, valor

def procesar_formulario_prioridades(*checks_globales,
                                    reglas: Dict[str, Dict[str, Any]] = None,
                                    **campos) -> Dict[str, Any]:
    """
    Variante con severidades. Estructura de reglas:
      "validadores": [(fn, "mensaje", "error"|"warning"), ...]
    """
    reglas = reglas or REGLAS_BASE
    errores: Dict[str, List[str]] = {}
    avisos:  Dict[str, List[str]] = {}
    valores_norm: Dict[str, Any] = {}

    for campo, spec in reglas.items():
        req = spec.get("requerido", False)
        norms = spec.get("normalizadores", [])
        vals  = spec.get("validadores", [])

        bruto = campos.get(campo, "")
        valor = aplicar_normalizadores(bruto, norms)

        if req and (valor is None or str(valor).strip() == ""):
            errores.setdefault(campo, []).append("Campo requerido")
            valores_norm[campo] = valor
            continue

        ok, errs, warns, val_out = validar_valor_con_nivel(valor, vals)
        if errs:
            errores.setdefault(campo, []).extend(errs)
        if warns:
            avisos.setdefault(campo, []).extend(warns)
        valores_norm[campo] = val_out

    global_errs: List[str] = []
    global_warns: List[str] = []
    for chk in checks_globales or []:
        ok, msg, nivel = chk(valores_norm)  # espera (ok, msg, "error"|"warning")
        if not ok and msg:
            if nivel == "error":
                global_errs.append(msg)
            else:
                global_warns.append(msg)

    if global_errs:
        errores["_global"] = global_errs
    if global_warns:
        avisos["_global"] = global_warns

    ok_total = len(errores) == 0  # warnings no bloquean
    return {"ok": ok_total, "errores": errores, "avisos": avisos, "valores": valores_norm}
```

**Ejemplo de reglas con severidad:**

```python
REGLAS_PRIORIDAD = {
    "email": {
        "normalizadores": [norm_email],
        "validadores": [
            (v_email, "Email inválido", "error"),
        ],
        "requerido": True,
    },
    "telefono": {
        "normalizadores": [norm_tel_es],
        "validadores": [
            (v_tel_es, "Formato de teléfono no reconocido", "warning"),  # p. ej. lo aceptas pero avisas
        ],
        "requerido": False,
    },
    "password": {
        "normalizadores": [norm_pwd],
        "validadores": [
            (v_pwd_relajada, "Contraseña débil", "error"),
            (v_pwd_estricta, "Se recomienda contraseña estricta", "warning"),
        ],
        "requerido": True,
    },
}

# Check global con nivel:
def check_email_corporativo_tel(valores: Dict[str, Any]):
    email = valores.get("email", "")
    tel = valores.get("telefono", "")
    if email.endswith("@empresa.com") and not tel:
        return False, "Para correo corporativo, añade teléfono", "error"
    return True, "", "warning"  # da igual este nivel si ok=True
```

---

# Reto 3 — **Hooks `before_validate` y `after_validate`**

Soporta callbacks para instrumentación, logging, side-effects (sin romper la pureza de validadores/normalizadores).

```python
from typing import Callable, Optional

BeforeHook = Callable[[Dict[str, Any], Dict[str, Dict[str, Any]]], None]
AfterHook  = Callable[[Dict[str, Any]], None]

def procesar_formulario_hooks(*checks_globales,
                              reglas: Dict[str, Dict[str, Any]] = None,
                              before_validate: Optional[BeforeHook] = None,
                              after_validate:  Optional[AfterHook]  = None,
                              **campos) -> Dict[str, Any]:
    """
    Variante con hooks:
      - before_validate(valores_brutos, reglas) -> None
      - after_validate(resultado_dict) -> None
    """
    reglas = reglas or REGLAS_BASE

    # Llamada pre-validación
    if before_validate:
        try:
            before_validate(dict(campos), reglas)
        except Exception as e:
            # No bloquear procesamiento por errores del hook
            pass

    errores: Dict[str, List[str]] = {}
    valores_norm: Dict[str, Any] = {}

    # Validación por campo (igual que la base)
    for campo, spec in reglas.items():
        req = spec.get("requerido", False)
        norms = spec.get("normalizadores", [])
        vals  = spec.get("validadores", [])

        bruto = campos.get(campo, "")
        valor = aplicar_normalizadores(bruto, norms)

        if req and (valor is None or str(valor).strip() == ""):
            errores.setdefault(campo, []).append("Campo requerido")
            valores_norm[campo] = valor
            continue

        ok, errs, val_out = validar_valor(valor, vals)
        if not ok:
            errores.setdefault(campo, []).extend(errs)
        valores_norm[campo] = val_out

    # Checks globales
    global_errs: List[str] = []
    for chk in checks_globales or []:
        ok, msg = chk(valores_norm)
        if not ok and msg:
            global_errs.append(msg)
    if global_errs:
        errores["_global"] = global_errs

    resultado = {"ok": len(errores) == 0, "errores": errores, "valores": valores_norm}

    # Llamada post-validación
    if after_validate:
        try:
            after_validate(dict(resultado))
        except Exception:
            pass

    return resultado
```

**Ejemplo de uso de hooks:**

```python
def mi_before(valores, reglas):
    # p. ej., logging o rellenar valores por defecto
    if "telefono" not in valores:
        valores["telefono"] = ""  # solo para observación; no muta el flujo principal

def mi_after(resultado):
    # p. ej., enviar métricas o auditoría
    print("[AUDIT] ok?", resultado["ok"], "errores:", list(resultado["errores"].keys()))

salida = procesar_formulario_hooks(
    check_email_telefono,   # mismos checks de tu base si quieres
    reglas=REGLAS_BASE,
    before_validate=mi_before,
    after_validate=mi_after,
    email="admin@empresa.com",
    password="Python123!"
)
```

---

## Notas rápidas

* Puedes **combinar** estos retos si lo deseas (e.g., alias + severidades + hooks) fusionando las variantes en un único `procesar_formulario`
* Mantén `REGLAS_BASE`, `aplicar_normalizadores` y `validar_valor` (o sus variantes) en tu módulo para reusar entre versiones.
