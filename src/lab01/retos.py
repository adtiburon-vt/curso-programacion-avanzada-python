# validaciones.py
import re
from typing import Iterable

# =========================
# Patrones compilados
# =========================
# Email con TLD alfabético de 2 a 24 caracteres
EMAIL_RE = re.compile(r'^[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,24}$')

# Teléfono español: 9 dígitos (se recomienda normalizar antes con solo_digitos)
TEL_ES_RE = re.compile(r'^\d{9}$')

# Password mínima: 8, al menos 1 mayúscula y 1 dígito
PASSWORD_RE = re.compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')

# Password estricta: 8+, al menos 1 mayúscula, 1 dígito y 1 símbolo permitido
PASSWORD_STRICT_RE = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$')

# Símbolos considerados (puedes ampliar)
_SIMBOLOS = r"""~`!@#$%^&*()_\-+={[}\]|\\:;"'<,>.?/=§±"""

# =========================
# Validadores
# =========================
def validar_email(valor: str) -> bool:
    return EMAIL_RE.match(valor or "") is not None

def validar_telefono_es(valor: str) -> bool:
    """Valida exactamente 9 dígitos (p. ej. móviles y fijos en ES)."""
    return TEL_ES_RE.match(valor or "") is not None

def validar_password(valor: str, *, strict: bool = False) -> bool:
    patron = PASSWORD_STRICT_RE if strict else PASSWORD_RE
    return patron.match(valor or "") is not None

def validar_password_extra(valor: str, *, min_len: int = 12, min_clases: int = 2) -> bool:
    """
    Reto opcional:
      - Longitud mínima configurable (por defecto 12).
      - Debe contener al menos `min_clases` de estas 4 categorías:
        mayúscula, minúscula, dígito, símbolo.
    Nota: Usa lógica en Python para contar clases (más claro que una regex compleja).
    """
    s = valor or ""
    if len(s) < min_len:
        return False

    clases = 0
    if re.search(r'[A-Z]', s): clases += 1
    if re.search(r'[a-z]', s): clases += 1
    if re.search(r'\d', s):    clases += 1
    if re.search(rf'[{re.escape(_SIMBOLOS)}]', s): clases += 1

    return clases >= min_clases

def validar_cp_es(valor: str) -> bool:
    """
    Códigos postales ES:
      - 5 dígitos.
      - Los dos primeros representan provincia 01–52 (00 es inválido).
    """
    s = (valor or "").strip()
    if not re.fullmatch(r'\d{5}', s):
        return False
    prov = int(s[:2])  # "01" -> 1
    return 1 <= prov <= 52

# =========================
# Helpers genéricos
# =========================
def normalizar_espacios(s: str) -> str:
    """Colapsa espacios múltiples a uno y recorta extremos."""
    return re.sub(r'\s+', ' ', (s or '').strip())

def solo_digitos(s: str) -> str:
    """Extrae solo dígitos (útil para normalizar teléfonos)."""
    return re.sub(r'\D+', '', s or '')

# =========================
# Utilidades de prueba
# =========================
def _assert_many(pares: Iterable[tuple[bool, bool]], *, titulo: str = "Checks") -> None:
    ok = all(exp == res for exp, res in pares)
    estado = "OK" if ok else "FALLO"
    print(f"[{estado}] {titulo}")
    if not ok:
        for i, (exp, res) in enumerate(pares, 1):
            if exp != res:
                print(f"  - Caso #{i}: esperado={exp}, obtenido={res}")

if __name__ == "__main__":
    # =========================
    # Pruebas rápidas manuales
    # =========================
    print("email ok:", validar_email("usuario@test.com"))
    print("tel ok:", validar_telefono_es("612345678"))
    print("pwd ok:", validar_password("Python123!"))
    print("pwd strict ok:", validar_password("Python123!", strict=True))

    # Criterios de aceptación del enunciado
    _assert_many([
        (True,  validar_email("usuario@test.com")),
        (False, validar_email("mal@com")),
    ], titulo="Email – criterios aceptación")

    _assert_many([
        (True,  validar_telefono_es("612345678")),
        (False, validar_telefono_es("12345678")),
    ], titulo="Teléfono ES – criterios aceptación")

    _assert_many([
        (False, validar_password("python123")),     # falta mayúscula
        (True,  validar_password("Python123")),
        (True,  validar_password("Python123!", strict=True)),
        (False, validar_password("Python123",  strict=True)),
    ], titulo="Password – criterios aceptación")

    # =========================
    # Demo simple (opcional)
    # =========================
    ejemplos = {
        "email": ["a@b.com", "mal@com", "user.name@mail.co", "x@y", "user@mail.technology"],
        "tel": ["612345678", "612 345 678", "12345", "612-345-678"],
        "pwd": ["python123", "Python123", "Python123!", "Short1!"],
        "cp":  ["01001", "52006", "00000", "99000", "28013"]
    }

    print("\n== DEMO EMAIL ==")
    for e in ejemplos["email"]:
        print(f"{e:>24} -> {validar_email(e)}")

    print("\n== DEMO TEL ==")
    for t in ejemplos["tel"]:
        print(f"{t:>24} -> {validar_telefono_es(solo_digitos(t))}  (normalizado='{solo_digitos(t)}')")

    print("\n== DEMO PASSWORD ==")
    for p in ejemplos["pwd"]:
        print(f"{p:>24} -> base:{validar_password(p)}  strict:{validar_password(p, strict=True)}  extra12>=2clases:{validar_password_extra(p)}")

    print("\n== DEMO CP ES ==")
    for cp in ejemplos["cp"]:
        print(f"{cp:>24} -> {validar_cp_es(cp)}")

    # Ejemplos extra para la password del reto (>=12 y >=2 clases)
    extras = [
        "abcdefghijkl",      # solo minúsculas -> False
        "ABCDEFGHIJKL",      # solo mayúsculas -> False
        "AAAAAAAAAAAA1",     # mayúsculas + dígitos (2 clases) -> True
        "Abcdefghijk1",      # mayúsc+minúsc+dígito (3 clases) -> True
        "Abcdefghij1!",      # 4 clases -> True
        "Short1!"            # <12 -> False
    ]
    print("\n== DEMO PASSWORD EXTRA (min_len=12, min_clases=2) ==")
    for p in extras:
        print(f"{p:>24} -> {validar_password_extra(p)}")
