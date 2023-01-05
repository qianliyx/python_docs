import uvicorn
from fastapi import FastAPI,Request




app = FastAPI()


@app.post('/test')
async def test1():
    return {'result': '这是一个POST'}




@app.post('/test/{apiname}')
async def test2(apiname, request: Request):
    """
    /test/<apiname>：后面的apiname表示任意名字
    """

    args = await request.json()

    return {'result': f'这是一个GET，您请求的是：{apiname}，您的参数是：{args}'}



if __name__ == '__main__':
    uvicorn.run(
        app = app,
        host = "0.0.0.0",
        port = 5678
    )