from bottle import Bottle, request

from app.controllers.application import Application

app = Bottle()
ctl = Application()

@app.route('/static/<filename:path>')
def serve_static(filename):
    return ctl.serve_static(filename)

@app.route('/')
def home():
    return ctl.home()

@app.route('/signup')
def signup():
    error = request.query.error
    return ctl.signup(error=error)

@app.route('/signup', method='POST')
def signup_post():
    username = request.forms.username
    email = request.forms.email
    password = request.forms.password
    return ctl.signup_post(username, email, password)

@app.route('/signin')
def signin():
    error = request.query.error
    return ctl.signin(error=error)

@app.route('/signin', method='POST')
def signin_post():
    username = request.forms.username
    password = request.forms.password
    return ctl.signin_post(username, password)

@app.route('/auction_display')
def auction_display():
    return ctl.auction_display()

if __name__ == "__main__":
    app.run(debug=True)