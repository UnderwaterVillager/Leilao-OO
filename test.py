import unittest
import requests

from app.models import create, destroy
from app.controllers.interfaces import SignUp, SignIn

class TestWriteUserData(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        destroy()
        create()

    def test_create_user(self):
        username = 'tester'
        email = 'tester@lala.com'
        password = '123456'
        signup = SignUp(username, password, email)
        result = signup.run()
        
        self.assertEqual(result, 'Dado registrado com sucesso')

    def test_duplicate_username(self):
        username = 'tester'
        email = 'tester1@lolo.com'
        password = '123456'
        
        with self.assertRaises(ValueError) as context:
            signup = SignUp(username, password, email)
            result = signup.run()
        
        self.assertEqual(str(context.exception), 'Nome de usuário já existe')

    def test_duplicate_email(self):
        username = 'tester1'
        email = 'tester@lala.com'
        password = '123456'

        with self.assertRaises(ValueError) as context:
            signup = SignUp(username, password, email)
            result = signup.run()
        
        self.assertEqual(str(context.exception), 'Email já cadastrado')

class TestLogIn(unittest.TestCase):
    def setUp(self):
        destroy()
        create()
        SignUp("Marco", "808", "marcola@gmail.com").run()
    
    def test_read_credentials_correct(self):
        login = SignIn('Marco', '808')
        result = login.run()
        self.assertEqual(result, "Usuário está autenticado!")

    def test_read_credentials_wrong_password(self):
        with self.assertRaises(ValueError) as context:
            login = SignIn('Marco', '101')
            result = login.run()

        self.assertEqual(str(context.exception), "Senha incorreta!")

    def test_read_credentials_user_not_found(self):
        with self.assertRaises(ValueError) as context:
            login = SignIn('Joe', '909')
            result = login.run()

        self.assertEqual(str(context.exception), "Usuário não encontrado!")


if __name__ == '__main__':
    unittest.main()

