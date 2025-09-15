# Enfoque

* Quiero **“extender”** una clase usando un **decorador de clase**.
* El decorador devolverá **otra clase** que hereda de un **mixin** común (`ControllerMixin`) + la clase original.
* Así, `UsersController` “gana” métodos (p. ej., `json`, `handle`) y un `base_path`.

---

# Paso a paso 

```python
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
```

```python
# app.py
from controller_decorators import controller

@controller(base_path="/users")
class UsersController:
    # ¡OJO! No hereda explícitamente de ControllerMixin,
    # el decorador se encarga de “extenderla”.

    # Handlers estilo REST (usarás handle("GET"...), handle("POST"...))
    def get(self, user_id: int):
        # 'json' viene del mixin
        return self.json({"id": user_id, "name": "Ana"})

    def post(self, name: str):
        return self.json({"status": "created", "name": name}, 201)


if __name__ == "__main__":
    uc = UsersController()
    print("Base path:", uc.base_path)  # -> /users

    print(uc.handle("GET", user_id=1))   # (200, {...}, '{"id":1,"name":"Ana"}')
    print(uc.handle("POST", name="Pepe"))# (201, {...}, '{"status":"created","name":"Pepe"}')
    print(uc.handle("DELETE"))           # (405, {...}, '{"error":"method not allowed"}')
```

---

## Bonus (opcional): Añadir otro mixin con un decorador genérico

```python
# extra_mixins.py
def extend_with(*mixins):
    """Devuelve un decorador que añade mixins a la clase."""
    def _decorar(cls):
        nombre = cls.__name__
        attrs = dict(cls.__dict__)
        attrs.pop("__dict__", None)
        attrs.pop("__weakref__", None)
        # MRO: primero los mixins, luego la clase original
        return type(nombre, (*mixins, cls), attrs)
    return _decorar


class AuthMixin:
    def require_auth(self, token: str):
        if token != "secret":
            return self.json({"error": "unauthorized"}, 401)
        return None
```

```python
# app_auth.py
from controller_decorators import controller
from extra_mixins import extend_with, AuthMixin

@extend_with(AuthMixin)            # añade require_auth
@controller(base_path="/users")    # añade json/handle y base_path
class UsersControllerSecure:
    def get(self, user_id: int, token: str):
        if (resp := self.require_auth(token)) is not None:
            return resp
        return self.json({"id": user_id, "name": "Ana"})
```

---

### Idea clave

* Un **decorador de clase** recibe la clase y **devuelve otra clase** (posiblemente con herencia adicional), lo que es perfecto para “extender” sin tocar el `class` original.
* El orden en `type(Nueva, (Mixin, Original), attrs)` define la **MRO**: métodos del **Mixin** se buscan antes que los de la clase original.
