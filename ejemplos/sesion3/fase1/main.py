from app.modelos import Usuario, Admin, Invitado, tiene_permiso
# from app.repositorio import RepositorioUsuarios

if __name__ == "__main__":
    u = Usuario("Ana", "ana@test.com")
    a = Admin("Root", "root@corp.com")
    g = Invitado("Visitante", "guest@example.org")

    print(u.presentarse(), u.permisos())
    print(a.presentarse(), a.permisos(), tiene_permiso(a, "borrar"))
    print(g)

    # u.email = "mal_email"  # descomenta para ver ValueError