import unittest
from app.modelos import Usuario
from app.repositorio import RepositorioUsuarios

class TestRepositorio(unittest.TestCase):
    def test_agregar_obtener(self):
        repo = RepositorioUsuarios()
        u = Usuario("Ana", "ana@test.com")
        repo.agregar(u)
        self.assertIs(repo.obtener_por_email("ana@test.com"), u)

    def test_duplicado_lanza(self):
        repo = RepositorioUsuarios()
        repo.agregar(Usuario("Ana", "ana@test.com"))
        with self.assertRaises(ValueError):
            repo.agregar(Usuario("Ana2", "ana@test.com"))

    def test_eliminar(self):
        repo = RepositorioUsuarios()
        repo.agregar(Usuario("Ana", "ana@test.com"))
        repo.eliminar("ana@test.com")
        self.assertIsNone(repo.obtener_por_email("ana@test.com"))

    def test_listar_activos(self):
        repo = RepositorioUsuarios()
        u1 = Usuario("A", "a@x.com", activo=True)
        u2 = Usuario("B", "b@x.com", activo=False)
        repo.agregar(u1); repo.agregar(u2)
        self.assertEqual([u.email for u in repo.listar_activos()], ["a@x.com"])

if __name__ == "__main__":
    unittest.main()