import unittest
from app.modelos import Usuario, Admin, Moderador

class TestUsuario(unittest.TestCase):
    def test_presentarse(self):
        u = Usuario("Ana", "ana@test.com")
        self.assertEqual(u.presentarse(), "Soy Ana (ana@test.com)")

    def test_email_invalido(self):
        with self.assertRaises(ValueError):
            Usuario("Luis", "sin-arroba")

    def test_password(self):
        u = Usuario("Ana", "ana@test.com")
        u.set_password("secreta1")
        self.assertTrue(u.check_password("secreta1"))
        self.assertFalse(u.check_password("otra"))

class TestRoles(unittest.TestCase):
    def test_admin_tiene_borrar(self):
        a = Admin("Root", "root@corp.com")
        self.assertIn("borrar", a.permisos())

    def test_moderador_nivel1_no_borrar(self):
        m = Moderador("Lucía", "lucia@test.com", nivel=1)
        self.assertNotIn("borrar", m.permisos())

    def test_moderador_nivel2_si_borrar(self):
        m = Moderador("Carlos", "carlos@test.com", nivel=2)
        self.assertIn("borrar", m.permisos())

if __name__ == "__main__":
    unittest.main()