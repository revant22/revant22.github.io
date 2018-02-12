#!/usr/bin/env python
"""
Minimal Example
===============

Generating a square wordcloud from the US constitution using default arguments.
"""

from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import numpy as np

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'data/text_dump.txt')).read()

out_filepath = path.join(d, 'images/mask.png')
# Generate a word cloud image
wordcloud = WordCloud().generate(text)

rs_coloring = np.array(Image.open(path.join(d, "images/mask.png")))

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt

stopwords = set(STOPWORDS)
stopwords.add("said")

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(background_color="white", max_words=400, mask=rs_coloring, width=1200, height=1600,random_state=42)
wordcloud.generate(text)
# plt.figure()
# plt.imshow(wordcloud, interpolation="bilinear")
# plt.axis("off")
# plt.show()

image_colors = ImageColorGenerator(rs_coloring)
# The pil way (if you don't have matplotlib)
# wordcloud.to_image().save(out_filepath)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.figure()
# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor
plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(rs_coloring, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
plt.show()

wordcloud.to_file(path.join(d, "../webapp/wordcloud.png"))

