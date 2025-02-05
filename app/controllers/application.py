from bottle import template, request, redirect
from .interfaces import SignUp, SignIn

class Application:
    def __init__(self):
        self.pages ={
            '/': self.home,
            'signup': self.signup
        }

    def home(self):
        return template()
    
    def signup(self, error_message=None):
        return template('signup', error_message=error_message)

    def signup_post(self, username, email, password):
        try:
            user_register = SignUp(username=username, password=password, email=email)
            user_register.run()
        except ValueError as e:
            return redirect(f'/signup')

    
    def login(self):
        return template()
    
    def auction(self):
        return template()
    
    def lot(self):
        return template()
    
    def bid(self):
        return template()
    
