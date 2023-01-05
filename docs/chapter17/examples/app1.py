import uvicorn
from fastapi import FastAPI,Request




app = FastAPI()


@app.get('/test')
async def test1():
    return {'result': '这是一个GET'}




@app.get('/test/{apiname}')
async def test2(apiname):
    """
    /test/<apiname>：后面的apiname表示任意名字
    """
    return {'result': f'这是一个GET，您请求的是：{apiname}'}



if __name__ == '__main__':
    uvicorn.run(
        app = app,
        host = "0.0.0.0",
        port = 5678
    )