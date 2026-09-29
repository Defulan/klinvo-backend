from pydantic import BaseModel

class UserCreateSchema(BaseModel):
    name: str
    password: str

class UserLoginSchema(BaseModel):
    id: int
    password: str

class UserOut(BaseModel):
    id: int
    name: str
