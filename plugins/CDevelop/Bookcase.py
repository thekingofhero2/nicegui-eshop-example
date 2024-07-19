from nicegui import events,ui 
from frame import frame
from .CDevelop import left_navs
from typing import List
import httpx

class Lightbox:
    """A thumbnail gallery where each image can be clicked to enlarge.
    Inspired by https://lokeshdhakar.com/projects/lightbox2/.
    """

    def __init__(self) -> None:
        with ui.dialog().props('maximized').classes('bg-black') as self.dialog:
            ui.keyboard(self._handle_key)
            self.large_image = ui.image().props('no-spinner fit=scale-down')
        self.image_list: List[str] = []

    def add_image(self, thumb_url: str, orig_url: str) -> ui.image:
        """Place a thumbnail image in the UI and make it clickable to enlarge."""
        self.image_list.append(orig_url)
        with ui.button(on_click=lambda: self._open(orig_url)).props('flat dense square'):
            return ui.image(thumb_url)

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

    def _open(self, url: str) -> None:
        self.large_image.set_source(url)
        self.dialog.open()



@ui.page("/c_develop/bookcase")
async def Bookcase():
    lightbox = Lightbox()
    async with httpx.AsyncClient() as client:  # using async httpx instead of sync requests to avoid blocking the event loop
        images = await client.get('https://picsum.photos/v2/list?page=4&limit=30')
    with frame("我的书架",left_navs,show_drawer=True):
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