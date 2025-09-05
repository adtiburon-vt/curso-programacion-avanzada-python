# 🧭 Laboratorio 5 — Dividir un proyecto en módulos + ejecución desde CLI

**Duración estimada:** 2 horas
**Sesión relacionada:** Sesión 5 (módulos y paquetes, estructura de proyecto, `if __name__ == "__main__":`)
**Modalidad:** presencial / remota

---

## 🎯 Objetivo general

Refactorizar el sistema de usuarios en un **paquete modular** (`app/`) y exponer una **CLI** (línea de comandos) con `argparse`, controlada mediante `if __name__ == "__main__":`.

---

## 📁 Estructura objetivo

```
lab5_modular_cli/
├─ app/                    # paquete de aplicación
│  ├─ __init__.py
│  ├─ modelos.py           # Usuario, Admin, Invitado, Moderador, mixins…
│  ├─ repositorio.py       # RepositorioUsuarios (en memoria)
│  └─ utils.py             # validaciones auxiliares (email, hashing simple…)
├─ cli.py                  # script CLI con argparse (punto de entrada)
├─ main.py                 # demo/entry manual con if __name__ == "__main__"
├─ tests/
│  ├─ __init__.py
│  └─ test_basico.py       # smoke tests
└─ README.md
```

> Puedes partir de tus archivos de Labs 3–4 y moverlos/ajustarlos.

---

## 🔬 Fases del laboratorio

### 🔹 Fase 1: Paquetización y separación por módulos

**Objetivo:** crear el paquete `app/` y repartir clases/funciones por responsabilidad.

**Scaffold mínimo**

**app/**init**.py**

```python
# Exponer lo esencial del paquete
from .modelos import Usuario, Admin, Invitado, Moderador
from .repositorio import RepositorioUsuarios
```

**app/utils.py**

```python
def validar_email(email: str) -> bool:
    email = (email or "").strip().lower()
    return "@" in email and "." in email and not (email.startswith("@") or email.endswith("@"))
```

**app/modelos.py** (importa utilidades y pega tus clases de Labs 3–4)

```python
from .utils import validar_email
# … Usuario, Admin, Invitado, Moderador, mixins …
# Asegúrate de que Usuario usa validar_email en el setter de email.
```

**app/repositorio.py**

```python
from typing import Callable, Optional
from .modelos import Usuario

class RepositorioUsuarios:
    def __init__(self):
        self._por_email: dict[str, Usuario] = {}

    def agregar(self, u: Usuario):
        k = u.email
        if k in self._por_email:
            raise ValueError(f"Ya existe usuario con email {k}")
        self._por_email[k] = u

    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        return self._por_email.get(email.strip().lower())

    def listar_activos(self):
        return [u for u in self._por_email.values() if u.activo]

    def eliminar(self, email: str):
        self._por_email.pop(email.strip().lower(), None)

    def buscar(self, pred: Callable[[Usuario], bool]):
        return [u for u in self._por_email.values() if pred(u)]
```

**Validación (rápida)**

```python
from app.modelos import Usuario
u = Usuario("Ana", "ana@test.com")
print(u)
```

---

### 🔹 Fase 2: `main.py` como entrada controlada (`__main__`)

**Objetivo:** lanzar una demo manual sin interferir cuando el módulo se importe.

**main.py**

```python
from app.modelos import Admin, Moderador
from app.repositorio import RepositorioUsuarios

def main():
    repo = RepositorioUsuarios()
    a = Admin("Root", "root@corp.com")
    m = Moderador("Lucía", "lucia@test.com", nivel=2, activo=False)

    repo.agregar(a)
    repo.agregar(m)
    print("Activos:", [str(u) for u in repo.listar_activos()])

    m.activar()
    print("Ahora activos:", [str(u) for u in repo.listar_activos()])

if __name__ == "__main__":
    main()
```

**Comprobación**

```bash
python main.py       # ejecuta demo
python -c "import main"   # no debe ejecutar la demo (no print)
```

---

### 🔹 Fase 3: CLI con `argparse` (crear/listar/eliminar usuarios)

**Objetivo:** exponer comandos desde terminal.

**cli.py**

```python
import argparse
from app.modelos import Usuario, Admin, Invitado, Moderador
from app.repositorio import RepositorioUsuarios

repo = RepositorioUsuarios()  # en memoria (ciclo de proceso)

def cmd_crear(args):
    rol = args.rol.lower()
    if rol == "admin":
        u = Admin(args.nombre, args.email)
    elif rol == "invitado":
        u = Invitado(args.nombre, args.email)
    elif rol == "moderador":
        u = Moderador(args.nombre, args.email, nivel=args.nivel)
    else:
        u = Usuario(args.nombre, args.email, rol="usuario")
    repo.agregar(u)
    print(f"Creado: {u}")

def cmd_listar(args):
    activos = repo.listar_activos() if args.solo_activos else list(repo.buscar(lambda u: True))
    for u in activos:
        print(u)

def cmd_eliminar(args):
    repo.eliminar(args.email)
    print(f"Eliminado (si existía): {args.email}")

def build_parser():
    p = argparse.ArgumentParser(prog="usuarios")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_crear = sub.add_parser("crear", help="Crear usuario")
    p_crear.add_argument("nombre")
    p_crear.add_argument("email")
    p_crear.add_argument("--rol", choices=["usuario","admin","invitado","moderador"], default="usuario")
    p_crear.add_argument("--nivel", type=int, default=1, help="Nivel para moderador")
    p_crear.set_defaults(func=cmd_crear)

    p_list = sub.add_parser("listar", help="Listar usuarios")
    p_list.add_argument("--solo-activos", action="store_true")
    p_list.set_defaults(func=cmd_listar)

    p_del = sub.add_parser("eliminar", help="Eliminar usuario por email")
    p_del.add_argument("email")
    p_del.set_defaults(func=cmd_eliminar)

    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
```

**Pruebas CLI**

```bash
python cli.py crear "Ana" ana@test.com --rol admin
python cli.py crear "Lucía" lucia@test.com --rol moderador --nivel 2
python cli.py listar
python cli.py eliminar ana@test.com
python cli.py listar --solo-activos
```

> Nota: el repositorio es **en memoria**; cada ejecución comienza “limpia”. Si quieres persistencia, guarda/carga JSON en `repo`.

---

## 🧠 Reflexión final

* ¿Qué mejoras de mantenibilidad aporta separar `modelos`, `repositorio` y `utils`?
* ¿Cuándo usarías **importaciones absolutas** vs **relativas**?
* ¿Qué ventajas tiene proteger el punto de entrada con `__main__` y ofrecer una **CLI**?

---

## ✅ Comprobación de conocimientos

1. ¿Qué sucede si importas `main` desde otro módulo? ¿Se ejecuta la demo?
2. ¿Cómo añadirías un subcomando `activar EMAIL` a la CLI que active un usuario?
3. ¿Cómo reorganizarías el código para que el repositorio sea inyectable (pasado como dependencia) en lugar de global?

---

## 🔥 Retos (opcionales)

* **Persistencia JSON**: añade `guardar(path)` / `cargar(path)` en `RepositorioUsuarios`.
* **Subcomando `buscar`**: por rol o texto en nombre/email.
* **Paquete instalable**: estructura `src/`, `pyproject.toml` y entrada de consola (`entry_points`) para ejecutar `usuarios` como comando del sistema.