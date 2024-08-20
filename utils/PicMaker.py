from PIL import Image, ImageDraw, ImageFont
import os 
from settings import ROOT

class PicMaker:
    def __init__(self):
        #self.font_path = os.path.join(ROOT,'assets','fonts','LinHaiLiShu-Regular_V1.002.ttf')
        self.font_path = os.path.join(ROOT,'assets','fonts','simhei.ttf')
    
    def maker(self,title="资源的基本信息：",text = "你好啊",img_filename = 'text_image.png'):
        """
        text：设置文本内容
        """
        # 设置图片大小
        width, height = 800, 800
        image = Image.new('RGB', (width, height), color = 'white')
        
        # 获取文字大小
        #text_width, text_height = font.getsize(text)
        
        # 计算文字位置
        x = (width ) / 2
        y = (height ) / 2
        
        # 创建画布
        draw = ImageDraw.Draw(image)
        
        #绘制小字
        draw.text((10,  40), text=title, font=ImageFont.truetype(self.font_path, 30), fill='black')

        # 绘制文字
        draw.text((10, (height ) / 2), text, font=ImageFont.truetype(self.font_path, 60), fill='black')
        # 绘制文字
        draw.text((10, height - 60), "请用支付宝扫码支付", font=ImageFont.truetype(self.font_path, 20), fill='black')
        #绘制小字
        draw.text(((width ) / 2, height - 20), "感谢字体`simhei`", font=ImageFont.truetype(self.font_path, 20), fill='red')
        # 保存图片
        image.save(img_filename)


if __name__ == '__main__':
    obj = PicMaker()
    obj.maker()