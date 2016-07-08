#this module has functions that preprocess the text for corpus of text mining
#complete trace of dev is in gensim-nltk.ipynb

def cleanBanshiName(text):
    '''this method takes the segmented Chinese text and put banshi names as one token w/o any whitespaces'''
    a=re.findall(ur'(\uff08.*?\uff09)',text)
    seta=set(a)
    for pat in seta:
        rep=pat.replace(" ","")
        text=text.replace(pat,rep)
    return text