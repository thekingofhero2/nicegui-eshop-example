from nicegui import ui ,events,app
from frame import frame
from .CDevelop import left_navs
import os
import time
import requests
import json
from fastapi import Depends
from sqlalchemy.orm import Session
from settings import *
import DB.CRUD as crud
from utils.PicMaker import PicMaker
from utils.ZipTools import ZipTools

class AssetFileMaker:
    def __init__(self,db):
        self.db = db
        self.init()
    
    def init(self,):
        #文件上传路径
        self.asset_org_dir = None
        self.asset_des_dir = None
        self.asset_before_img_path = None
        self.asset_after_img_path = None
        
        #信号
        self.signals_dict = {
            "task.show":False
            ,"ready_show_pic" : False 
            ,"first_next_step" :False
            ,"second_next_step" :False
            ,"complete_step" :False

        } 
        #本资源对象，在第一次创建后变成数据库对象
        self.asset_obj = None
        #本资源相关属性
        self.asset_obj_dict = {
            "assetname":"请输入文件名",
            "assetpwd":"123456",
            "assetpath":None, #文件上传路径
            "assetinfo":f"""本资源包含：*********请添加资源说明****************
                        资源内容需要解压“encrypted.zip”，解压密码需要付费后可见，付费链接 : ***********点击“生成图片”后自动更新***************
                        声明：本资源符合国家法律要求，保证无不良引导。资源内容仅供学习参考使用。
                        """,
            "assetprice":1.99,
            "asset_img_url":"/assets/default_asset_pic.png",
            "asset_before_img_url":"https://vip.helloimg.com/i/2024/08/19/66c2e85ed9851.jpg",
            "asset_after_img_url":"https://vip.helloimg.com/i/2024/08/19/66c2e86041462.jpg",
            "asset_8pic_url":None,
            "if_checked":False
            
        }
        

    def multi_upload(self,e:events.MultiUploadEventArguments):
        for filename,filecontent in zip(e.names,e.contents):
            with open(os.path.join(self.asset_org_dir,filename),"wb") as fp:
                fp.write(filecontent.read())
        pass

    def upload_image(self,):
        
        
   
        
        pic_token = app.storage.user['auth_config']['pic_token']
        pic8_pid = app.storage.user['auth_config']['pic8_pid']
        pic8_key = app.storage.user['auth_config']['pic8_key']
        if pic_token == '' or \
           pic8_pid == '' or \
            pic8_key == ''   :
            ui.notify("请回到管理后台，填写“2.参数配置”并做好验证",position="center",type="warning")
            return
        ##################
        
        # files=[
        #         ('file',('04069acbef5bb66fcaba8365c95d3a95.jpg',open('/D:/04069acbef5bb66fcaba8365c95d3a95.jpg','rb'),'image/jpeg'))
        #         ]
        

        # response = requests.request("POST", url, headers=headers, data=payload, files=files)
        """
        上传付费前可看见的图片
        """
        with open(self.asset_before_img_path,'rb') as fp:
            res = requests.post("https://tucdn.wpon.cn/api/upload",files={"image":(f"{time.time()}.jpg",fp.read())},headers={"token":pic_token})
        
        res_json = json.loads(res.content.decode("utf-8"))
        #print(res_json)
        if res_json['code'] == 200:
            self.asset_obj_dict["asset_before_img_url"] = res_json["data"]["url"]

        """
        上传付费后可看见的图片
        """
        with open(self.asset_after_img_path,'rb') as fp:
            res = requests.post("https://tucdn.wpon.cn/api/upload",files={"image":(f"{time.time()}.png",fp.read())},headers={"token":pic_token})
        #print("--")
        res_json = json.loads(res.content.decode("utf-8"))
        #print(res_json)
        if res_json['code'] == 200:
            self.asset_obj_dict["asset_after_img_url"] = res_json["data"]["url"]

        # 其他图床"""
        # 上传付费前可看见的图片
        # pic_headers = {
        #     'Authorization': 'Bearer '+pic_token,
        #     'Accept': 'application/json',
        #     }
        # """
        # with open(self.asset_before_img_path,'rb') as fp:
        #     res = requests.post("https://www.helloimg.com/api/v1/upload",files={'file': (self.asset_before_img_path,fp,'image/jpeg')},headers=pic_headers,verify=False)
        # if res.status_code == 200:
        #     res_json = json.loads(res.content.decode("utf-8"))
        #     if res_json['status'] :
        #         self.asset_obj_dict["asset_before_img_url"] = res_json['data']['links']['url']
        # """
        # 上传付费后可看见的图片
        # """
        # with open(self.asset_after_img_path,'rb') as fp:
        #     res = requests.post("https://www.helloimg.com/api/v1/upload",files={'file': (self.asset_after_img_path,fp,'image/jpeg')},headers=pic_headers,verify=False)
        # if res.status_code == 200:
        #     res_json = json.loads(res.content.decode("utf-8"))
        #     if res_json['status'] :
        #         self.asset_obj_dict["asset_after_img_url"] = res_json['data']['links']['url']

        time.sleep(1)

        ############上传图片至8图片
        to_8pic_url = f"""http://web.8tupian.com/api/b.php?act=up2&pic={self.asset_obj_dict["asset_before_img_url"]}&pic2={self.asset_obj_dict["asset_after_img_url"]}&price={int(float(self.asset_obj_dict["assetprice"]) * 100)}&pid={pic8_pid}&key={pic8_key}"""   
        #to_8pic_url = f"""http://web.8tupian.com/api/b.php?act=up2&pic={self.asset_obj_dict["asset_before_img_url"]}&pic2={self.asset_obj_dict["asset_after_img_url"]}&price=1&pid={pic8_pid}&key={pic8_key}""" 
        #print(to_8pic_url)
        res = requests.post(to_8pic_url)
        #print(res)
        res_json = json.loads(res.content.decode("utf-8"))
        #print(res_json)
        if res_json['code'] == 0:
            self.asset_obj_dict["asset_pic8_url"] = res_json["picurl"]
                #break
        ##############


        # self.asset_obj_dict["asset_before_img_url"]  = "https://tucdn.wpon.cn/2024/07/19/ecbab3ee7a236.png"
        # self.asset_obj_dict["asset_after_img_url"] = "https://tucdn.wpon.cn/2024/07/19/363fa34185f7b.png"
        # self.asset_obj_dict["asset_pic8_url"] = "http://dt2.8tupian.net/2/14535a32b1.pg1"
        try:
            if self.asset_obj_dict["asset_pic8_url"] is not None:
                    self.asset_obj_dict["assetinfo"] = f"""本资源包含：*********请添加资源说明****************
                            资源内容需要解压“encrypted.zip”，解压密码需要付费后可见，付费链接 : {self.asset_obj_dict["asset_pic8_url"]}
                            声明：本资源符合国家法律要求，保证无不良引导。资源内容仅供学习参考使用。
                            """
                    self.asset_obj.assetinfo = self.asset_obj_dict["assetinfo"]
                    self.asset_obj.asset_before_img_url = self.asset_obj_dict["asset_before_img_url"]
                    self.asset_obj.asset_after_img_url = self.asset_obj_dict["asset_after_img_url"]
                    self.asset_obj.asset_8pic_url = self.asset_obj_dict["asset_pic8_url"]
                    self.db.commit()
            else:
                print("上传失败，请重试1",type="warning")
        except:
            print("上传失败，请重试2",type="warning")  
            

    def add_new_one(self,e:events.ClickEventArguments):
        self.init()
        self.signals_dict["task.show"] = False
        #self.asset_obj_dict["assetpath"] = os.path.join(ASSETS_DIR,"uploads",str(time.time()))
        self.asset_obj_dict["assetpath"] = os.path.join("uploads",str(time.time()))
        self.asset_org_dir = os.path.join(self.asset_obj_dict["assetpath"],"org")
        self.asset_des_dir = os.path.join(self.asset_obj_dict["assetpath"],"des")
        self.asset_before_img_path = os.path.join(self.asset_obj_dict["assetpath"],"付费前图片.jpg")
        self.asset_after_img_path = os.path.join(self.asset_obj_dict["assetpath"],"付费后图片.jpg")
        #本资源根目录
        os.makedirs(self.asset_obj_dict["assetpath"])
        #本资源原始文件目录
        os.mkdir(self.asset_org_dir)
        #本资源目标目录
        os.mkdir(self.asset_des_dir)
        self.signals_dict["task.show"] = True
        self.ui_maker.refresh()

    def gen_pic(self,e:events.ClickEventArguments):
        spinner = ui.spinner(size='lg')
        obj = PicMaker()
        obj.maker(title=f"“{self.ui_filename.value}”，付费后可查看密码",text=f"密码是：XXXXXXXX",img_filename=self.asset_before_img_path)
        obj.maker(title=f"“{self.ui_filename.value}”，您已付费",text=f"密码是：{self.ui_pwd.value}",img_filename=self.asset_after_img_path)
        self.upload_image()
        if "ready_show_pic" in self.signals_dict.keys() \
            and self.asset_obj_dict["asset_before_img_url"] is not None \
            and self.asset_obj_dict["asset_after_img_url"] is not None:
            
            self.signals_dict["ready_show_pic"] = True
        self.pic_show.refresh()
        spinner.visible = False

    @ui.refreshable
    def pic_show(self,):
        im1 = ui.image(self.asset_obj_dict["asset_before_img_url"]).props("bordered").classes('w-[300px] h-[300px] shadow-10').bind_visibility(self.signals_dict,"ready_show_pic")
        im2 = ui.image(self.asset_obj_dict["asset_after_img_url"]).props("bordered").classes('w-[300px] h-[300px] shadow-10').bind_visibility(self.signals_dict,"ready_show_pic")  
        im1.force_reload()
        im2.force_reload()

    @ui.refreshable
    def ui_maker(self,):
        
        with ui.row().classes("w-full justify-centrer").bind_visibility(self.signals_dict,"task.show"):
            with ui.stepper().classes('w-full') as stepper:
                with ui.step('一、资源制作'):
                    with ui.stepper_navigation():
                        with ui.column():
                            ui.label("1.输入资源名称").classes("text-h6 text-blue-grey-9")
                            self.ui_filename = ui.input("资源名称",placeholder="资源名称长度应该在16位以内",validation={'名称太长了': lambda value: len(value) <= 16,
                                                                                                        '名称不能为空':lambda value : len(value) > 0,
                                                                                                        '资源名称有重复':lambda value: not crud.check_asset_exists(self.db ,value)}).bind_value(self.asset_obj_dict,"assetname")
                            ui.label("2.选择要上传的文件(点击“+”添加文件，然后点击“上传按钮”进行上传)").classes("text-h6 text-blue-grey-9")
                            ui_targetfile = ui.upload(multiple=True,on_multi_upload=self.multi_upload)
                            ui.label("3.设置加密密码").classes("text-h6 text-blue-grey-9")
                            self.ui_pwd = ui.input("密码",placeholder="输入长度应该在8位以内",validation={'密码太长了': lambda value: len(value) <= 8}).bind_value(self.asset_obj_dict,"assetpwd")
                            ui.label("4.资源售价(元)").classes("text-h6 text-blue-grey-9")
                            self.ui_asset_price = ui.input("价格",placeholder="价格（元），如“1.99”",value="1.99").bind_value(self.asset_obj_dict,"assetprice")
                            ui.button("暂存(每次修改都需要暂存一下)",on_click = self.create_asset)
                            ui.button('下一步', on_click = stepper.next).bind_visibility(self.signals_dict,"first_next_step")
                with ui.step('二、密码图片上传'):
                    with ui.stepper_navigation():
                        with ui.column():
                            ui.label("5.生成付费前后的图片").classes("text-h6 text-blue-grey-9")
                            with ui.row().classes("w-full"):
                                ui.button("生成图片",on_click=self.gen_pic)
                                self.pic_show()
                            ui.label("6.资源说明").classes("text-h6 text-blue-grey-9")
                            self.ui_asset_info = ui.textarea(label='资源说明如下：').classes("w-[800px] h-[200px]").bind_value(self.asset_obj_dict,"assetinfo")
                            ui.label("7.生成加密文件").classes("text-h6 text-blue-grey-9")
                            ui.button("生成文件",on_click = self.make_zipfile)
                            with ui.row():
                                ui.button('上一步', on_click=stepper.previous).props('flat')
                                ui.button('下一步', on_click=stepper.next).bind_visibility(self.signals_dict,"second_next_step")
                with ui.step('三、资源验证'):
                    ui.label('下载资源，尝试在本地电脑解压，并检查文件内容是否正确')
                    with ui.stepper_navigation():
                        with ui.column():
                            with ui.card().tight().classes('w-[300px] h-[300px]'):
                                ui.image(self.asset_obj_dict["asset_img_url"])
                                with ui.card_section():
                                    ui.label(self.asset_obj_dict["assetinfo"].split("\n")[0])
                                ui.button('下载到本地检查', on_click=lambda: ui.download(os.path.join(self.asset_obj_dict["assetpath"],"asset.zip")))
                            ui.label("""核验内容应包含：""")
                            ui.label("""①文件是否完整""")
                            ui.label("""②密码是否可用""")
                                                        
                            ui.checkbox("检查已完成",on_change=self.update_checked).bind_value(self.asset_obj_dict,"if_checked")
                            with ui.row():
                                ui.button('上一步', on_click=stepper.previous).props('flat')
                                ui.button('完成', on_click=lambda: ui.notify('完成，可以回到资源管理页面查看!', type='positive')).bind_visibility(self.signals_dict,"complete_step")
    def create_asset(self,):
        uid = app.storage.user["uid"]
        if len(self.ui_filename.value) == 0 :
            ui.notify("暂存失败，1.资源名称不能为空")
            return 
        if len(self.ui_pwd.value) == 0:
            ui.notify("暂存失败，密码不能为空")
            return 
        if self.asset_obj is None:
            self.asset_obj = crud.create_asset(db=self.db 
                            ,uid=uid
                                ,assetname = self.asset_obj_dict["assetname"]
                                ,assetpath = self.asset_obj_dict["assetpath"]
                                ,assetprice_fen = int(float(self.asset_obj_dict["assetprice"]) * 100))
        else:
            self.asset_obj.assetname = self.asset_obj_dict["assetname"]
            self.asset_obj.assetpath = self.asset_obj_dict["assetpath"]
            self.asset_obj.assetprice_fen = int(float(self.asset_obj_dict["assetprice"]) * 100)
            self.db.commit()
        self.signals_dict["first_next_step"] = True

    def make_zipfile(self,):
        self.asset_obj.assetinfo = self.asset_obj_dict["assetinfo"]
        with open(os.path.join(self.asset_des_dir,"说明.txt"),'w') as fpw:
            fpw.write( self.asset_obj_dict["assetinfo"])
        # 创建一个加密的ZIP文件
        ZipTools.zip_folder(self.asset_org_dir, os.path.join(self.asset_des_dir,"encrypted.zip"), self.ui_pwd.value)

        # 创建包含资源的非加密的ZIP文件
        ZipTools.zip_folder(self.asset_des_dir, os.path.join(self.asset_obj_dict["assetpath"],"asset.zip"))

        self.signals_dict["second_next_step"] = True
        self.db.commit()

    def update_checked(self,e :events.ValueChangeEventArguments):
        self.asset_obj_dict['if_checked'] = e.value
        if self.asset_obj_dict['if_checked']:
            self.signals_dict["complete_step"] = True
        else:
            self.signals_dict["complete_step"] = False
        self.asset_obj.asset_img_url = self.asset_obj_dict['asset_img_url']
        self.asset_obj.if_checked = self.asset_obj_dict['if_checked']
        self.db.commit()


  
@ui.page("/c_develop/workspace")
async def Workspace(db:Session = Depends(get_db)):
    obj = AssetFileMaker(db)
    with frame("我的工作台",left_navs,show_drawer=True):
        ui.button("点击按钮，创建一个新任务",on_click=obj.add_new_one)
        obj.ui_maker()
        
        