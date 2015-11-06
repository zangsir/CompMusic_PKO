#the extract banshi task is to extract all banshi passages from the complete scripts scraped from xikao.com.
#this task was completed using a ipython notebook  
#this script extract some of the essential functions from that ipynb, to be a stand alone script to reference or use

#f=open('京剧剧本-《女起解》.txt','r')
#text=f.read()

#currently use absolute path, so doesn't matter where this is located as long as those path are valid
import re
import codecs
from os import listdir
from os.path import isfile, join
mypath='/Users/zangsir/Desktop/xikao-text/'
outputPath='/Users/zangsir/Desktop/xikao_bs/'
onlyfiles = [ f for f in listdir(mypath) if f.endswith(".txt") ]



#compile BAN) pattern , sb holds all symbols we can look for
pat_ban=re.compile(ur'\u677f\uff09')
#compile symbols pattern
pat_sb_all=re.compile(ur'[.\u201c\u201d\u2026\u250a\u3000\u3001\u3002\u300a\u300b\u3010\u3011\uff01\uff08\uff09\uff0c\uff1a\uff1b\uff1f]')
pat_sb=re.compile(ur'[.,\u3001\u3002\uff01\uff0c\uff1a\uff1b\uff1f]')



############################## ############################## Function Defs
def findRightBound(textseg,startpos_abs,ws_positions):
    '''recursively find the right boundary of a banshi passage'''
    a=re.search(pat_sb,textseg)
    first_symbol=a.start()
    first_symbol_abs=first_symbol+startpos_abs + 1
    if first_symbol_abs in ws_positions:
        startpos_sub=first_symbol+14
        startpos_abs=startpos_abs+first_symbol+14
        textsegnew=textseg[startpos_sub:]
        return findRightBound(textsegnew,startpos_abs,ws_positions)
    return first_symbol_abs
        

def findBanshiNameStart(text,startban):
    """ given the starting position of BAN), find the name of this ban by finding the matching parenthesis preceding this """
    #u'\uff08' is ( for chinese characters
    match_pos=startban-2
    while text[match_pos]!=u'\uff08':
        match_pos=match_pos-1
    return match_pos

def extractPassage(test):
    '''this is main function for extracting a passage of banshi, given only a piece of text. first finds the left boundary by RE, and then find right boundary by calling findRightBound()'''
    #compile 13ws pattern, get all starting positions in a list
    #NOTICE this has to be defined according to the current dataset, such as test, or a doc, text_dec
    ws_positions=[]
    pat_ws=re.compile(ur'\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000')
    for m in pat_ws.finditer(test):
        ws_positions.append(m.start())
    #print 'wspos', ws_positions
    all_start=[]
    all_end=[]
    for m in pat_ban.finditer(test):
        #print m.start(),m.group()
        #for each position of m.start(), search for the first symbol after this position
        start_banshi=m.start()
        start_banshi_name=findBanshiNameStart(test,start_banshi)
        all_start.append(start_banshi_name)
        #print "start",start_banshi
        right_bound=findRightBound(test[start_banshi:],start_banshi,ws_positions)
        #print "RIGHT",right_bound
        all_end.append(right_bound)
    #print "start:",all_start
    #print "end:",all_end
    return all_start,all_end











############################## ############################## Main Usage
#this will write extracted banshi passages for each play to txt files in specified directory

for fileName in onlyfiles:
    #process one document
    f=open(mypath+fileName,'r')
    text=f.read()
    outputName=outputPath+"bs_" + fileName
    with open(outputName,"w") as f:
        writer=csv.writer(f)
    #decode
    text_dec=codecs.decode(text,'utf-8')
    #this returns two lists, with starting_index list and a ending_index list
    starts,ends=extractPassage(text_dec)
    if len(starts)==len(ends):
        try:
            for i in range(len(starts)):
                passage=text_dec[starts[i]:ends[i]]
                #strip the passage's whitespace \u3000
                passage_nw=re.sub(ur'\u3000',"",passage)
                #write to file, which in the end will contain only all banshi passages in the current doc
                with open(outputName, "a") as myfile:
                    myfile.write(passage_nw.encode('utf-8'))
                    myfile.write('\n')
        except:
            print "starts and ends lists have different length, error"


