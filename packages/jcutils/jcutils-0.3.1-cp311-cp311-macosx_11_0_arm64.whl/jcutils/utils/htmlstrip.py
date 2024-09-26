"""
Created on 2017/2/17
@author: lijc210@163.com
Desc: 功能描述。
"""
import re

from pyquery import PyQuery as pq


class HTMLStrip:
    @staticmethod
    def strip(snippet):
        """
        去html标签
        :param snippet:
        :return:
        """
        doc = pq(snippet)
        return doc.text()

    @staticmethod
    def fenju(text):
        """
        分句
        :param text:
        :return:
        """
        content = HTMLStrip.strip(text)
        # pattern=re.compile(r'\；|\。|\！|\？')
        # pattern1 = re.compile(r'\[|\]|\{|\}|\(|\)|\<|\>|\'|\"|\（|\）|\{|\}|\【|\】|\《|\》|\r|\n|\t|\“|\”|\‘|\’')
        # content = re.sub(pattern1, ' ', content)
        pattern2 = re.compile(r"\；|\。|\！|\？|\?|\.|\,|\;|\:|\!|\，")
        sentenselist = re.split(pattern2, content)
        return sentenselist


if __name__ == "__main__":
    content = """首先，首先，我大中华有靠谱的不忽悠人的良心装修企业吗？<br>这不是一个人的问题，这整个行业都厚颜无耻。这也不是一个行业的问题，在目前体制下，有良心的企业很难活得久。"""
    content_new = HTMLStrip.strip(content)
    print(content_new)
    ls = HTMLStrip.fenju(
        "家里装修，地面材料的种类很多，木地板、瓷砖、地毯等，要怎么进行选购也是个大人值得深思的大问题。我们可以从功能、审美需求、脚感、生活习惯等四个方面来进行选购的啊。1按功能区选:起居室的沙发区最好选择柔软、易清洁更换的材料，比如一块小地毯。这样可以满足大人赤足放松看电视、儿童席地玩耍的需要。厨房的地面易附着水和污物，可选择毛孔小、吸水率低的瓷砖，清理起来比较省力。卫生间地面比较潮湿，一般不宜使用木地板，选择瓷砖也要注意防滑性。2按审美需求选:近年来，木地板产品在颜色上有了不少突破，市面上已经有彩色木地板供应，但相对而言，地毯、瓷砖组成的图案和色彩变化更丰富一些，也更容易体现个性。3按脚感选:木地板富有弹性，并有温暖感，喜欢赤足的业主应该首选木地板。随着制作工艺水平的提高，瓷砖的冰凉脚感得到了改善，布艺纹、皮革纹、木纹质感的瓷砖都已面世，脚感接近木地板，并且清洁起来更容易，加上地热采暖逐渐步入家庭，选瓷砖的人也逐渐增多。4按生活习惯选:如果你工作繁忙，无暇打理家居，应当选择易于清洁的瓷砖。如果有充分的时间，并且喜好打理家居，可以选择木地板和地毯。木地板比较难打理，因为木地板怕水，要保持一定的干燥度。瓷砖比较好打理，做起卫生来非常方便，但是脚感却不好。地毯脚感好，但却容易滋生细菌，要用吸尘器做卫生，比较麻烦。根据自己家的实际情况来选购吧！"
    )
    print(ls)
    print(len(ls))
