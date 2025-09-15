# class A:
#     def accion(self):
#         print("A empieza")
#         super().accion()
#         print("A termina")

# class B(A):
#     def accion(self):
#         print("B empieza")
#         super().accion()
#         print("B termina")

# class C(A):
#     def accion(self):
#         print("C empieza")
#         super().accion()
#         print("C termina")

# class D(B, C):
#     def accion(self):
#         print("D empieza")
#         super().accion()
#         print("D termina")

# # ---- Ejecutamos ----
# d = D()
# d.accion()

# print("MRO:", D.mro())



class A: 
    def saludar(self): return "A"

class B(A): 
    def saludar(self): return "B"

class C(A): 
    def saludar(self): return "C"

class D(B, C): 
    pass

d = D()
print(d.saludar())     # "B" según el MRO
print(D.mro())         # [D, B, C, A, object]





# controller_decorators.py
from typing import Any, Tuple

class ControllerMixin:
    """Comportamientos comunes para controladores."""
    base_path: str = "/"

    def json(self, data: Any, status: int = 200) -> Tuple[int, dict, str]:
        # Respuesta JSON minimalista (simulada)
        import json
        body = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        return status, headers, body

    def handle(self, method: str, **kwargs):
        """Despacha por nombre de método HTTP: get/post/put/delete..."""
        method = method.lower()
        if not hasattr(self, method):
            return self.json({"error": "method not allowed"}, 405)
        return getattr(self, method)(**kwargs)


class AuthMixin:
    def require_auth(self, token: str):
        if token != "secret":
            return self.json({"error": "unauthorized"}, 401)
        return None


def controller(base_path: str = "/"):
    """
    Decorador de clase que:
      1) Inyecta ControllerMixin por herencia.
      2) Fija base_path en la clase resultante.
    """
    def _decorar(cls):
        # Construimos una nueva clase que hereda de (ControllerMixin, cls)
        # para que el mixin aporte utilidades y pueda sobreescribir si hiciera falta.
        nombre = cls.__name__
        attrs = dict(cls.__dict__)
        # Limpiezas opcionales para evitar warnings en type()
        attrs.pop("__dict__", None)
        attrs.pop("__weakref__", None)

        Nueva = type(nombre, (ControllerMixin, cls), attrs)
        Nueva.base_path = base_path
        return Nueva
    return _decorar



def auth():
    """
    Decorador de clase que:
      1) Inyecta AuthMixin por herencia.
    """
    def _decorar(cls):
        # Construimos una nueva clase que hereda de (ControllerMixin, cls)
        # para que el mixin aporte utilidades y pueda sobreescribir si hiciera falta.
        nombre = cls.__name__
        attrs = dict(cls.__dict__)
        # Limpiezas opcionales para evitar warnings en type()
        attrs.pop("__dict__", None)
        attrs.pop("__weakref__", None)


        Nueva = type(nombre, (AuthMixin, cls), attrs)
        return Nueva
    return _decorar








@auth()            # añade require_auth
@controller(base_path="/users")    # añade json/handle y base_path
class UsersControllerSecure:
    def get(self, user_id: int, token: str):
        if (resp := self.require_auth(token)) is not None:
            return resp
        return self.json({"id": user_id, "name": "Ana"})