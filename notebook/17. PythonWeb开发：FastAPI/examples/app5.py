
import uvicorn
from fastapi import FastAPI


# 导入Request上下文对象，用来在前后台之间传递参数
from starlette.requests import Request

from starlette.staticfiles import StaticFiles
# 导入jinja2模板引擎对象，用于后续使用
from starlette.templating import Jinja2Templates


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
# 实例化一个模板引擎对象，指定模板所在路径
templates=Jinja2Templates(directory='templates')

@app.get("/sign")
async def read_items(request: Request):
    # 返回一个模板对象，同时使用上下文中的数据对模板进行渲染
    return templates.TemplateResponse(name='sign.html',context = {'request':request})



@app.post("/sign")
async def read_sign(request: Request):
    args = await request.form()
    username = args['username']
    passwd = args['password']
    print(username,passwd)
    # 返回一个模板对象，同时使用上下文中的数据对模板进行渲染

    if username == 'test' and passwd == '123456':
        return templates.TemplateResponse(name='success.html',context = {'request':request,'username':username})
    return templates.TemplateResponse(name='bad.html',context = {'request':request})


if __name__ == '__main__':
    uvicorn.run(
        app = app,
        host = "0.0.0.0",
        port = 5678
    )