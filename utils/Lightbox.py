from nicegui import events,ui 
from typing import List
from DB.CRUD import *
import DB.Models as Models
from settings import *
class Lightbox:
   
    def __init__(self,db,if_edit) -> None:
        with ui.dialog().classes('bg-black') as self.dialog:
            self.large_image = ui.image().props('no-spinner fit=scale-down')
            self.lb_info = ui.label("134342341").classes("text-white")
        self.if_edit = if_edit    
        self.db = db
        self.image_list: List[str] = []
        self.asset_list: List[Models.DevelopAsset] = []

  
    def add_asset(self, asset_obj: Models.DevelopAsset) -> ui.image:
        
        """Place a thumbnail image in the UI and make it clickable to enlarge."""
        self.asset_list.append(asset_obj.id)
        
        self.image_list.append(asset_obj.asset_img_url)
        with ui.card().tight().classes('w-[300px] h-[300px]'):
            with ui.button(on_click=lambda: self._open(asset_obj.asset_img_url,asset_obj.assetinfo)).props('flat dense square'):
                ui.image(asset_obj.asset_img_url)
                with ui.card_section():
                    ui.label(asset_obj.assetinfo.split("\n")[0])
            with ui.row():
                ui.button('下载',on_click=lambda : ui.download(os.path.join(asset_obj.assetpath,"asset.zip")))
                if self.if_edit:
                    self.ui_shelves_status = ui.switch("上架",value = asset_obj.shelves_status != 0,on_change = lambda x:self.update_shelves_status(asset_obj.id,x.value))
    def update_shelves_status(self,asset_id,shelves_status):
        this_asset_obj = query_asset_by_id(self.db,asset_id)
        if shelves_status :
            this_asset_obj.shelves_status = 1
        else:
            this_asset_obj.shelves_status = 0
       
        self.db.commit()
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

    def _open(self, url: str,assetinfo: str) -> None:
        self.large_image.set_source(url)
        self.lb_info.set_text(assetinfo)

        self.dialog.open()
   