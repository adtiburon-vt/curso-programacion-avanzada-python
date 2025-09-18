def validar_email(email: str) -> bool:
    email = (email or "").strip().lower()
    return "@" in email and "." in email and not (email.startswith("@") or email.endswith("@"))