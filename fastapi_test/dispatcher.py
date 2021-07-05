from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

#from pydantic import BaseModel                  # class 처리
from .db.schemas import Item

from fastapi.responses import HTMLResponse      # html code return

from .view_config import template
from fastapi import Request

from .db import crud, models, schemas
from .db.database import SessionLocal, engine


# class Item(BaseModel):
#     id : int
#     name: str

app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/", response_class=HTMLResponse)
async def read_root_html():
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
async def read_root_html_file(request: Request):
    return template.TemplateResponse("test_home.html", {"request":request})


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": "get " + str(item_id), "q": q}

@app.put("/items/{item_id}")
async def read_item_put(item_id: int, q: Optional[str] = None):
    return {"item_id": "put " + str(item_id), "q": q}

@app.post("/items/{item_id}")
async def read_item_post(item: Item, item_id: int, q: Optional[str] = None):
    return {"recv": item, "item_id": "put " + str(item_id), "q": q}


##############################################################################
# db 연동

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/dbtest/id/{item_id}")
async def read_db_test(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_items_by_id(db, item_id)
    if item is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return item

@app.get("/dbtest/name/{item_name}")
async def read_db_test(item_name: str, db: Session = Depends(get_db)):
    item = crud.get_items_by_name(db, item_name)
    if item is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return item
    