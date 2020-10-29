from typing import Dict

import pandas as pd
import collections
import spacy
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nlp = spacy.load('en_core_web_sm')  # 加载spacy

p_o = pd.read_excel("library.xlsx", sheet_name="Sheet1")

print(p_o)
my_dict = p_o.fillna("").to_dict("index")
# my_dict = {}

my_lst = []

word_lst = []
for i, v in my_dict.items():
    # print(i)
    v["authors"] = ", ".join(v["authors"].replace(",", "").split('\n'))
    v["tags"] = [i for i in v["tags"].split("\n") if i != ""]
    # v["links"] = None
    doc = nlp(v["title"])
    for token in doc:
        if token.pos_ == "NOUN":
            word_lst.append(token.lemma_)

    my_lst.append(v)

# print([i for i in collections.Counter(word_lst).items()])
t_counter = dict(collections.Counter(word_lst))
# result = " ".join(word_lst)
#print(result)
# 3.生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
# 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
wc = WordCloud(
        # 设置字体，不指定就会出现乱码
        # 设置背景色
        background_color='white',
        # 设置背景宽
        width=800,
        # 设置背景高
        height=600,
        # 最大字体
        max_font_size=300,
        # 最小字体
        min_font_size=15,
        mode='RGBA'
        #colormap='pink'
        )
# 产生词云
wc.generate_from_frequencies(t_counter)
# 保存图片
wc.to_file(r"wordcloud.png") # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰

import json

with open("papers_lst.json", "w") as f:
    json.dump(my_lst, f)

with open("word_lst.json", "w") as f:
    json.dump(t_counter, f)
