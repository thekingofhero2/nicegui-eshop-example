from nicegui import ui,app,Client,native
from fastapi import Request,Depends
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from pages.LoginPage.Login import login
from DB.DB import init_db,close_db
from DB.CRUD import *
from hashlib import md5
from frame import frame
from settings import *
from utils.Lightbox import Lightbox
class AuthMiddleware(BaseHTTPMiddleware):
    """This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get('authenticated', False):
            if request.url.path in Client.page_routes.values() and request.url.path not in unrestricted_page_routes:
                app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
                return RedirectResponse('/login')
        return await call_next(request)




app.on_startup(init_db)
app.on_shutdown(close_db)
app.add_middleware(AuthMiddleware)




@ui.page('/')
async def main_page(db:Session = Depends(get_db)) -> None:
    with frame("首页",[]):
        # with ui.column().classes('absolute-center items-center'):
        #     #ui.label(f'Hello {app.storage.user["username"]}!').classes('text-2xl')
        #     ui.button(on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login')), icon='logout') \
        #         .props('outline round')
        # if  app.storage.user.get('authenticated', False):
        #     check_res = check_pwd(db=db,uname = "admin",pwd=md5(b"123456").hexdigest())
        #     print(check_res)
        #     if check_res is not None:
        #         with ui.dialog() as dialog, ui.card():
        #             ui.label('请一定更新密码!')
        #             p1 = ui.input("新密码",placeholder="请一定记住",password=True,validation={'不要输入123456':lambda value: value != '123456'})
        #             p2 = ui.input("再次输入",placeholder="请一定记住",password=True,validation={'两次输入的不一致':lambda value:value ==p1.value})
        #             def save_pwd(e):
        #                 if p1.value == p2.value:
        #                     update_pwd(db ,"admin",md5(p2.value.encode("utf8")).hexdigest())
        #                     dialog.close()
        #             ui.button('保存并关闭', on_click=save_pwd)
        #         dialog.open()
        lightbox = Lightbox(db,False)
        with ui.row().classes('w-full'):
            for asset_obj in query_asset_by_shelves_status(db,shelves_status=1):
                lightbox.add_asset(asset_obj)
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
ui.run(host=local_ip,storage_secret="abc",reload=True, port=native.find_open_port())
