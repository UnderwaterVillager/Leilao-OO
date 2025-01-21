from bottle import Bottle, run

app = Bottle()

@app.route('/')
def home():
    return 

if __name__ == "__main__":
    app.run(debug=True)