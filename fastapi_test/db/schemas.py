from typing import List, Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    id: int
    name: Optional[str] = None
    def printObject():
        print(str(id) + " " + name)

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    class Config:
        orm_mode = True
    
    def idName():
        super().printObject()


class License(BaseModel):
    id : int
    companyname : str
    hostname :str

# class ItemBase(BaseModel):
#     title: str
#     description: Optional[str] = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []

#     class Config:
#         orm_mode = True