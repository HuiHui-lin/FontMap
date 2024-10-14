from fontTools.ttLib import TTFont
import os
from PIL import Image
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.misc.transform import Offset


class HuiFontMap:
    """
    HuiFontMap 类用于初始化读取字体文件并获取字体映射，同时支持将字形保存为图片。
    默认是保存图片之后进行识别，方便肉眼对比，不建议生成图片就立即识别，不保存图片数据。
    """

    def __init__(self, fontpath: str, savepath: str, issaveimg: bool = True):
        """
        初始化读取字体和获取字体文件映射。

        :param fontpath: 字体文件路径
        :param savepath: 字形图片保存路径
        :param issaveimg: 是否开启保存图片
        """
        self.font = TTFont(fontpath)  # 实例化TTFont
        self.savepath = savepath
        self.cmap = self.font.getBestCmap()
        if issaveimg:
            self.__saveFontImg()

    def __save(self, value:dict):
        """
        :param value: 多线程传递的参数体
        :return: 无返回值
        """
        glyph =value['glyph']
        cmapid = value['cmapid']
        pen = FreeTypePen(None)  # 实例化Pen子类
        glyph.draw(pen)  # “画”出字形轮廓

        width, ascender, descender = (
            glyph.width,
            self.font['OS/2'].usWinAscent,
            -self.font['OS/2'].usWinDescent
        )  # 获取字形的宽度和上沿以及下沿

        height = ascender - descender  # 利用上沿和下沿计算字形高度
        fontimg = pen.image(width=width, height=height, transform=Offset(0, -descender))

        original_width, original_height = fontimg.size
        proportional_size = self.__get_proportional_size(original_width, original_height)
        resizeimg = fontimg.resize(proportional_size, Image.Resampling.LANCZOS)

        old_size = resizeimg.size
        new_size = (200, 200)
        white_background = Image.new("RGBA", (200, 200), 'white')  # 白色背景
        white_background.paste(
            resizeimg,
            (int((new_size[0] - old_size[0]) / 2), int((new_size[1] - old_size[1]) / 2)),
            resizeimg.split()[1]
        )
        white_background.save(os.path.join(self.savepath, cmapid + '.png'))

    def __saveFontImg(self):
        """
        根据字体文件生成对应字形图像并保存。
        使用多线程加快生成速度
        """
        # 经过对比，线程池比进程池生成图片速度更快
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=3) as executor:
            # 参数列表
            parameter_list = [
                {'cmapid': self.cmap[i], 'glyph': self.font.getGlyphSet()[self.cmap[i]]} for i in self.cmap
            ]
            executor.map(self.__save, parameter_list)  # 启动任务

    def ocrFontImg(self, jsonpath: str = None):
        """
        进行OCR识别并返回识别结果。

        :param jsonpath: OCR字典结果的保存路径，默认不保存
        :return: 返回一个OCR识别字典结果
        """
        import ddddocr
        import json

        ocr = ddddocr.DdddOcr()
        file_list = os.listdir(self.savepath)
        dis = {}
        reversed_dict = {value: key for key, value in self.cmap.items()}
        ocrfail = {}

        for i in file_list:
            imgname = i.split('.')[0]
            if imgname in reversed_dict:
                path = os.path.join(self.savepath, i)
                with open(path, 'rb') as f:
                    img_bytes = f.read()
                    res = ocr.classification(img_bytes)

                if res == '':
                    dis[imgname] = 'Null'
                    ocrfail[imgname] = 'Null'
                else:
                    dis[imgname] = res
            else:
                continue

        if len(ocrfail) != 0:
            print(f'由于ddddocr识别没有识别到,已为您打印失败结果：{ocrfail}')
            print('如果您有好的解决办法,请联系我QQ:2176189493')

        if jsonpath is not None:
            with open(jsonpath, 'w', encoding='utf-8') as f:
                json.dump(dis, fp=f, ensure_ascii=False)

        return dis

    def __get_proportional_size(self, original_width: int, original_height: int):
        """
        此对象的私有方法，用于计算字体等比例宽高。

        :param original_width: 原始字形宽
        :param original_height: 原始字形高
        :return: 返回计算后的宽度和高度
        """
        max_size = 100
        aspect_ratio = original_width / original_height

        if original_width > original_height:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(max_size * aspect_ratio)

        return (new_width, new_height)


if __name__ == '__main__':
    hui = HuiFontMap(
        fontpath=r"C:\Users\21761\Desktop\dc027189e0ba4cd.woff2",
        savepath=r"C:\Users\21761\Desktop\新建文件夹",
        issaveimg=False
    )
    ocrContent = hui.ocrFontImg()
