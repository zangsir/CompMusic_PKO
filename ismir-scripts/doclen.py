from os import listdir
import codecs
import matplotlib.pyplot as plt

mypath="/Users/zangsir/Desktop/data_collection_ismir16/play_sq_bs_docs/naming_sqbs_pl/"

onlyfiles = [ f for f in listdir(mypath) if f.endswith(".txt") ]
doclen=[]

for file in onlyfiles:
    f=open(mypath+file,'r')
    doc=f.read()
    f.close()
    doclen.append(len(codecs.decode(doc,'utf-8')))


plt.xlabel('document length by unicode character')
plt.ylabel('count')
plt.hist(doclen,bins=200)#range=[6.5, 12.5]
plt.savefig('doclens.pdf', format='pdf')