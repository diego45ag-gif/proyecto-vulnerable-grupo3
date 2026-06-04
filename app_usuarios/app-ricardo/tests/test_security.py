import unittest
from app.main import app, users_db

class TestSecurityControls(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Limpiar la base de datos simulada antes de cada prueba
        users_db.clear()

    def test_register_empty_fields_should_fail(self):
        """Verifica el requisito S-SDLC: No permitir registros con campos vacíos"""
        response = self.app.post('/register', data={
            'nombre': '',
            'email': 'test@vulnerable.com',
            'password': ''
        }, follow_redirects=True)
        self.assertIn(b'Todos los campos son estrictamente obligatorios.', response.data)

    def test_register_short_name_should_fail(self):
        """Verifica el requisito S-SDLC: Control de longitud del nombre (mínimo 3 caracteres)"""
        response = self.app.post('/register', data={
            'nombre': 'Al',
            'email': 'test@vulnerable.com',
            'password': 'PasswordSecure123!'
        }, follow_redirects=True)
        self.assertIn(b'El nombre debe tener entre 3 y 50 caracteres.', response.data)

if __name__ == '__main__':
    unittest.main()