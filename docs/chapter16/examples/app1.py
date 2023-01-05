from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/sign', methods=['GET'])
def signin_form():
    return '''
            <h1>这是一个注册页面</h1>
            <form action="/sign" method="post">
                <p>用户名：<input name="username"></p>
                <p>密码：<input name="password"></p>
                <p><button type="submit">Sign In</button></p>
            </form>
        '''

@app.route('/sign', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    if request.form['username']=='test' and request.form['password']=='123456':
        return f"<h1>Hello, {request.form['username']}!,欢迎回来!</h1>"
    return '<h1>Bad username or password.</h1>'


if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 5678)