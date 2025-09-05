# 🔹 Fase 2: `main.py` como entrada controlada (`if __name__ == "__main__":`)

### 🎯 Objetivo

Crear un **punto de entrada** para ejecutar una demo rápida del proyecto **sin** que se ejecute cuando se importe como módulo. Practicar el patrón:

```python
if __name__ == "__main__":
    main()
```

---

## 🧱 Scaffold

A la estructura de la Fase 1, añade/edita `main.py` en la raíz:

```
lab5_modular_cli/
├─ app/
│  ├─ __init__.py
│  ├─ modelos.py
│  ├─ repositorio.py
│  └─ utils.py
└─ main.py   ← aquí
```

---

## 🧭 Implementación (main.py)

```python
# main.py
from app import Admin, Moderador, RepositorioUsuarios

def main():
    # 1) Crear repositorio en memoria
    repo = RepositorioUsuarios()

    # 2) Crear instancias de ejemplo
    a = Admin("Root", "root@corp.com")
    m = Moderador("Lucía", "lucia@test.com", nivel=2, activo=False)

    # 3) Guardarlas en repositorio
    repo.agregar(a)
    repo.agregar(m)

    # 4) Mostrar estado inicial
    print("Activos:", [str(u) for u in repo.listar_activos()])

    # 5) Activar moderador y volver a listar
    m.activar()
    print("Ahora activos:", [str(u) for u in repo.listar_activos()])

    # 6) Borrado de un usuario y listado final
    repo.eliminar("root@corp.com")
    print("Tras eliminar admin:", [str(u) for u in repo.listar_activos()])

if __name__ == "__main__":
    main()
```

> Nota: Importamos desde el **paquete** `app` para demostrar la paquetización de la Fase 1.

---

## ▶️ Ejecución

```bash
# Ejecuta la demo:
python main.py

# Importa sin ejecutar la demo (debe NO imprimir nada automáticamente):
python -c "import main"
```

---

## ✅ Criterios de aceptación

* Ejecutar `python main.py` imprime:

  * Lista de activos inicial (solo `Admin`, porque el `Moderador` empieza inactivo).
  * Lista de activos tras activar al moderador (ambos).
  * Lista final tras eliminar al admin (solo el moderador).
* Importar `main` **no** ejecuta la demo (no hay prints), confirmando que el bloque protegido por `__main__` funciona.

---

## 🔥 Reto (opcional)

1. **Parámetros de demo**
   Acepta un flag `--crear-n` para crear N moderadores de prueba (usa `argparse`) y listarlos.
2. **Inyección de repositorio**
   Cambia `main(repo=None)` para permitir pasar un repositorio externo (facilita tests).
3. **Errores controlados**
   Envuelve `repo.agregar` con `try/except ValueError` y muestra un mensaje si hay duplicados.