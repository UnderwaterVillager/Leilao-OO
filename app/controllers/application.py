from bottle import template

class Application:
    def __init__(self):
        self.pages ={
            '/': self.home
        }

    def home(self):
        return template()
    
    def login(self):
        return template()
    
    def signuṕ(self):
        return template()
    
    def auction(self):
        return template()
    
    def lot(self):
        return template()
    
    def bid(self):
        return template()
    
