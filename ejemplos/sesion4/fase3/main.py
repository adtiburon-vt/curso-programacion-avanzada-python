# main.py
from app.modelos import AdminConLogger, Moderador

if __name__ == "__main__":
    a = AdminConLogger("Root", "root@corp.com")
    print(a.presentarse())           # debería loguear la llamada
    a.activar()                      # logs antes y después gracias al mixin

    m = Moderador("Lucía", "lucia@test.com", nivel=2, activo=False)
    print(m)                         # [MODERADOR-N2] ...
    m.activar()                      # (no loguea, no hereda del mixin)

    print("MRO AdminConLogger:", AdminConLogger.mro())