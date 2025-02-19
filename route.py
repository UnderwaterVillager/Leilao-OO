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

if __name__ == "__main__":
    app.run(debug=True)