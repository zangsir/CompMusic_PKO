#use this to read in a mallet topic model file and output a very similar csv file used for machine learning classification
import sys

mallet_output=sys.argv[1]
f=open(mallet_output,'r')
doctopic=f.read()
doctopic_list=doctopic.split('\n')
f.close()
filenames=[]
data=[]
data_str=[]
for line in doctopic_list:
    if line!='':
        line=line.split('\t')
        filenames.append(line[1])
        line_float=[float(i) for i in line[2:]]
        data_str.append(line[2:])
        data.append(line_float) 


names=[file.split('/')[-1].split('.')[0].split("_")[0] for file in filenames]
header=range(20)
header.append('class')
header=[str(i) for i in header]
outputname=mallet_output.split('.')[0]+"-train.csv"

f=open(outputname,'w')
f.write(','.join(header)+'\n')
for i in range(len(data)):
    numbers=",".join(data_str[i])
    label=names[i]
    line=numbers + "," + label
    f.write(line+"\n")
f.close()