import DB.Models as models
from sqlalchemy.orm import Session

def check_pwd(db :Session,uname:str,pwd:str):
    whoami = db.query(models.User).filter(models.User.uname == uname).first()
    if whoami is not None \
        and whoami.pwd == pwd:
        return whoami.id
    return None

def update_pwd(db :Session,uname:str,pwd:str):
    whoami = db.query(models.User).filter(models.User.uname == uname).first()
    whoami.pwd = pwd
    db.commit()
    
    return True

def check_user_exists(db :Session,uname:str):
    q = db.query(models.User).filter(models.User.uname == uname)
    return db.query(q.exists()).scalar()


def create_user(db :Session,uname:str,pwd:str):
    user = models.User(uname=uname,pwd=pwd)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def check_asset_exists(db :Session,assetname:str):
    q = db.query(models.DevelopAsset).filter(models.DevelopAsset.assetname == assetname)
    return  db.query(q.exists()).scalar()

def create_asset(db :Session,
                 uid :str
                 ,assetname:str
                
                 ,assetpath:str
                 ,assetprice_fen:int):
    # asset_obj = models.DevelopAsset(user_id = uid 
    #     ,asset_img_url = asset_img_url
    #     ,asset_before_img_url = asset_before_img_url
    #     ,asset_after_img_url = asset_after_img_url
    #     ,assetname = assetname
    #     ,assetpath = assetpath
    #     ,assetinfo  = assetinfo
    #     ,assetprice_fen = assetprice_fen
    # )
    asset_obj = models.DevelopAsset(user_id = uid 
        ,assetname = assetname
        ,assetpath = assetpath
        ,assetprice_fen = assetprice_fen
    )
    db.add(asset_obj)
    db.commit()
    db.refresh(asset_obj)
    return asset_obj

def query_all_asset(db :Session):
    all = db.query( models.DevelopAsset).all()
    return list(filter(lambda x : x.asset_img_url is not None and x.assetinfo is not None,all))