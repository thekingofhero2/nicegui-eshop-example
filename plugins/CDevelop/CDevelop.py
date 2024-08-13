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
        with ui.row().classes("w-full"):
            with ui.column().classes("col-span-7"):
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
                contact_way = ui.input("联系方式（qq/微信/电话/邮箱等，展示在首页）")
                def save_auth(e):
                    with open('auth.auth','w') as fpw:
                        json.dump(app.storage.user['auth_config'],fp=fpw)
                    with open('auth.contact','w') as fpw:
                        json.dump({"contact_way":contact_way.value},fp=fpw)
                ui.button('保存账号信息', on_click=save_auth)
            with ui.column().classes("col-span-5"):
                @ui.refreshable
                def check_8pic():
                    url = f"http://web.8tupian.com/api/a.php?act=query&pid={app.storage.user['auth_config']['pic8_pid']}&key={app.storage.user['auth_config']['pic8_key']}"
                    import requests 
                    res = requests.get(url)
                    js = json.loads(res.content.decode('utf-8'))
                    if js['code'] == 0:
                        with ui.card():
                            ui.label(f"用户名：{js['name']}")
                            ui.label(f"联系QQ:{js['contactqq']}")
                            ui.label(f"联系邮箱：{js['email']}")
                            ui.label(f"联系电话：{js['phone']}")
                            ui.label(f"注册时间：{js['registerTime']}")
                            ui.label(f"最后登录时间：{js['lastlandtime']}")
                            ui.label(f"账户余额：{float(js['balance'])/100}")
                            ui.label(f"支付宝账号：{js['zfb_account']}")
                            ui.label(f"结算次数：{js['jiesuannum']}")
                            ui.label(f"历史结算总金额：{float(js['jiesuansum'])/100}")
                            ui.label(f"账户状态：{'正常' if js['warning'] == '0' else '异常'}")
                    else:
                        ui.label("参数错误")    
                ui.button('验证8图片',on_click=lambda : check_8pic.refresh())
                check_8pic()
        # #待上架（待验证（）/已验证）