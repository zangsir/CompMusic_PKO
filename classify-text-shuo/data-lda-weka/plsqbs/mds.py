# -*- coding: utf-8 -*-



import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
import os  # for os.path.basename
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def plot_mds(pos,names,outputname):
    xs, ys = pos[:, 0], pos[:, 1]
    for x, y, name in zip(xs, ys, names):
        if '西皮原板' in name:
            color = 'orange'
            lab='xpyuanb'
        elif '二黄原板' in name:
            color = 'yellow'  
            lab='ehyuanb'  
        elif '西皮慢板' in name:
            color = 'skyblue'
            lab='xpmb'
        elif '二黄慢板' in name:
            color = 'blue'
            lab='ehmb'
        elif '西皮摇板' in name:
            color = 'red'
            lab='xpyaob'
        elif '二黄摇板' in name:
            color = 'deeppink'
            lab='ehyaob'
        elif '快板' in name:
            color = 'yellow'
            lab='xpkb'
        plt.xlabel('MDS dimension 1')
        plt.ylabel('MDS dimension 2')
        plt.scatter(x, y, c=color,label=lab)
        
        #plt.text(x, y, name) 
        plt.savefig(outputname, format='pdf')



# supply your mallet topic model file to be read on cmd line, such as 'doc-topics-plsqbs.txt'
mallet_output=sys.argv[1]
f=open(mallet_output,'r')
doctopic=f.read()
doctopic_list=doctopic.split('\n')
f.close()
filenames=[]
data=[]
for line in doctopic_list:
    if line!='':
        line=line.split('\t')
        filenames.append(line[1])
        line_float=[float(i) for i in line[2:]]
        data.append(line_float) 

dtm=np.array(data)
diste = euclidean_distances(dtm)
#distc = 1 - cosine_similarity(dtm)

mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)

pose = mds.fit_transform(diste)  # shape (n_components, n_samples)
#posc = mds.fit_transform(distc)

#euclidean distance


names=[file.split('/')[-1].split('.')[0] for file in filenames]

print 'plotting euclidean distance'
plot_mds(pose,names,'mds_euclid.pdf')
#plot_mds(posc,names,'mds_cosine.pdf')