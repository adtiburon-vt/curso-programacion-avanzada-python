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