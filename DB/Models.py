from settings import Base,SQLALCHEMY_DB_URI
from sqlalchemy import Column,BIGINT,VARCHAR,Integer,TEXT,ForeignKey,Boolean
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uname = Column(VARCHAR(255) )
    pwd = Column(VARCHAR(64))

class DevelopAsset(Base):
    __tablename__ = "develop_asset"
    __table_args__ = {
        "comment":"资源"
    }
    id = Column(Integer,primary_key=True,autoincrement=True,comment = "id表示每一个资源")
    user_id = Column(Integer,ForeignKey("user.id"))
    user = relationship("User",backref="asset_of_user")
    
    asset_img_url = Column(VARCHAR(255),comment = "资源显示的图片url，可编辑修改")
    asset_before_img_url = Column(VARCHAR(255),comment = "资源付费前显示的图片url，可编辑修改")
    asset_after_img_url = Column(VARCHAR(255),comment = "资源付费后显示的图片url，可编辑修改")
    asset_8pic_url = Column(VARCHAR(255),comment = "资源在8图片上的地址")
    assetname = Column(VARCHAR(255))
    assetpath = Column(VARCHAR(255),comment = "资源压缩后的路径")
    assetinfo  = Column(TEXT)
    assetprice_fen = Column(Integer,comment = "资源价格,分")
    if_checked = Column(Boolean,comment = "是否已经检查完成",default = 0)
    shelves_status = Column(Integer,comment = "上架状态：0-未上架 1-已上架",default = 0)

