from nicegui import ui,app
from settings import NavItem
from frame import frame 

left_navs = [
    NavItem("我的资源","/c_develop/bookcase",r"plugins.CDevelop.Bookcase"),
    # NavItem("地图获客","/search/mapsearch",r"plugins.CustomSearch.SearchOnMap"),
    # NavItem("商机获客","/search/dealsearch",r"plugins.CustomSearch.DealSearch"),
    NavItem(None,"",r""),
    NavItem("工作台","/c_develop/workspace",r"plugins.CDevelop.Workspace")
            ]

@ui.page("/c_develop")
async def CDevelop():
    with frame("管理后台",left_navs,show_drawer=True):
        ui.label("创作中心")