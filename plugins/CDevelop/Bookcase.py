from nicegui import events,ui 
from frame import frame
from .CDevelop import left_navs
from typing import List
from DB.CRUD import *
import DB.Models as Models
from settings import *
from fastapi import Depends
from utils.Lightbox import Lightbox


@ui.page("/c_develop/bookcase")
async def Bookcase(db:Session = Depends(get_db)):
    lightbox = Lightbox(db,True)
    # async with httpx.AsyncClient() as client:  # using async httpx instead of sync requests to avoid blocking the event loop
    #     images = await client.get('https://picsum.photos/v2/list?page=4&limit=30')
    with frame("我的资源",left_navs,show_drawer=True):
        # with ui.row().classes(" justify-center w-full"):
        #     with ui.input(placeholder="资源关键词",).on("keyup.enter",handler=lambda e :ui.open(target=f'/DetailPage/{i.value}')).props("rounded outlined ").classes("w-96") as i:
        #         btn_search = ui.button("检索",on_click=lambda e :ui.open(target=f'/DetailPage/{i.value}')).props("flat dense")  
            
        #ui.separator()
        with ui.row().classes('w-full'):
            asset_list = query_all_asset(db)
            if len(asset_list) == 0:
                ui.label("空空如也,快去工作台添加资源~").classes("text-h2")
            else:
                for asset_obj in asset_list:
                    lightbox.add_asset(asset_obj)
               