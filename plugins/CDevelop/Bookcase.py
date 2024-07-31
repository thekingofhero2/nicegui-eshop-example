from nicegui import events,ui 
from frame import frame
from .CDevelop import left_navs
from typing import List
from DB.CRUD import *
from settings import *
from fastapi import Depends
import httpx

class Lightbox:
    """A thumbnail gallery where each image can be clicked to enlarge.
    Inspired by https://lokeshdhakar.com/projects/lightbox2/.
    """

    def __init__(self) -> None:
        #with ui.dialog().props('maximized').classes('bg-black') as self.dialog:
        with ui.dialog().classes('bg-black') as self.dialog:
            #ui.keyboard(self._handle_key)
            self.large_image = ui.image().props('no-spinner fit=scale-down')
            self.lb_info = ui.label("134342341").classes("text-white")
            self.btn_download = ui.button('下载')

        self.image_list: List[str] = []

    def add_image(self, asset_img_url: str, assetinfo: str,assetpath:str) -> ui.image:
        self.asset_img_url = asset_img_url
        self.assetinfo = assetinfo
        self.assetpath = assetpath
        """Place a thumbnail image in the UI and make it clickable to enlarge."""
        self.image_list.append(asset_img_url)
        with ui.button(on_click=lambda: self._open(asset_img_url)).props('flat dense square'):
            with ui.card().tight().classes('w-[300px] h-[300px]'):
                    ui.image(asset_img_url)
                    with ui.card_section():
                        ui.label(assetinfo.split("\n")[0])
                    

    def _handle_key(self, event_args: events.KeyEventArguments) -> None:
        if not event_args.action.keydown:
            return
        if event_args.key.escape:
            self.dialog.close()
        image_index = self.image_list.index(self.large_image.source)
        if event_args.key.arrow_left and image_index > 0:
            self._open(self.image_list[image_index - 1])
        if event_args.key.arrow_right and image_index < len(self.image_list) - 1:
            self._open(self.image_list[image_index + 1])

    async def _open(self, url: str) -> None:
        self.large_image.set_source(url)
        self.lb_info.set_text(self.assetinfo)
        self.btn_download.on_click = lambda: ui.download(os.path.join(self.assetpath,"asset.zip"))
        await self.dialog
        self.dialog.open()



@ui.page("/c_develop/bookcase")
async def Bookcase(db:Session = Depends(get_db)):
    lightbox = Lightbox()
    # async with httpx.AsyncClient() as client:  # using async httpx instead of sync requests to avoid blocking the event loop
    #     images = await client.get('https://picsum.photos/v2/list?page=4&limit=30')
    with frame("我的书架",left_navs,show_drawer=True):
        ui.label("我的书架") 
        with ui.row().classes(" justify-center w-full"):
            with ui.input(placeholder="书籍名称",).on("keyup.enter",handler=lambda e :ui.open(target=f'/DetailPage/{i.value}')).props("rounded outlined ").classes("w-96") as i:
                btn_search = ui.button("检索",on_click=lambda e :ui.open(target=f'/DetailPage/{i.value}')).props("flat dense")  
            
        ui.separator()
        with ui.row().classes('w-full'):
            ui.button(icon="add").classes('w-[300px] h-[200px]')
            for asset_obj in query_all_asset(db):
                print(asset_obj.asset_img_url,asset_obj.assetinfo)
                lightbox.add_image(
                    asset_img_url = asset_obj.asset_img_url,
                    assetinfo = asset_obj.assetinfo,
                    assetpath = asset_obj.assetpath
                )
            # for image in images.json():  # picsum returns a list of images as json data
            #     # we can use the image ID to construct the image URLs
            #     image_base_url = f'https://picsum.photos/id/{image["id"]}'
            #     # the lightbox allows us to add images which can be opened in a full screen dialog
                