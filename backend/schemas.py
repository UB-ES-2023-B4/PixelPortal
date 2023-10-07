from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


############################################ Publication ###############################################################

class PublicationBase(BaseModel):
    name: str
    data: bytes
    account_id: int
class PublicationCreate(PublicationBase):
    pass

class Publication(PublicationBase):
    id: int
    class Config:
        orm_mode = True


############################################ ACCOUNT ###############################################################
class AccountBase(BaseModel):
    username: Optional[str]
    is_admin: int = 0
class AccountCreate(AccountBase):
    username: str = Field(..., description="username")
    password: str = Field(..., min_length=8, max_length=24 ,description="user password")
class Account(AccountBase):
    publications : list[Publication] = []
    class Config:
        orm_mode = True
class SystemAccount(Account):
    password: str

############################################ TOKEN ###############################################################
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None