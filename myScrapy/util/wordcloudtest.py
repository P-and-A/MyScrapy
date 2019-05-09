
from importlib import reload
from os import path
import os

from py._xmlgen import unicode
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from scipy.misc import imread
import jieba
import jieba.analyse
import matplotlib as mpl
import sys

from myScrapy.util.common import my_select_row

# reload(sys)
#
# # sys.setdefaultencoding('utf-8')
# d=path.dirname(__file__)
# # text = open(path.join(d,"wordcloudData.txt")).read()
# # text_from_file_with_apath =open(path.join(d,"wordcloudData.txt")).read().encode(encoding='UTF-8')
# content = open("wordcloudData.txt","rb").read()
# # tags extraction based on TF-IDF algorithm
# tags = jieba.analyse.extract_tags(content, topK=100, withWeight=False)
# text =" ".join(tags)
# # text = unicode(text)
#
# # str(my_select_row()).decode("utf-8")  #
#
# # wordlist_after_jieba = jieba.cut(text_from_file_with_apath, cut_all = True)
#
# # wl_space_split = " ".join(wordlist_after_jieba)
#
# # font=os.path.join(os.path.dirname(__file__), "DroidSansFallbackFull.ttf")
#
# my_wordcloud = WordCloud(max_font_size=40).generate(text)
#
# assert isinstance(my_wordcloud, object)
#
# plt.imshow(my_wordcloud)
#
# plt.axis("off")
#
# plt.show()








mpl.rcParams['font.sans-serif'] = ['FangSong']
    #mpl.rcParams['axes.unicode_minus'] = False

content = open("wordcloudData.txt","rb").read()

    # tags extraction based on TF-IDF algorithm
tags = jieba.analyse.extract_tags(content, topK=200, withWeight=False)
text =" ".join(tags)
# text = unicode(text)
    # read the mask
texts = {}
my_word_list = []
# for text in tags:
#         texts[text[0]]=text[1]*100
#         my_word_list.append(text[0])
#         print(texts)
d = path.dirname(__file__)
trump_coloring = imread(path.join(d, "basketball2.png"))

wc = WordCloud(font_path='simsun.ttc',
        background_color="white", max_words=100, #mask=trump_coloring,
        collocations=False)#,normalize_plurals=True)
def add_word(list):
    for items in list:
        jieba.add_word(items)
add_word(my_word_list)
    # generate word cloud
# wc.fit_words(texts)

wc.generate(text)
# wc.generate_from_frequencies(texts)
    # generate color from image
image_colors = ImageColorGenerator(trump_coloring)

plt.imshow(wc)
plt.axis("off")
plt.show()


















# d=path.dirname(__file__)
# text = open(path.join(d,"wordcloudData.txt")).read()
# alice_coloring = imread(path.join(d,"basketball.png"))
# wc = WordCloud(background_color="white", #背景颜色max_words=2000,# 词云显示的最大词数
#                 mask=alice_coloring,#设置背景图片
#                 stopwords=STOPWORDS.add("said"),
#                 max_font_size=40, #字体最大值
#                 random_state=42)
# # 生成词云, 可以用generate输入全部文本(中文不好分词),也可以我们计算好词频后使用generate_from_frequencies函数
# wc.generate(text)
# # wc.generate_from_frequencies(txt_freq)
# # txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]
# # 从背景图片生成颜色值
# image_colors = ImageColorGenerator(alice_coloring)
#
# # 以下代码显示图片
# plt.imshow(wc)
# plt.axis("off")
# # 绘制词云
# plt.figure()
# # recolor wordcloud and show
# # we could also give color_func=image_colors directly in the constructor
# plt.imshow(wc.recolor(color_func=image_colors))
# plt.axis("off")
# # 绘制背景图片为颜色的图片
# plt.figure()
# plt.imshow(alice_coloring, cmap=plt.cm.gray)
# plt.axis("off")
# plt.show()
# # 保存图片
# wc.to_file(path.join(d, "名称.png"))