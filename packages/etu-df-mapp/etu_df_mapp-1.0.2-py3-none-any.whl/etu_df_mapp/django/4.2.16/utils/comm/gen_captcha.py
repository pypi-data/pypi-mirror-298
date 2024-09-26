# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 19:02
# @Author  : Jieay
# @File    : gen_captcha.py
import os
import random
import math
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class VieCode:
    __font_size = 20  # 字体大小
    __width = 120  # 画布宽度
    __height = 45  # 画布高度
    __length = 4  # 验证码长度
    __draw = None  # 画布
    __img = None  # 图片资源
    __code = None  # 验证码字符
    __str = None  # 自定义验证码字符集
    __in_curve = True  # 是否画干扰线
    __in_noise = True  # 是否画干扰点
    __type = 2  # 验证码类型 1、纯字母  2、数字字母混合
    # __font_path = 'app/utils/fonts/1.ttf'  # 字体
    __font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', '1.ttf')  # 字体

    def get_code_image(self, size=80, length=4):
        """
        获取验证码图片
        :param size:
        :param length:
        :return:
        """
        self.__length = length
        self.__font_size = size
        self.__width = self.__font_size * self.__length
        self.__height = int(self.__font_size * 1.5)

        # 生成验证码图片
        self.__create_code()
        self.__create_image()
        self.__create_noise()
        self.__print_string()
        self.__create_filter()

        return self.__img, self.__code

    def __create_filter(self):
        """
        模糊处理
        """
        self.__img = self.__img.filter(ImageFilter.BLUR)
        _filter = ImageFilter.ModeFilter(8)
        self.__img = self.__img.filter(_filter)

    def __create_code(self):
        """
        创建验证码字符
        """
        # 是否自定义字符集合
        if not self.__str:
            # 源文本
            number = "3456789"
            src_letter = "qwertyuipasdfghjkzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            src_upper = src_letter.upper()
            if self.__type == 1:
                self.__str = number
            else:
                self.__str = src_letter + src_upper + number

        # 构造验证码
        self.__code = random.sample(self.__str, self.__length)

    def __create_image(self):
        """
        创建画布
        """
        bg_color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        self.__img = Image.new('RGB', (self.__width, self.__height), bg_color)
        self.__draw = ImageDraw.Draw(self.__img)

    def __create_noise(self):
        """
        画干扰点
        """
        if not self.__in_noise:
            return
        font = ImageFont.truetype(self.__font_path, int(self.__font_size / 1.5))
        for i in range(5):
            # 杂点颜色
            noise_color = (random.randint(150, 200), random.randint(150, 200), random.randint(150, 200))
            put_str = random.sample(self.__str, 2)
            for j in range(2):
                # 绘杂点
                size = (random.randint(-10, self.__width), random.randint(-10, self.__height))
                self.__draw.text(size, put_str[j], font=font, fill=noise_color)
        pass

    def __create_curve(self):
        """
        画干扰线
        """
        if not self.__in_curve:
            return
        x = y = 0

        # 计算曲线系数
        a = random.uniform(1, self.__height / 2)
        b = random.uniform(-self.__width / 4, self.__height / 4)
        f = random.uniform(-self.__height / 4, self.__height / 4)
        t = random.uniform(self.__height, self.__width * 2)
        xend = random.randint(int(self.__width / 2), self.__width * 2)
        w = (2 * math.pi) / t

        # 画曲线
        color = (random.randint(30, 150), random.randint(30, 150), random.randint(30, 150))
        for x in range(xend):
            if w != 0:
                for k in range(int(self.__height / 10)):
                    y = a * math.sin(w * x + f) + b + self.__height / 2
                    i = int(self.__font_size / 5)
                    while i > 0:
                        px = x + i
                        py = y + i + k
                        self.__draw.point((px, py), color)
                        i -= i

    def __print_string(self):
        """
        打印验证码字符串
        """
        font = ImageFont.truetype(self.__font_path, self.__font_size)
        x = 0
        # 打印字符到画板
        for i in range(self.__length):
            # 设置字体随机颜色
            color = (random.randint(30, 150), random.randint(30, 150), random.randint(30, 150))
            # 计算座标
            x = random.uniform(self.__font_size * i * 0.95, self.__font_size * i * 1.1)
            y = self.__font_size * random.uniform(0.3, 0.5)
            # 打印字符
            self.__draw.text((x, y), self.__code[i], font=font, fill=color)


# 生成验证码
def get_captcha():
    image, code = VieCode().get_code_image()
    code = ''.join(code).lower()
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    return out, code
