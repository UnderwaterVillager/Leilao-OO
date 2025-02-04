from bottle import Bottle

from app.controllers.application import Application

app = Bottle()
ctl = Application()


@app.route('/')
def home():
    return ctl.home()

@app.route('/signup', method='POST')
def signup():
    return ctl.signup()

if __name__ == "__main__":
    app.run(debug=True)