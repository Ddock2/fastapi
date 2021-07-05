from typing import Optional
from fastapi import FastAPI

import uvicorn

from pydantic import BaseModel                  # class 처리
from fastapi.responses import HTMLResponse      # html code return

from fastapi.templating import Jinja2Templates  # html file return
from fastapi import Request

class Item(BaseModel):
    id : int
    name: str

template = Jinja2Templates(directory="html_file")

app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/", response_class=HTMLResponse)
def read_root_html():
    html_content = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
            <a href="http://192.182.8.125:8000/home_file">test page</a>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/home_file", response_class=HTMLResponse)
def read_root_html_file(request: Request):
    return template.TemplateResponse("test_home.html", {"request":request})

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": "get " + str(item_id), "q": q}

@app.put("/items/{item_id}")
def read_item_put(item_id: int, q: Optional[str] = None):
    return {"item_id": "put " + str(item_id), "q": q}

@app.post("/items/{item_id}")
def read_item_post(item: Item, item_id: int, q: Optional[str] = None):
    return {"recv": item, "item_id": "put " + str(item_id), "q": q}

if __name__ == "__main__":
    uvicorn.run(app, host="192.182.8.125", port=8000)