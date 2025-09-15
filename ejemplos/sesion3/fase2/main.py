# main.py
from app.modelos import Usuario

if __name__ == "__main__":
    # Caso feliz
    u = Usuario("Ana", "ANA@Test.com", rol="admin")
    u.set_password("secreta!")
    print(u.presentarse(), u.rol, u.check_password("secreta!"))

    # Email inválido
    try:
        u.email = "sin-arroba"
    except ValueError as e:
        print("Email inválido OK:", e)

    # Rol inválido
    try:
        u.rol = "superuser"
    except ValueError as e:
        print("Rol inválido OK:", e)

    # desde_dict
    datos = {"nombre": "Luis", "email": "luis@test.com", "rol": "invitado", "activo": False}
    u2 = Usuario.desde_dict(datos)
    print(repr(u2))

    # Password mínima
    try:
        u2.set_password("123")
    except ValueError as e:
        print("Password corta OK:", e)