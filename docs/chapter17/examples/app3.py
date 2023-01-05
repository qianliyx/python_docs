import uvicorn
from fastapi import FastAPI,Request,APIRouter



router = APIRouter(prefix='/bp',tags = ['bp'])




# @router.get('/test')
# @router.post("/test")
@router.api_route("/test",methods=['GET','POST'])
async def test1():
    return {'result': '这是一个GET或者POST'}



@router.post('/test/{apiname}')
# @router.get('/test/{apiname}')
# @router.api_route('/test/{apiname}',methods=['POST'])
async def test2(apiname, request: Request):
    """
    /test/<apiname>：后面的apiname表示任意名字
    """

    args = await request.json()

    return {'result': f'这是一个GET，您请求的是：{apiname}，您的参数是：{args}'}


app = FastAPI()
app.include_router(router)



if __name__ == '__main__':
    uvicorn.run(
        app = app,
        host = "0.0.0.0",
        port = 5678
    )