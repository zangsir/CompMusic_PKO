# -*- coding: utf-8 -*-


import matplotlib
import codecs
import re
import os
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
import numpy as np  
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.manifold import MDS


corpus_path = 'sqbs7_all_docs'



#what is the top words? in each document
def get_word_dist(dtm,i):
    """input is the index of the document, such as i=1 is the first document"""
    fdist=[]
    for word in vocab_list:
        #print word
        freq=dtm[i, vocab == word]
        fdist.append((word,freq[0]))

    rank=sorted(fdist, key=lambda x: x[1])[::-1]
    return rank


def print_top_words():
	for i in range(7):
	    print filenames[i]
	    rank=get_word_dist(i)
	    for words in rank[:20]:
	        print words[0],words[1]




def get_word_dist_all(dtm):
    """input is the index of the document, such as i=1 is the first document"""
    all_dtm=np.sum(dtm,axis=0)
    fdist=[]
    for word in vocab_list:
        #print word
        freq=all_dtm[vocab == word]
        fdist.append((word,freq[0]))

    rank=sorted(fdist, key=lambda x: x[1])[::-1]
    return rank


def print_top_words_all():
	rank=get_word_dist_all()
	for words in rank[:50]:
	    print words[0],words[1],


#we need to see about the stopword list. 
stop_ori='我 一 不 你 把 了 是 来 在 他 的 有 将 见 人 与 得 要 到 听 那 又 为 上 这 三 只 好 二 说 无 家 也'
frwords=codecs.decode(stop_ori,'utf-8')
stoplist=set(frwords.split())
stoplist_ori=set(stop_ori.split())#not useful now


filenames=[os.path.join(corpus_path, fn) for fn in sorted(os.listdir(corpus_path))]
if 'sqbs7_all_docs/.DS_Store' in filenames:
    filenames.remove('sqbs7_all_docs/.DS_Store')

print filenames

pat=re.compile(r'(?u)\b\w+\b',re.UNICODE )
vectorizer = CountVectorizer(input='filename',stop_words=stoplist,token_pattern=pat) 
dtm = vectorizer.fit_transform(filenames)  # a sparse matrix 
vocab_list = vectorizer.get_feature_names()
type(dtm)                                         
dtm = dtm.toarray()  # convert to a regular array 
#note that vocab_list is a python list, vocab is a numpy array
vocab = np.array(vocab_list)



#cosine similarity
dist = 1 - cosine_similarity(dtm)
np.round(dist, 2)
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(dist)  # shape (n_components, n_samples)

xs, ys = pos[:, 0], pos[:, 1]
names = [os.path.basename(fn).replace('.txt', '') for fn in filenames]


import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from matplotlib import font_manager

fontpath = '/Library/Fonts/华文细黑.ttf' 
prop = font_manager.FontProperties(fname=fontpath)
matplotlib.rcParams['font.family'] = prop.get_name()

for x, y, name in zip(xs, ys, names):
    
    if '原板' in name:
        color = 'orange'
        print 'uyes'
    elif '慢板' in name:
        color = 'skyblue'
    elif '摇板' in name:
        color = 'red'
    elif '快板' in name:
        color = 'yellow'
        
    plt.scatter(x, y, c=color)
    #nameu=codecs.decode(name,'utf-8')
    print name
    plt.text(x, y, name) 


plt.savefig('figure1.pdf', format='pdf')



mds = MDS(n_components=3, dissimilarity="precomputed", random_state=1)

pos = mds.fit_transform(dist)
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2])

for x, y, z, s in zip(pos[:, 0], pos[:, 1], pos[:, 2], names):
    ax.text(x, y, z, s)
 

plt.savefig('figure2.pdf', format='pdf')


