from nicegui import ui,app
from settings import *
from frame import frame 
from DB.CRUD import *
import DB.Models as Models
from fastapi import Depends
from hashlib import md5
import json
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
        ui.label("个人中心").classes("text-h2")
        ui.label('1.密码修改，请一定更新密码!').classes("text-h2 text-red-6")
        p_org = ui.input("原密码",password=True)
        p1 = ui.input("新密码",placeholder="请一定记住",password=True,validation={'不要输入123456':lambda value: value != '123456'})
        p2 = ui.input("再次输入",placeholder="请一定记住",password=True,validation={'两次输入的不一致':lambda value:value ==p1.value})
        def save_pwd(e):
            if check_pwd(db,'admin',md5(p_org.value.encode("utf8")).hexdigest()) is None:
                ui.notification("原密码错误",type="warning")
            elif p1.value == p2.value:
                update_pwd(db ,"admin",md5(p2.value.encode("utf8")).hexdigest())
        ui.button('保存密码', on_click=save_pwd)
        ui.separator()
        ui.label('2.参数配置').classes("text-h2 text-red-6")
        #jisu_pic_token
        #pic8_pid 
        #pic8_key 
        
        if os.path.exists('auth.auth'):
            with open('auth.auth') as fp:
                app.storage.user['auth_config'] = json.load(fp)
        else:
            app.storage.user['auth_config'] = {"jisu_pic_token":"","pic8_pid":"","pic8_key":""}
        
        jisu_pic_token = ui.input("极速图床的token").bind_value(app.storage.user['auth_config'],"jisu_pic_token")
        pic8_pid = ui.input("8pic的PID").bind_value(app.storage.user['auth_config'],"pic8_pid")
        pic8_key = ui.input("8pic的key").bind_value(app.storage.user['auth_config'],"pic8_key")
        def save_auth(e):
            with open('auth.auth','w') as fpw:
                json.dump(app.storage.user['auth_config'],fp=fpw)
        ui.button('保存账号信息', on_click=save_auth)
        # #待上架（待验证（）/已验证）