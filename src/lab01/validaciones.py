
import re

# Patrones compilados (reutilizables y performantes)
EMAIL_RE = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$')
TEL_ES_RE = re.compile(r'^\d{9}$')
PASSWORD_RE = re.compile(r'^(?=.*[A-Z])(?=.*\d).{8,}$')
PASSWORD_STRICT_RE = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$')
PASSWORD_ULTRA_ALL4_RE = re.compile(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=!]).{12,}$')

def validar_email(valor: str) -> bool:
    return EMAIL_RE.match(valor or "") is not None

def validar_telefono_es(valor: str) -> bool:
    return TEL_ES_RE.match(valor or "") is not None

def validar_password(valor: str, *, strict: bool = False) -> bool:
    patron = PASSWORD_STRICT_RE if strict else PASSWORD_RE
    return patron.match(valor or "") is not None

def validar_password_ultra_all4(valor: str) -> bool:
    return PASSWORD_ULTRA_ALL4_RE.match(valor or "") is not None

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
    print("tel ok:", validar_telefono_es("61234567"))
    print("pwd ok:", validar_password("Python123!"))
    print("pwd strict ok:", validar_password("Python123!", strict=True))
    tel_raw = "612 345 678 f"
    tel_norm = solo_digitos(tel_raw)
    ok = validar_telefono_es(tel_norm)
    print("tel ok:", tel_raw, tel_norm, ok)

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


    print("all4:", validar_password_ultra_all4('Jamon_123Alborznoz'))
    
