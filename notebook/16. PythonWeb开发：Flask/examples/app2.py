from flask import Flask, render_template,url_for
from flask import request


app = Flask(__name__)


@app.route('/sign', methods=['GET'])
def signin_form():
    return render_template("sign.html")

@app.route('/sign', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    username = request.form['username']
    passwd = request.form['password']
    if username=='test' and passwd=='123456':
        return render_template("success.html", username = username)
    return render_template("bad.html")


if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 5678)