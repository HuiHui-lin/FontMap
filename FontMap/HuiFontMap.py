import json
from fontTools.ttLib import TTFont
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.misc.transform import Offset
import os
from tqdm import tqdm



class HuiFontMap:
    def __init__(self,fontpath,savepath,issaveimg=True):
       """
       初始化读取字体和获取字体文件映射
       :param font: 字体文件路径
       :param savepath:字形图片保存路径
       :param issaveimg:是否开启保存图片
       """
       self.font = TTFont(fontpath) # 实例化TTFont
       self.savepath = savepath
       self.cmap = self.font.getBestCmap()
       if issaveimg:
        self.saveFontImg(cmap=self.cmap,savepath=savepath)
    def saveFontImg(self,cmap,savepath):
        """
        根据字体文件生成对应字形图像并保存
        :param cmap:字符映射字典
        :param savepath:生成的字形图像保存地址
        :return:无返回值。函数执行后，字形图像将被保存到指定路径。
        """
        from PIL import Image
        for i in tqdm(cmap, desc='任务进行中', unit='items'):
            pen = FreeTypePen(None)  # 实例化Pen子类
            glyph = self.font.getGlyphSet()[cmap[i]] # 通过字形名称选择某一字形对象
            glyph.draw(pen) # “画”出字形轮廓
            width, ascender, descender = glyph.width, self.font['OS/2'].usWinAscent, -self.font['OS/2'].usWinDescent # 获取字形的宽度和上沿以及下沿
            height = ascender - descender # 利用上沿和下沿计算字形高度
            fontimg = pen.image(width=width, height=height, transform=Offset(0, -descender))
            original_width, original_height = fontimg.size
            proportional_size= self.__get_proportional_size(original_width,original_height)
            resizeimg = fontimg.resize(proportional_size, Image.Resampling.LANCZOS)
            old_size = resizeimg.size
            new_size = (400,400)
            red_background = Image.new("RGBA", (400,400), 'red') #红色背景
            red_background.paste(resizeimg, (int((new_size[0] - old_size[0]) / 2),
                                  int((new_size[1] - old_size[1]) / 2)),resizeimg.split()[1])
            red_background.save(os.path.join(savepath ,cmap[i] + '.png'))

        print('字形图片保存完毕')
    def ocrFontImg(self,jsonpath = None):
        """
        :param jsonpath: ocr字典结果的保存路径，默认不保存
        :return: 返回一个ocr识别字典结果
        """
        import ddddocr
        import unicodedata
        ocr = ddddocr.DdddOcr()
        file_list = os.listdir(self.savepath)
        dis  = {}
        reversed_dict = {value: key for key, value in self.cmap.items()}
        for i in file_list:
            imgname = i.split('.')[0]
            if imgname in reversed_dict:
                try:
                    unicodedata.name(chr(reversed_dict[imgname]))
                    dis[imgname] = chr(reversed_dict[imgname])
                    continue
                except ValueError:
                    path = os.path.join(self.savepath,i)
                    with open(path, 'rb') as f:
                        img_bytes = f.read()
                        res = ocr.classification(img_bytes)
                        dis[imgname]=res
            else:
                continue
        print('识别完毕')
        if jsonpath!= None:
            with open(jsonpath, 'w', encoding='utf-8') as f:
                json.dump(dis,fp=f,ensure_ascii=False)
            print('文件已保存')
        return dis
    def __get_proportional_size(self,original_width, original_height):
        """
        notes:此对象的私有方法，用于计算字体等比例宽高
        :param original_width: 原始字形宽
        :param original_height: 原始字形高
        :return : 返回计算后的宽度和高度
        """
        max_size = 200
        aspect_ratio = original_width / original_height
        if original_width > original_height:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(max_size * aspect_ratio)
        return (new_width,new_height)


if __name__ == '__main__':
    hui = HuiFontMap(fontpath=r"C:\Users\21761\Desktop\file.woff",savepath=r"C:\Users\21761\Desktop\新建文件夹",issaveimg=False)
    diststr = hui.ocrFontImg()



