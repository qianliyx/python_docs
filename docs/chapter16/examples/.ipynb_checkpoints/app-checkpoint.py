from flask import Flask


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return '<h1>这是一个主页</h1>'


if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 5678)