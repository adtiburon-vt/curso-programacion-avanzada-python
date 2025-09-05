# 🔹 Fase 2: Funciones reutilizables con `*args` y `**kwargs`

### 🎯 Objetivo

Construir funciones **flexibles y reutilizables** que reciban formularios dinámicos con `**kwargs`, apliquen **validadores** y **normalizadores**, y permitan **componer reglas** mediante `*args` (checks extra) sin reescribir lógica.

---

### 🧱 Scaffold (estructura inicial)

Crea `funciones.py` (reutilizará lo hecho en `validaciones.py` de la Fase 1):

```python
from typing import Callable, Dict, List, Tuple, Any
from validaciones import (
    validar_email, validar_telefono_es, validar_password,
    normalizar_espacios, solo_digitos
)

# Tipos base
Validador = Callable[[Any], bool]
Normalizador = Callable[[Any], Any]
ResultadoCampo = Tuple[bool, List[str], Any]  # (ok, errores, valor_normalizado)

# --- Normalizadores de ejemplo ---
def norm_email(v: str) -> str:
    return normalizar_espacios(v).lower()

def norm_tel_es(v: str) -> str:
    return solo_digitos(v)

def norm_pwd(v: str) -> str:
    return (v or "").strip()

# --- Validadores “en forma de función” para composición ---
def v_email(v: str) -> bool:
    return validar_email(v)

def v_tel_es(v: str) -> bool:
    return validar_telefono_es(v)

def v_pwd_relajada(v: str) -> bool:
    return validar_password(v, strict=False)

def v_pwd_estricta(v: str) -> bool:
    return validar_password(v, strict=True)

# --- Reglas por campo (editable por cada formulario) ---
REGLAS_BASE: Dict[str, Dict[str, Any]] = {
    "email": {
        "normalizadores": [norm_email],
        "validadores": [(v_email, "Email inválido")],
        "requerido": True,
    },
    "telefono": {
        "normalizadores": [norm_tel_es],
        "validadores": [(v_tel_es, "Teléfono ES inválido (9 dígitos)")],
        "requerido": False,
    },
    "password": {
        "normalizadores": [norm_pwd],
        "validadores": [(v_pwd_relajada, "Contraseña no cumple requisitos básicos")],
        "requerido": True,
    },
}

def aplicar_normalizadores(valor: Any, normalizadores: List[Normalizador]) -> Any:
    for f in normalizadores or []:
        valor = f(valor)
    return valor

def validar_valor(valor: Any, validadores: List[Tuple[Validador, str]]) -> ResultadoCampo:
    errores: List[str] = []
    ok = True
    for val_fn, msg in validadores or []:
        if not val_fn(valor):
            ok = False
            errores.append(msg)
    return ok, errores, valor

# ------------------------------------------------------------
# API REUTILIZABLE
# ------------------------------------------------------------
def procesar_formulario(*checks_globales: Callable[[Dict[str, Any]], Tuple[bool, str]],
                        reglas: Dict[str, Dict[str, Any]] = None,
                        **campos) -> Dict[str, Any]:
    """
    Procesa un formulario con reglas por campo y checks globales opcionales.
    - *checks_globales: funciones que reciben el dict de campos normalizados y devuelven (ok, error_msg)
    - reglas: diccionario de reglas por campo (normalizadores, validadores, requerido)
    - **campos: pares clave/valor del formulario
    Retorna dict con:
      {
        "ok": bool,
        "errores": {campo: [mensajes...] , "_global": [mensajes...]},
        "valores": {campo: valor_normalizado}
      }
    """
    reglas = reglas or REGLAS_BASE
    errores: Dict[str, List[str]] = {}
    valores_norm: Dict[str, Any] = {}

    # 1) Normalizar y validar cada campo definido en 'reglas'
    for campo, spec in reglas.items():
        requerido = spec.get("requerido", False)
        normalizadores = spec.get("normalizadores", [])
        validadores = spec.get("validadores", [])

        bruto = campos.get(campo, "")
        valor = aplicar_normalizadores(bruto, normalizadores)

        if requerido and (valor is None or str(valor).strip() == ""):
            errores.setdefault(campo, []).append("Campo requerido")
            valores_norm[campo] = valor
            continue

        ok, errs, val_out = validar_valor(valor, validadores)
        if not ok:
            errores.setdefault(campo, []).extend(errs)
        valores_norm[campo] = val_out

    # 2) Checks globales (e.g., coherencia entre campos)
    global_errs: List[str] = []
    for chk in checks_globales or []:
        ok, msg = chk(valores_norm)
        if not ok and msg:
            global_errs.append(msg)

    if global_errs:
        errores["_global"] = global_errs

    ok_total = len(errores) == 0
    return {"ok": ok_total, "errores": errores, "valores": valores_norm}

# ------------------------------------------------------------
# Checks globales de ejemplo (se pasan por *args)
# ------------------------------------------------------------
def check_email_telefono(valores: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Ejemplo: exige que exista teléfono si el email es de dominio corporativo.
    """
    email = valores.get("email", "")
    tel = valores.get("telefono", "")
    if email.endswith("@empresa.com") and not tel:
        return False, "Si el email es corporativo, el teléfono es obligatorio"
    return True, ""

def check_pwd_fuerte(valores: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Ejemplo: para perfiles de alto privilegio, podrías exigir v_pwd_estricta.
    Aquí solo muestra cómo podrías reforzar.
    """
    pwd = valores.get("password", "")
    if not v_pwd_estricta(pwd):
        return False, "Password debe ser estricta (mayúscula, dígito y símbolo)"
    return True, ""

if __name__ == "__main__":
    # Ejemplo 1: formulario básico
    salida = procesar_formulario(
        check_email_telefono,
        reglas=REGLAS_BASE,
        email="  Usuario@TEST.com ",
        telefono="612 345 678",
        password="Python123!"
    )
    print("BÁSICO:", salida)

    # Ejemplo 2: sin teléfono con email corporativo (falla check global)
    salida2 = procesar_formulario(
        check_email_telefono,
        reglas=REGLAS_BASE,
        email="admin@empresa.com",
        password="Python123!"
    )
    print("CORP SIN TEL:", salida2)

    # Ejemplo 3: password estricta requerida globalmente
    salida3 = procesar_formulario(
        check_pwd_fuerte,
        reglas=REGLAS_BASE,
        email="root@empresa.com",
        telefono="612-345-678",
        password="Python123"   # sin símbolo -> debe fallar check global
    )
    print("PWD FUERTE:", salida3)
```

---

### 🧭 Pasos

1. **Define normalizadores** por campo (email → `lower` + trim; teléfono → solo dígitos; password → trim).
2. **Declara validadores** como funciones simples que devuelvan `True/False`.
3. **Crea `REGLAS_BASE`** con lista de normalizadores, lista de `(validador, mensaje)` y si es `requerido`.
4. **Implementa `procesar_formulario`** para:

   * Recibir **checks globales** vía `*args`.
   * Aceptar el formulario dinámicamente via `**campos`.
   * Normalizar, validar por campo y luego ejecutar checks globales.
   * Devolver `{"ok", "errores", "valores"}`.
5. **Añade checks globales** de ejemplo (coherencia entre campos, política de contraseñas reforzada).
6. **Ejecuta los ejemplos** (`python funciones.py`) y revisa salidas.

---

### 🔥 Reto (opcional)

1. **Campos dinámicos con alias**
   Permite mapear sinónimos: p.ej., `tel`, `telefono`, `phone` → mismo campo interno `"telefono"`.
   *Tip:* añade un paso previo que normalice claves del dict `**campos` con un mapa `ALIAS = {"tel": "telefono", "phone": "telefono"}`.

2. **Errores por prioridad**
   Haz que cada validador pueda tener severidad (`"warning" | "error"`) y que el “ok global” sea `True` si solo hay *warnings*.
   *Tip:* usa `(val_fn, msg, nivel)` y separa en `errores` vs `avisos`.

3. **Hooks**
   Añade `before_validate(valores)` y `after_validate(resultado)` como callbacks opcionales que se pasan por `**kwargs` a `procesar_formulario` (p.ej., para logging centralizado).

---

### ✅ Validación (criterios de aceptación)

* **Caso feliz**:
  Entrada: `email="  Usuario@TEST.com "`, `telefono="612 345 678"`, `password="Python123!"`
  → `ok=True`, `errores={}`, `valores={"email":"usuario@test.com", "telefono":"612345678", "password":"Python123!"}`

* **Email corporativo sin teléfono** (con `check_email_telefono` activo):
  → `ok=False`, `errores["_global"]` con el mensaje correspondiente.

* **Password no estricta** (con `check_pwd_fuerte` activo):
  → `ok=False`, `errores["_global"]` indicando política de password estricta.

---

### 🧹 Buenas prácticas

* Mantén **normalizadores** y **validadores** como funciones **puras** (sin efectos secundarios).
* Separa **reglas** de la **lógica** (`REGLAS_BASE` editable sin tocar `procesar_formulario`).
* Reutiliza `*args` para **checks globales**; usa `**kwargs` para **configuración** opcional.
* Devuelve un resultado **estructurado** (ok/errores/valores) apto para tests y para UI.

