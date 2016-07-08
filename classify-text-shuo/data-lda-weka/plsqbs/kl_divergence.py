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





def KL_divergence(a,b):
    """a,b are two topic vectors"""
    dist=0
    for i in range(len(a)):
        dist+=a[i]*np.log(a[i]/b[i])
    return dist



def dist_matrix_KL(dtm):
    """input is a n*m matrix, each row is a vector, return the dist matrix between these row vectors, dim=n*n"""
    dist_matrix=[]
    for i in range(dtm.shape[0]):
        row=[]
        for j in range(dtm.shape[0]):
            dist=KL_divergence(dtm[i],dtm[j])
            row.append(dist)
        dist_matrix.append(row)
    return dist_matrix
            

def symmetric(dist_matrix):
    """make the asytmmetric dist matrix symmetric by taking the min value"""
    for i in range(len(dist_matrix)):
        for j in range(len(dist_matrix)):
            if dist_matrix[i][j]!=dist_matrix[j][i]:
                dist_matrix[i][j]=dist_matrix[j][i]=min(dist_matrix[i][j],dist_matrix[j][i])
    return dist_matrix

#input data file
mallet_output=sys.argv[1]
#'doc-topics-plsqbs4.txt'
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

#compute KL divergence distance matrix
distkl=dist_matrix_KL(dtm)
distkl_sym=symmetric(distkl)
dist_klsm=np.array(distkl_sym)

#MDS
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(dist_klsm)

names=[file.split('/')[-1].split('.')[0] for file in filenames]

print 'plotting KL_divergence distances'
plot_mds(pos,names,'mds_KL.pdf')
