from pydantic import BaseModel

class UserSchema(BaseModel):
    email: str

    class Config:
        orm_mode = True