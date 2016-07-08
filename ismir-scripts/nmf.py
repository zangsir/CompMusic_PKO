# -*- coding: utf-8 -*-


import sys, os
import numpy as np
reload(sys)
sys.setdefaultencoding("utf-8")
from sklearn import decomposition

import codecs,re
from sklearn.feature_extraction.text import CountVectorizer


#corpus_path = 'sqbs7_all_docs'
corpus_path = sys.argv[1]
outfile=sys.argv[2]

stop_ori='的 一 不 在 人 有 是 为 以 于 上 他 而 后 之 来 及 了 因 下 可 到 由 这 与 也 此 但 并 个 其 已 无 小 我 们 起 最 再 今 去 好 只 又 或 很 亦 某 把 那 你 乃 它 吧 被 比 别 趁 当 从 到 得 打 凡 儿 尔 该 各 给 跟 和 何 还 即 几 既 看 据 距 靠 啦 了 另 么 每 们 嘛 拿 哪 那 您 凭 且 却 让 仍 啥 如 若 使 谁 虽 随 同 所 她 哇 嗡 往 哪 些 向 沿 哟 用 于 咱 则 怎 曾 至 致 着 诸 自'
frwords=codecs.decode(stop_ori,'utf-8')
stoplist=set(frwords.split())
stoplist_ori=set(stop_ori.split())#not useful now



filenames=[os.path.join(corpus_path, fn) for fn in sorted(os.listdir(corpus_path))]
if 'naming_sqbs_pl/.DS_Store' in filenames:
    filenames.remove('sqbs7_all_docs/.DS_Store')



pat=re.compile(r'(?u)\b\w+\b',re.UNICODE )
vectorizer = CountVectorizer(input='filename',stop_words=stoplist,token_pattern=pat) 
dtm = vectorizer.fit_transform(filenames)  # a sparse matrix 
vocab_list = vectorizer.get_feature_names()
type(dtm)                                         
dtm = dtm.toarray()  # convert to a regular array 
#note that vocab_list is a python list, vocab is a numpy array
vocab = np.array(vocab_list)


num_topics = 20
num_top_words = 20
clf = decomposition.NMF(n_components=num_topics, random_state=1)
doctopic = clf.fit_transform(dtm)
np.nan_to_num(doctopic)
np.savetxt(outfile,doctopic)

#distance and plotting: 

# choose a distance measure

# it is possible to have NaN in the doctopic, in which case we'll need to fix it. 



















