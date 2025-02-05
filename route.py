from bottle import Bottle, request

from app.controllers.application import Application

app = Bottle()
ctl = Application()


@app.route('/')
def home():
    return ctl.home()

@app.route('/signup')
@app.route('/signup/<error_message:re:Erro.*!>')
def signup(error_message=None):
    return ctl.signup(error_message)

@app.route('/signup', method='POST')
def signup_post():
    username = request.forms.username
    email = request.forms.email
    password = request.forms.password
    return ctl.signup_post(username, email, password)

if __name__ == "__main__":
    app.run(debug=True)