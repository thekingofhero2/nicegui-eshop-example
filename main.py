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
        contact_way = {'contact_way':"尚未更新联系方式，请勿购买!"}
        ui.label().bind_text(contact_way,'contact_way').classes("text-h2 text-red-6")
        if os.path.exists('auth.contact'):
            import json
            with open('auth.contact') as fp:
                contact_way_js = json.load(fp)
            contact_way['contact_way'] = "以下资源如有使用问题请联系："+contact_way_js['contact_way']
        lightbox = Lightbox(db,False)
        with ui.row().classes('w-full'):
            for asset_obj in query_asset_by_shelves_status(db,shelves_status=1):
                lightbox.add_asset(asset_obj)
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
ui.run(host=local_ip,storage_secret="abc",reload=False, port=native.find_open_port())
