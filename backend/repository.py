from sqlalchemy import DateTime, or_
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import models, schemas

############################################ PUBLICATION ###############################################################
def create_publication(db: Session,user_name:str, publi: schemas.PublicationCreate):
    db_publi = models.Account(name =publi.name, data = publi.data, account = user_name)
    db.add(db_publi)
    db.commit()
    db.refresh(db_publi)
    return db_publi
def get_publications_by_username(db: Session,user_name:str,skip: int = 0, limit: int = 100):
    db_publi = db.query(models.Publication).filter(models.Publication.username == user_name).offset(skip).limit(limit).all()
    return db_publi
def get_publications_by_name(db: Session,name:str,skip: int = 0, limit: int = 100):
    db_publi = db.query(models.Publication).filter(models.Publication.name== name).offset(skip).limit(limit).all()
    return db_publi
def delete_publication(db: Session, id: int ):
    db_acc = db.query(models.Publication).filter(models.Publication.id== id).first()
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
    publications = get_publications_by_username(db,username)
    db_acc = db.query(models.Account).filter(models.Account.username == username).first()
    if not db_acc:
        return None
    for image in publications:
        db.delete(image)
    db.delete(db_acc)
    db.commit()
    return db_acc