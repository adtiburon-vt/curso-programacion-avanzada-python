* Evito duplicidades y errores de coherencia centralizando permisos por rol.
* Hago `desde_dict` una **factory** que devuelve la subclase adecuada.
* Defino **igualdad y hash por email** para usar objetos en `set`/`dict`.
* En el repositorio, añado **persistencia JSON** sin filtrar contraseñas.
* Verifico todo en `main.py` con **pruebas mínimas** y asserts.

---

# 1) `app/modelos.py` — Cambios paso a paso

## 1.1. Catálogo central de permisos

**Qué:** Añadir una constante `CATALOGO_PERMISOS`.
**Por qué:** Evitar duplicar listas de permisos en varias clases y tener una “fuente de verdad” única.

```diff
+ from typing import Final
+
+ # --- Catálogo central de permisos por rol ---
+ CATALOGO_PERMISOS: Final[dict[str, list[str]]] = {
+     "admin":    ["ver", "crear", "editar", "borrar"],
+     "usuario":  ["ver"],
+     "invitado": ["ver"],
+ }
```

## 1.2. `Usuario.permisos()` delega al catálogo

**Qué:** Cambiar la implementación para que lea del catálogo.
**Por qué:** Si mañana cambian permisos, se actualiza en un único sitio.

```diff
 class Usuario(BaseUsuario):
@@
-    # Permisos por defecto del rol "usuario"
-    def permisos(self) -> list[str]:
-        return ["ver"]
+    # Permisos por defecto según el catálogo central
+    def permisos(self) -> list[str]:
+        return list(CATALOGO_PERMISOS.get(self.rol, []))
```

## 1.3. Subclases también delegan al catálogo

**Qué:** Actualizar `Admin.permisos()` e `Invitado.permisos()` para leer del catálogo.
**Por qué:** Misma razón; cero duplicidades.

```diff
 class Admin(Usuario):
@@
-    def permisos(self) -> list[str]:
-        return ["ver", "crear", "editar", "borrar"]
+    def permisos(self) -> list[str]:
+        return list(CATALOGO_PERMISOS["admin"])
 
 class Invitado(Usuario):
@@
-    def permisos(self) -> list[str]:
-        return ["ver"]
+    def permisos(self) -> list[str]:
+        return list(CATALOGO_PERMISOS["invitado"])
```

## 1.4. Igualdad y hash por email normalizado

**Qué:** Implementar `__eq__` y `__hash__` basados en el email (en minúsculas y sin espacios), más helper `_email_norm()`.
**Por qué:** Poder usar instancias en `set`/`dict` y considerar iguales dos usuarios con el mismo email (aunque cambie el nombre/rol).

> ⚠️ Nota: si cambias el `.email` *después* de meter la instancia en un `set`/como clave en un `dict`, el hash cambia y puedes “perder” la referencia. Evita mutar el email en esos casos.

```diff
 class Usuario(BaseUsuario):
@@
+    # ---------- Igualdad y hash por email normalizado ----------
+    def _email_norm(self) -> str:
+        return (self._email or "").strip().lower()
+
+    def __eq__(self, other: object) -> bool:
+        if not isinstance(other, Usuario):
+            return NotImplemented
+        return self._email_norm() == other._email_norm()
+
+    def __hash__(self) -> int:
+        return hash(self._email_norm())
```

## 1.5. Factory por rol en `desde_dict`

**Qué:** Hacer que `Usuario.desde_dict()` **devuelva subclases** (`Admin`, `Invitado`) según `rol`.
**Por qué:** Facilita crear instancias desde datos (por ejemplo, al importar JSON) sin `ifs` dispersos.

```diff
 class Usuario(BaseUsuario):
@@
-    @classmethod
-    def desde_dict(cls, datos: dict) -> "Usuario":
-        return cls(
-            nombre=datos.get("nombre", ""),
-            email=datos.get("email", ""),
-            rol=datos.get("rol", "usuario"),
-            activo=bool(datos.get("activo", True)),
-        )
+    @classmethod
+    def desde_dict(cls, datos: dict) -> "Usuario":
+        """Factory: devuelve Admin/Invitado/Usuario según 'rol'."""
+        rol = (datos.get("rol") or "usuario").strip().lower()
+        nombre = datos.get("nombre", "")
+        email = datos.get("email", "")
+        activo = bool(datos.get("activo", True))
+        if rol == "admin":
+            return Admin(nombre, email, activo=activo)
+        if rol == "invitado":
+            return Invitado(nombre, email, activo=activo)
+        return cls(nombre=nombre, email=email, rol="usuario", activo=activo)
```

*(El resto de tu scaffold —validaciones de email/rol, `presentarse`, `check_password`, etc.— se mantiene igual.)*

---

# 2) `app/repositorio.py` — Cambios paso a paso

Partimos del repositorio “en memoria” (agregar/obtener/eliminar/listar/buscar) y añadimos **persistencia JSON**.

## 2.1. Exportar a JSON (sin contraseñas)

**Qué:** Añadir `_to_dict()` y `exportar_json(ruta)`.
**Por qué:** Persistir usuarios **sin** exponer `__password_hash`.

```diff
-from typing import Callable, Optional
+from typing import Callable, Optional, Iterable
+import json
 from .modelos import Usuario
@@
 class RepositorioUsuarios:
@@
+    # ---------- Persistencia JSON (sin contraseñas) ----------
+    def _to_dict(self, u: Usuario) -> dict:
+        return {"nombre": u.nombre, "email": u.email, "rol": u.rol, "activo": u.activo}
+
+    def exportar_json(self, ruta: str) -> None:
+        data = [self._to_dict(u) for u in self._por_email.values()]
+        with open(ruta, "w", encoding="utf-8") as f:
+            json.dump(data, f, ensure_ascii=False, indent=2)
```

## 2.2. Importar desde JSON con política de conflicto

**Qué:** Añadir `importar_json(ruta, on_conflicto="error")` con políticas:

* `"error"`: lanza si existe el email
* `"omitir"`: no sobrescribe
* `"reemplazar"`: pisa el existente
  **Por qué:** Control fino de merges/cargas. Reutilizamos `Usuario.desde_dict()` (factory) para instanciar la subclase correcta.

```diff
+    def importar_json(self, ruta: str, on_conflicto: str = "error") -> None:
+        with open(ruta, "r", encoding="utf-8") as f:
+            datos = json.load(f)
+        if not isinstance(datos, list):
+            raise ValueError("Formato JSON inválido: se esperaba una lista de usuarios")
+        for item in datos:
+            u = Usuario.desde_dict(item)
+            k = u.email
+            if k in self._por_email:
+                if on_conflicto == "error":
+                    raise ValueError(f"Conflicto al importar: ya existe {k}")
+                if on_conflicto == "omitir":
+                    continue
+                if on_conflicto == "reemplazar":
+                    self._por_email[k] = u
+                    continue
+                raise ValueError(f"on_conflicto inválido: {on_conflicto}")
+            self._por_email[k] = u
```

## 2.3. Helper opcional `cargar(iterable)`

**Qué:** Atajo útil para tests (carga desde una lista de dicts).
**Por qué:** Facilita poblar el repositorio en pruebas/unit tests sin archivos.

```diff
+    def cargar(self, items: Iterable[dict], on_conflicto: str = "error") -> None:
+        for item in items:
+            u = Usuario.desde_dict(item)
+            k = u.email
+            if k in self._por_email and on_conflicto == "error":
+                raise ValueError(f"Conflicto al cargar: ya existe {k}")
+            self._por_email[k] = u
```

*(El resto del CRUD de memoria se mantiene tal cual.)*

---

# 3) `main.py` — Cambios paso a paso

Añadimos una **demo** que valida:

* ABC no instanciable
* Factory por rol
* Igualdad/hash por email
* Repositorio con duplicados y persistencia JSON
* Criterios de aceptación con asserts

```diff
-from app.modelos import Usuario, Admin, Invitado, BaseUsuario
+from app.modelos import Usuario, Admin, Invitado, BaseUsuario
+from app.repositorio import RepositorioUsuarios
@@
 if __name__ == "__main__":
@@
     try:
         BaseUsuario()  # ❌ debe fallar: clase abstracta
     except TypeError as e:
         print("Abstracta OK:", e)
 
+    # --- Factory por rol desde dict
+    datos = [
+        {"nombre": "Juan", "email": "juan@site.com", "rol": "admin", "activo": True},
+        {"nombre": "Eva", "email": "eva@site.com", "rol": "usuario", "activo": True},
+        {"nombre": "Inv", "email": "inv@site.com", "rol": "invitado", "activo": False},
+    ]
+    objs = [Usuario.desde_dict(d) for d in datos]
+    print([type(o).__name__ for o in objs])  # ['Admin', 'Usuario', 'Invitado']
+
+    # --- Igualdad/Hash por email
+    u1 = Usuario("Ana Clone", "ANA@test.com")
+    print("u == u1?", u == u1)           # True (email normalizado)
+    print({u, u1})                        # set con un único elemento
+
+    # --- Repositorio: CRUD + validaciones
+    repo = RepositorioUsuarios()
+    repo.agregar(a)
+    repo.agregar(g)
+    repo.agregar(u)
+    print("Activos:", [x.email for x in repo.listar_activos()])
+
+    g.desactivar()
+    print("Activos tras desactivar invitado:", [x.email for x in repo.listar_activos()])
+
+    try:
+        repo.agregar(Usuario("Ana 2", "ana@test.com"))
+    except ValueError as e:
+        print("Duplicado OK:", e)
+
+    # --- Persistencia JSON
+    ruta = "usuarios.json"
+    repo.exportar_json(ruta)
+    print("Exportado a", ruta)
+
+    repo2 = RepositorioUsuarios()
+    repo2.importar_json(ruta, on_conflicto="error")
+    print("Importados:", [x.email for x in repo2.listar_activos()])
+
+    # --- Criterios de aceptación (asserts rápidos)
+    assert Admin("X", "x@x").tiene_permiso("borrar") is True
+    assert Invitado("Y", "y@y").tiene_permiso("borrar") is False
+    assert Usuario("Z", "z@z").permisos() == ["ver"]
+    print("✅ Criterios de aceptación OK")
```

---

## ✅ Checklist de aceptación (todos cubiertos)

* `Admin(...).tiene_permiso("borrar")` → **True**
* `Invitado(...).tiene_permiso("borrar")` → **False**
* `Usuario(...).permisos()` → **\["ver"]**
* Instanciar `BaseUsuario()` → **TypeError**
* Repositorio: añadir dos usuarios con el mismo email → **ValueError**
* `listar_activos()` excluye desactivados → **OK**
* **Retos extra**:

  * Factory en `desde_dict` → **OK**
  * `__eq__/__hash__` por email → **OK**
  * Catálogo central de permisos → **OK**
  * Exportar/Importar JSON sin contraseñas → **OK**

---

## ℹ️ Consejos rápidos

* Si vas a usar `Usuario` en `set`/`dict`, **evita cambiar `email`** después de insertarlo (hash cambiante).
* Si en el futuro añades más roles, **solo** toca `CATALOGO_PERMISOS` y, si quieres una subclase propia, crea `class Editor(Usuario)` y añade su entrada en el catálogo.
