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
import httpx
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
        if  app.storage.user.get('authenticated', False):
            check_res = check_pwd(db=db,uname = "admin",pwd=md5(b"123456").hexdigest())
            print(check_res)
            if check_res is not None:
                with ui.dialog() as dialog, ui.card():
                    ui.label('请一定更新密码!')
                    p1 = ui.input("新密码",placeholder="请一定记住",password=True,validation={'不要输入123456':lambda value: value != '123456'})
                    p2 = ui.input("再次输入",placeholder="请一定记住",password=True,validation={'两次输入的不一致':lambda value:value ==p1.value})
                    def save_pwd(e):
                        if p1.value == p2.value:
                            update_pwd(db ,"admin",md5(p2.value.encode("utf8")).hexdigest())
                            dialog.close()
                    ui.button('保存并关闭', on_click=save_pwd)
                dialog.open()
        lightbox = Lightbox()
    async with httpx.AsyncClient() as client:  # using async httpx instead of sync requests to avoid blocking the event loop
        images = await client.get('https://picsum.photos/v2/list?page=4&limit=30')
        ui.label("我的书架") 
        with ui.row().classes(" justify-center w-full"):
            with ui.input(placeholder="书籍名称",).on("keyup.enter",handler=lambda e :ui.open(target=f'/DetailPage/{i.value}')).props("rounded outlined ").classes("w-96") as i:
                btn_search = ui.button("检索",on_click=lambda e :ui.open(target=f'/DetailPage/{i.value}')).props("flat dense")  
            
        ui.separator()
        with ui.row().classes('w-full'):
            ui.button(icon="add").classes('w-[300px] h-[200px]')
            for image in images.json():  # picsum returns a list of images as json data
                # we can use the image ID to construct the image URLs
                image_base_url = f'https://picsum.photos/id/{image["id"]}'
                # the lightbox allows us to add images which can be opened in a full screen dialog
                lightbox.add_image(
                    thumb_url=f'{image_base_url}/300/200',
                    orig_url=f'{image_base_url}/{image["width"]}/{image["height"]}',
                ).classes('w-[300px] h-[200px]')
#ui.run(storage_secret="abc")
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
ui.run(host=local_ip,storage_secret="abc",reload=True, port=native.find_open_port())
