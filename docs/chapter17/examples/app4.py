import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/index")
async def read_items():
    html_content = """
    <html>
        <head>
            <title>index</title>
        </head>
        <body>
            <h1>花卷老师真帅!</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)




if __name__ == '__main__':
    uvicorn.run(
        app = app,
        host = "0.0.0.0",
        port = 5678
    )