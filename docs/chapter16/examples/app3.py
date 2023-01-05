from flask import Flask, render_template,url_for
from flask import request


app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test1():
    return {'result': '这是一个GET'}




@app.route('/test/<apiname>', methods=['GET'])
def test2(apiname):
    """
    /test/<apiname>：后面的apiname表示任意名字
    """
    return {'result': f'这是一个GET，您请求的是：{apiname}'}



if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 5678)