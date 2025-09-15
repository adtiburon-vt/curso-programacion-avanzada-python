# ✅ Resolución paso a paso — CLI con `argparse`

---

## 🔹 Reto 1 — Activar y desactivar usuarios

---

### 1. Añade las funciones `cmd_activar` y `cmd_desactivar`:

```python
def cmd_activar(args):
    u = repo.obtener_por_email(args.email)
    if u:
        u.activar()
        print(f"{args.email} ha sido activado.")
    else:
        print(f"Usuario no encontrado: {args.email}")

def cmd_desactivar(args):
    u = repo.obtener_por_email(args.email)
    if u:
        u.desactivar()
        print(f"{args.email} ha sido desactivado.")
    else:
        print(f"Usuario no encontrado: {args.email}")
```

---

### 2. Añade los subcomandos al parser en `build_parser()`:

```python
    # activar
    p_act = sub.add_parser("activar", help="Activar usuario por email")
    p_act.add_argument("email")
    p_act.set_defaults(func=cmd_activar)

    # desactivar
    p_des = sub.add_parser("desactivar", help="Desactivar usuario por email")
    p_des.add_argument("email")
    p_des.set_defaults(func=cmd_desactivar)
```

---

### ✅ Prueba:

```bash
python cli.py activar lucia@test.com
python cli.py desactivar lucia@test.com
```

---

## 🔹 Reto 2 — Buscar usuarios por texto

---

### 1. Añade la función `cmd_buscar`:

```python
def cmd_buscar(args):
    texto = (args.texto or "").lower()
    resultados = repo.buscar(lambda u: texto in u.nombre.lower() or texto in u.email.lower())
    if not resultados:
        print("(sin coincidencias)")
    else:
        for u in resultados:
            print(u)
```

---

### 2. Añade el subcomando en `build_parser()`:

```python
    # buscar
    p_buscar = sub.add_parser("buscar", help="Buscar usuarios por nombre o email")
    p_buscar.add_argument("--texto", required=True)
    p_buscar.set_defaults(func=cmd_buscar)
```

---

### ✅ Prueba:

```bash
python cli.py buscar --texto luc
```

---

## 🔹 Reto 3 — Exportar usuarios como JSON

---

### 1. Modifica la función `cmd_listar` para soportar `--salida json`:

```python
import json

def cmd_listar(args):
    usuarios = repo.listar_activos() if args.solo_activos else repo.buscar(lambda _: True)
    if not usuarios:
        print("(sin usuarios)")
        return

    if args.salida == "json":
        # convertir objetos Usuario a dicts simples
        datos = [
            {
                "nombre": u.nombre,
                "email": u.email,
                "rol": u.rol,
                "activo": u.activo
            } for u in usuarios
        ]
        print(json.dumps(datos, indent=2))
    else:
        for u in usuarios:
            print(u)
```

---

### 2. Modifica el subcomando `listar` en `build_parser()`:

```python
    p_list.add_argument("--salida", choices=["texto", "json"], default="texto")
```

---

### ✅ Prueba:

```bash
python cli.py listar --salida json
```

---

# 🧹 Extras (opcional)

Si usas varias funciones `cmd_*`, puedes agruparlas al final para mantener el código limpio:

```python
# --- Registro de subcomandos ---
# En build_parser() defines todos los comandos
# Cada uno con su parser.add_argument() y .set_defaults(func=cmd_xxx)
```
