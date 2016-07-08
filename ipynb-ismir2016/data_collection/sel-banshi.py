# -*- coding: utf-8 -*-

import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
#first check if this csv is legit
#this will print out any lines with more than 2 columns
from collections import defaultdict
import csv
import codecs, re


per_label = defaultdict(list)

inputfilename="xk-seg-cln-nop.csv"


with open(inputfilename, 'rU') as inputfile:
    reader = csv.reader(inputfile)
    # skip the header row
    #next(reader, None)  

    for banshi,lyrics in reader:
        bsdec=codecs.decode(banshi,'utf-8')
        lydec=codecs.decode(lyrics,'utf-8')
        per_label[bsdec].append([lydec])



selected= '西皮摇板,西皮慢板,西皮原板,西皮快板,二黄摇板,二黄慢板,二黄原板'
seldec=codecs.decode(selected,'utf-8')
seldec=seldec.split(",")


sel_dic={}
for k,v in per_label.iteritems():
    if k in seldec:
        sel_dic[k]=v        
        
for banshi_name,banshi_text in sel_dic.iteritems():
    for passage in banshi_text:
        print banshi_name+","+passage[0]
