⭐️ **简介**

本库是一个基于 python 的工具集，用于生成字体文件字典映射。

✨️ **理念**

简单，可靠，省心。

📕 **背景**

进行数据采集的时候，常常会遇到字体反爬，常用的解决办法是通过获取字体字形映射关系替换文本解决，但生成或者说是获取字体映射关系的方法不是很常见，所以写了这个库，方便生成获取

🌠 **用法**

这里介绍工具用法。
## 安装
```python
pip install FontMap
```
## 使用
#### 导包
```python
import FontMap
```
#### 实例化

```python
fontmap = FontMap.HuiFontMap(fontpath='字体文件路径',savepath='生成的字形图片保存路径',issaveimg='是否保存图片')
```
执行会根据传入的路径生成并保存字形文件
##### 方法
目前只使用了ddddocr识别，测试大部分是没有问题基本，一小部分的化可能会存在识别精度的问题
```python
fontmap.ocrFontImg(jsonpath='识别结果的保存路径')
```
此方法返回执行的结果，类型为字典，默认是不保存识别结果的

👨‍💻 **更新**

优化了图片生成速度和ddddocr识别精度

☕ **最后**
如果本项目有问题，欢迎反馈，QQ：2176189493