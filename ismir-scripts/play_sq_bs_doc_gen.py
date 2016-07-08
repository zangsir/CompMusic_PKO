# -*- coding: utf-8 -*-

#generate play_shengqiang_banshi_docs,  distinguish shengqiang


#first check if this csv is legit
#this will print out any lines with more than 2 columns
from collections import defaultdict
import csv,sys
import codecs, re


per_label = defaultdict(dict)

#inputfilename="xk-seg-cln-nop-fix.csv"
inputfilename = sys.argv[1]

with open(inputfilename, 'rU') as inputfile:
    reader = csv.reader(inputfile)
    for row in reader:
        if len(row)!=3:
            print 'len=',len(row)
            for i in row:print i
            print 'found mistakes...........'



with open(inputfilename, 'rU') as inputfile:
    reader = csv.reader(inputfile)
    # skip the header row
    #next(reader, None)  

    for play,banshi,lyrics in reader:
        pldec=codecs.decode(play,'utf-8')
        bsdec=codecs.decode(banshi,'utf-8')
        lydec=codecs.decode(lyrics,'utf-8')
        if not bsdec in per_label[pldec]:#the banshi doesn't exist yet in this play
            per_label[pldec][bsdec]=[lydec]
        else:
            per_label[pldec][bsdec].append(lydec)


selected='西皮摇板,西皮慢板,西皮原板,西皮快板,二黄摇板,二黄慢板,二黄原板'
seldec=codecs.decode(selected,'utf-8')
seldec=seldec.split(",")

for k in per_label:
    #print k
    for key in per_label[k]:
        
        key_clean=key.replace(u'\uff09','').replace(u'\uff08','')
        if key_clean in seldec:
            outfilename = key_clean + "_" + k + '.txt'
            f=open(outfilename,'a')
            for line in per_label[k][key]:
                f.write(line.encode('utf-8') + '\n')
            f.close()