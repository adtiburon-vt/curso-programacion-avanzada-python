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