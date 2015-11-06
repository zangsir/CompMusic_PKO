from collections import defaultdict
import csv

per_label = defaultdict(list)

inputfilename="/Users/zangsir/Desktop/xikao-scrape/xk-seg-cln-nop.csv"

with open(inputfilename, 'rU') as inputfile:
    reader = csv.reader(inputfile)
    # skip the header row
    #next(reader, None)  

    for banshi,text in reader:
        per_label[banshi].append([text])