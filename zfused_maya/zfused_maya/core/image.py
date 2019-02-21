# coding:utf-8
#--author-- lanhua.zhou
from __future__ import print_function

import colorsys
import PIL.Image as Image
 
def get_dominant_color(image):
    image = Image.open(image)
    image = image.convert('RGB')
    max_score = 0.0001
    dominant_color = None
    for count,(r,g,b) in image.getcolors(image.size[0]*image.size[1]):
        # 转为HSV标准
        saturation = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)[1]
        y = min(abs(r*2104+g*4130+b*802+4096+131072)>>13,235)
        y = (y-16.0)/(235-16)
        # 忽略高亮色
        if y > 0.9:
            continue
        score = (saturation+0.1)*count
        if score > max_score:
            max_score = score
            dominant_color = (r,g,b)
    return dominant_color
 
if __name__ == '__main__':
    image = r'\\192.168.101.88\works\FanMan\Projects_backup\sintel\asset\char\pan\model\maya2016\texture\dimian_02.jpg'
    print(get_dominant_color(image))