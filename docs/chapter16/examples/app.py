from flask import Flask


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return '<h1>花卷老师真帅!</h1>'


if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 5678)