from bottle import template, request, redirect, Response, static_file
from .interfaces import SignUp, SignIn

class Application:
    def __init__(self):
        ...

    def serve_static(self, filename):
        return static_file(filename, root='./static')

    def home(self):
        return template()
    
    def signup(self, error=None):
        if error:
            return template('signup', error=error)
        else:
            return template('signup', error=None)

    def signup_post(self, username, email, password):
        try:
            user_register = SignUp(username=username, password=password, email=email)
            user_register.run()
            return {"message": "Usuário registrado com sucesso!"}

        except ValueError as e:
            redirect(f'/signup?error={e}')

    
    def login(self):
        return template()
    
    def auction(self):
        return template()
    
    def lot(self):
        return template()
    
    def bid(self):
        return template()
    
