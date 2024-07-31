from nicegui import ui,app
from settings import *
from frame import frame 
from DB.CRUD import *
import DB.Models as Models
from fastapi import Depends

left_navs = [
    NavItem("我的资源","/c_develop/bookcase",r"plugins.CDevelop.Bookcase"),
    # NavItem("地图获客","/search/mapsearch",r"plugins.CustomSearch.SearchOnMap"),
    # NavItem("商机获客","/search/dealsearch",r"plugins.CustomSearch.DealSearch"),
    NavItem(None,"",r""),
    NavItem("工作台","/c_develop/workspace",r"plugins.CDevelop.Workspace")
            ]

@ui.page("/c_develop")
async def CDevelop(db :Session = Depends(get_db)):
    with frame("管理后台",left_navs,show_drawer=True):
        ui.label("创作中心")
        #已上架
        
       
        # #待上架（待验证（）/已验证）