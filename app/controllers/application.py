from bottle import template, request, redirect, response, static_file
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
            message = user_register.run()
            if message:
                response.set_cookie("user", username)
                redirect('/auction_display')

        except ValueError as e:
            redirect(f'/signup?error={e}')

    
    def signin(self, error=None):
        if error:
            return template('signin', error=error)
        else:
            return template('signin', error=None)
    
    def signin_post(self, username, password):
        try:
            user_signin = SignIn(username=username, password=password)
            message = user_signin.run()
            if message:
                response.set_cookie("user", username)
                redirect('/auction_display')

        except ValueError as e:
            redirect(f'/signin?error={e}')

    def auction_display(self):
        return template('auctions')
    
    def get_auctions(self):
        ...

    def lot(self):
        return template()
    
    def bid(self):
        return template()
    
