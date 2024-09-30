from pylinuxauto.image import Image

from pylinuxauto.config import config

config.IMAGE_SERVER_IP = "10.8.11.69"

config.IMAGE_BASE_URL = "http://10.8.12.24/image_res/deepin-music/"

def test_image_01():
    # 简写形式，@ 符号代表 IMAGE_BASE_URL
    a = Image().find_element_by_image("@1.png").result
    print(a)

def test_image_02():
    # 全URL
    a = Image().find_element_by_image("http://10.8.12.24/image_res/deepin-music/1.png").result
    print(a)

def test_image_03():
    # 本机绝对路径
    a = Image().find_element_by_image("~/Desktop/1.png").result
    print(a)
