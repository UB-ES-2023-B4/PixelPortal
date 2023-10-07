from sqlalchemy import DateTime, or_
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import models, schemas

############################################ IMAGE ###############################################################
def create_image(db: Session,user_name:str, image: schemas.ImageCreate):
    db_account = models.Account(name =image.name, data = image.data, account = user_name)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
def get_images_by_username(db: Session,user_name:str,skip: int = 0, limit: int = 100):
    db_images = db.query(models.Image).filter(models.Image.username == user_name).offset(skip).limit(limit).all()
    return db_images
def get_images_by_name(db: Session,name:str,skip: int = 0, limit: int = 100):
    db_images = db.query(models.Image).filter(models.Image.name== name).offset(skip).limit(limit).all()
    return db_images
def delete_image(db: Session, name: str ):
    db_acc = db.query(models.Image).filter(models.Image.name == name).first()
    if not db_acc:
        return None
    db.delete(db_acc)
    db.commit()
    return db_acc
############################################ ACCOUNT ###############################################################
def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(username=account.username, password=account.password, is_admin=account.is_admin)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account
def get_account_by_name(db: Session, name: str):
    user = db.query(models.Account).filter(models.Account.username == name).first()
    return user

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def update_account(db: Session, username: str, account: schemas.Account):
    db_acc = db.query(models.Account).filter(models.Account.username == username).first()
    if not db_acc:
        return None
    for var, value in vars(account).items():
        if value is not None:
            setattr(db_acc, var, value)
    db.add(db_acc)
    db.commit()
    db.refresh(db_acc)
    return db_acc

def delete_account(db: Session, username: str):
    images = get_images_by_username(db,username)
    db_acc = db.query(models.Account).filter(models.Account.username == username).first()
    if not db_acc:
        return None
    for order in images:
        db.delete(order)
    db.delete(db_acc)
    db.commit()
    return db_acc