from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'There is no ignorance, there is knowledge.'

if '__main__' == __name__:
    app.run(port=5000)