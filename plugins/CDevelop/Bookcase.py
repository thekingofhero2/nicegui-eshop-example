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
            for asset_obj in query_all_asset(db):
                
                lightbox.add_asset(asset_obj)
                # lightbox.add_image(
                #     asset_img_url = asset_obj.asset_img_url,
                #     assetinfo = asset_obj.assetinfo,
                #     assetpath = asset_obj.assetpath
                # )
            # for image in images.json():  # picsum returns a list of images as json data
            #     # we can use the image ID to construct the image URLs
            #     image_base_url = f'https://picsum.photos/id/{image["id"]}'
            #     # the lightbox allows us to add images which can be opened in a full screen dialog
                