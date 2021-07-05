from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

#from pydantic import BaseModel                  # class 처리
#from .db.schemas import Item

from fastapi.responses import HTMLResponse      # html code return

from .view_config import template
from fastapi import Request

from .db import crud, models, schemas
from .db.database import SessionLocal, engine

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
            <a href="http://192.182.8.125:8000/home_file">test page</a><br/>
            <a href="http://192.182.8.125:8000/license">test license</a>
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
async def read_item_post(item: schemas.Item, item_id: int, q: Optional[str] = None):
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
async def read_db_test2(item_name: str, db: Session = Depends(get_db)):
    item = crud.get_items_by_name(db, item_name)
    if item is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return item

@app.put("/dbtest/insert")
async def insert_db_test(item: schemas.Item, db: Session = Depends(get_db)):
    return insert_item(db, item)



# license page
# @app.get("/license")
# async def get_license_page(request: Request):
#     return template.TemplateResponse("license.html", {"request":request, "ab":{"ab_name":"name", "ab_tel","tel", "ab_birth":"brith", "ab_comdept":"comdept", "ab_memo":"memo"}})

@app.get("/license/get")
async def get_license(db: Session = Depends(get_db)):
    license = crud.get_license(db)
    if license is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return license