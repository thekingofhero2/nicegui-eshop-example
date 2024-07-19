from pathlib import Path
from nicegui import app
from dataclasses import dataclass,field
from typing import List
import os

@dataclass
class NavItem:
    """
    每一个导航链接（包含在每一个expander下）
    """
    nav_name :str
    uri :str
    module_path :str = field(compare=False)

@dataclass 
class LeftNav:
    """
    每个tab页对应的左侧导航,包含2级
    """
    expander_name :str
    nav_items :List[NavItem]

@dataclass
class Section:
    """
    每个tab页
    """
    section_name :str
    uri :str
    module_path :str = field(compare=False)
    #left_navs :List[LeftNav] = field(compare=False)

############基本配置#################"
ROOT = Path(__file__).parent
ASSETS_DIR = os.path.join(ROOT,"assets")
ASSET_DEFAULT_PIC = os.path.join(ASSETS_DIR,"default_asset_pic.png")
app.add_static_files("/assets", ROOT / "assets")


unrestricted_page_routes = {'/','/login','/register'}
#####################################

#######页面布局########
sections = [

    Section("管理后台","/c_develop",r"plugins.CDevelop")

            ]


#######数据库############
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
SQLALCHEMY_DB_URI = "sqlite:///./db2.db"
engine = create_engine(SQLALCHEMY_DB_URI,connect_args={"check_same_thread": False})




db_session =  sessionmaker(engine)
#Base.metadata.create_all(engine)


# Dependency
def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
