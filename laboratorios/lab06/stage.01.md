# 🔹 Fase 1 — Tests manuales (punto de partida rápido)

### 🎯 Objetivo

Crear **pruebas manuales** mínimas (con `print`) para verificar el comportamiento esperado del sistema de usuarios y del repositorio. Estas comprobaciones servirán de **guía** para convertirlas en tests automatizados en la Fase 2.

---

## 🧱 Scaffold

En la raíz del proyecto (donde está tu paquete `app/`), crea un archivo temporal:

```
lab6_testing/
├─ app/
│  ├─ __init__.py
│  ├─ modelos.py
│  ├─ repositorio.py
│  └─ utils.py
└─ scratch.py   ← pruebas manuales
```

---

## 🧭 Implementación (`scratch.py`)

```python
# scratch.py
from app.modelos import Usuario, Admin, Moderador, Invitado
from app.repositorio import RepositorioUsuarios

print("=== PRUEBAS MANUALES: MODELOS ===")
u = Usuario("Ana", "ana@test.com")
print("presentarse():", u.presentarse())  # Esperado: "Soy Ana (ana@test.com)"

try:
    Usuario("Luis", "sin-arroba")
    print("[ERROR] Se aceptó un email inválido")
except ValueError:
    print("[OK] Email inválido lanza ValueError")

a = Admin("Root", "root@corp.com")
print("Admin tiene 'borrar'?:", "borrar" in a.permisos())  # Esperado: True

m1 = Moderador("Lucía", "lucia@test.com", nivel=1)
m2 = Moderador("Carlos", "carlos@test.com", nivel=2)
print("Moderador n1 'borrar'?:", "borrar" in m1.permisos())  # Esperado: False
print("Moderador n2 'borrar'?:", "borrar" in m2.permisos())  # Esperado: True

m1.set_password("secreta1")
print("check_password ok?:", m1.check_password("secreta1"))  # Esperado: True
print("check_password fallo?:", m1.check_password("otra"))   # Esperado: False

print("\n=== PRUEBAS MANUALES: REPOSITORIO ===")
repo = RepositorioUsuarios()
repo.agregar(u)
repo.agregar(a)
repo.agregar(m2)
print("Obtener por email 'ana@test.com':", repo.obtener_por_email("ana@test.com"))
print("Listar activos:", [x.email for x in repo.listar_activos()])

# Duplicados
try:
    repo.agregar(Usuario("Ana2", "ana@test.com"))
    print("[ERROR] Se permitió duplicado por email")
except ValueError:
    print("[OK] Duplicado bloqueado por email")

# Eliminar y revalidar
repo.eliminar("root@corp.com")
print("Tras eliminar admin, activos:", [x.email for x in repo.listar_activos()])

# Búsqueda libre
print("Buscar por rol moderador:", [x.email for x in repo.buscar(lambda u: u.rol == "moderador")])
```

---

## ▶️ Ejecución

```bash
python scratch.py
```

---

## ✅ Criterios de aceptación (lo que deberías ver)

* `presentarse()` imprime **“Soy Ana ([ana@test.com](mailto:ana@test.com))”**.
* Crear `Usuario("Luis","sin-arroba")` **lanza `ValueError`**.
* `Admin` **sí** tiene permiso `"borrar"`.
* `Moderador` **nivel 1** **no** tiene `"borrar"`, **nivel 2** **sí**.
* `set_password/check_password` funciona (True/False).
* El repositorio:

  * Permite **agregar** y **obtener** por email.
  * **Bloquea duplicados** por email (`ValueError`).
  * **Eliminar** no rompe el flujo y actualiza el listado.
  * `buscar` retorna el moderador cuando filtras por rol.

> Si algo **no coincide**, anótalo: será un **caso de test** en la Fase 2 y/o un **bug** a corregir en la Fase 3.

---

## 🔥 Reto (opcional)

1. **Normalización de email**
   Prueba `repo.obtener_por_email("  ANA@TEST.COM  ")`.

   * Si **no** encuentra a `ana@test.com`, apunta este “bug” para Fase 3 (normalizar entrada en el repo).

2. **Validación de nivel**
   Intenta `Moderador("X","x@x.com", nivel=0)` o `nivel="2"`.

   * Si se acepta, es otro “bug”: valida tipo y rango.

3. **Emails borde**
   Prueba `Usuario("Z","@x")` y `Usuario("Z","x@")`.

   * Si pasan, refuerza `validar_email` (Fase 3) y anota el caso para tests.

---

## 🧹 Buenas prácticas

* Mantén `scratch.py` **temporal**: sirve para explorar rápido, pero todo lo importante pasará a **tests automatizados**.
* Anota cada comportamiento esperado/observado; eso se convierte en **aserciones** (`assert*`) en la Fase 2.
* Evita dependencias externas o E/S en estas pruebas manuales (foco en lógica de dominio).