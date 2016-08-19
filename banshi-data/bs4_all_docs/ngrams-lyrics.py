from collections import defaultdict
from os import listdir
import sys,codecs
#text is a list, the product of preprocess
def ngrams(n,text):
    dic=defaultdict(int)
    for i in range(len(text)-n):
        tokens=text[i]
        for j in range(1,n):
            tokens+=" " + text[i+j]
        dic[tokens]+=1
    dit=sorted(dic.items(), key=lambda x: x[1],reverse=True)
    return dit
    

def print_result(result):
    output=[]
    
    for k,v in result:
        if ',' not in k and '.' not in k:
            output.append([k,str(v)])
    return output



def preprocess(file):
    f=open(file,'r')
    t=f.read()
    tdec=codecs.decode(t,'utf-8')
    tres=tdec.replace('   ',',')
    tresn=tres.replace('\n','.')
    tresns=tresn.replace(' ','')
    newt=[]
    for c in tresns:
        newt.append(c)
    return newt

def write_to_file(out,inputfile,outname):
    """out is the data to be written to the file"""
    y=open(outname,'a')
    y.write('\n\n'+ "#" + inputfile + '\n')
    for line in out[:100]:
        ttw=' '.join(line)
        y.write(ttw.encode('utf-8'))
        y.write('\n')
    y.close()



n=int(sys.argv[1])
print 'n=',n
mypath='./data'
onlyfiles = [ f for f in listdir(mypath) if f.endswith(".txt") ]
outname=str(n)+'-pattern-lyrics.txt'#write results to this file

for file in onlyfiles:
    filepath=mypath+'/'+file
    print filepath
    res=preprocess(filepath)
    result=ngrams(n,res)
    out=print_result(result)
    write_to_file(out,file,outname)








