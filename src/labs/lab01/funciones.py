from typing import Callable, Dict, List, Tuple, Any
from validaciones import (
    validar_email,
    validar_telefono_es,
    validar_password,
    normalizar_espacios,
    solo_digitos
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

def procesar_con_alias(*checks_globales: Callable[[Dict[str, Any]], Tuple[bool, str]],
                        reglas: Dict[str, Dict[str, Any]] = None,
                        **campos) -> Dict[str, Any]:
    campos_formateados = {}
    d_names = campos.get('ALIAS', {})
    for campo in campos:
        nombre_nuevo = d_names.get(campo, campo)
        campos_formateados[nombre_nuevo] = campos.get(campo)
    # print(campos_formateados)
    return procesar_formulario(*checks_globales, reglas=reglas, **campos_formateados)


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
        password="Python123!",
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

    salida_alias = procesar_con_alias(
        check_email_telefono,
        reglas=REGLAS_BASE,
        email="  Usuario@TEST.com ",
        tel="612 345 678",
        password="Python123!",
        ALIAS={"tel": "telefono"}
    )
    print("CON ALIAS:", salida_alias)