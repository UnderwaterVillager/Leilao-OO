from bottle import template

class Application:
    def __init__(self):
        self.pages ={
            '/': self.home
        }

    def home(self):
        return template()
    
