from nicegui import ui,app,client
from contextlib import contextmanager
from importlib import import_module
from settings import * 

    

@contextmanager
def frame(nav_title :str,left_navs :List[NavItem],show_drawer=False):
    ui.page_title(nav_title)
    with ui.header().classes("shadow-12 bg-blue-grey-10"):
        with ui.row().classes("w-full items-center"):
            if  nav_title!="首页":
                ui.button(icon='menu',on_click=lambda :left_drawer.toggle() ).props('flat color=white')           
            with ui.link(target="/"):
                ui.button("NiceGUI_eshop").props("flat").style("font-size:150%;font-width:300").classes("text-yellow-6")
                #ui.button("jjz").props("flat").style("font-size:150%;font-width:300").classes("text-yellow-6")
            for section in sections:
                with ui.link(target = section.uri):
                    import_module(section.module_path)
                    ui.button(section.section_name).props("flat").classes("text-blue-grey-1")
            ui.space()
            if  app.storage.user.get('authenticated', False):
                ui.label(f'Hello {app.storage.user["username"]}!')
                ui.button(on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login'))
                        , icon='logout').props('outline round')
            else:
                ui.button(text="请登录",on_click=lambda: (app.storage.user.clear(), ui.navigate.to('/login'))
                        , icon='login').props('outline ')
    if  nav_title!="首页":
        with ui.left_drawer(value = show_drawer).classes("bg-blue-grey-1") as left_drawer:
            for item in left_navs:
                if item.nav_name is not None:
                    with ui.link(target = item.uri):
                            import_module(item.module_path)
                            ui.button(item.nav_name).props("flat").classes("text-blue-grey-10")
                else:
                    ui.separator()
    yield