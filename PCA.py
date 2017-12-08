from __future__ import division
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from mpl_toolkits.mplot3d import Axes3D

#self define pca
def PCA_Self_define(baby):
    ee=pd.DataFrame(preprocessing.scale(baby),columns=baby.columns,index=baby.index)
    Variance_s,PCs_s=np.linalg.eig(np.cov(ee.T))
    R_s=dict()
    R_s['loadings'] = pd.DataFrame(PCs_s, columns=['PC' + str(i) for i in range(1, baby.shape[1] + 1)],
                                   index=[baby.columns])
    R_s['variance'] = Variance_s
    Newdata=np.dot(ee,PCs_s.T)
    R_s['score'] = pd.DataFrame(Newdata,columns=['PC' + str(i) for i in range(1, baby.shape[1] + 1)])
    return R_s



y_offsets={'Retail':-0.3,'Wheelbase':-0.3,'CityMPG':0.3,'Book Value':-0.8,
           '52 week high':-0.6,'EBITDA':0.6,'Earnings/Share':0.3,'52 week low':-0.3}  # set for right words do not overlap
def biplot(score,loadings,PC1='PC1',PC2='PC2'):
    fig3 = plt.figure()
    plt.scatter(score[PC1],score[PC2],alpha=0.5)
    for i,n in enumerate(loadings.columns):
        plt.arrow(0, 0, loadings.loc[PC1,n]*7, loadings.loc[PC2,n]*7,color='r',alpha=0.5,head_width=0.25)
        if n in y_offsets:
            plt.text(loadings.loc[PC1,n] * 7, loadings.loc[PC2,n] * 7+y_offsets[n], n)
        else:
            plt.text(loadings.loc[PC1,n]*7, loadings.loc[PC2,n]*7,n)
    plt.title('Bi-plot for PCA score')
    plt.xlabel('{}'.format(PC1))
    plt.ylabel('{}'.format(PC2))
biplot(rv['score'],rv['loadings'])
biplot(rb['score'],rb['loadings'])




y_offsets_3={'Retail':0.5,'52 week low':-0.5,'Price':0.3}  # set for right words do not overlap
def tri_plot(score,loadings,PC1='PC1',PC2='PC2',PC3='PC3'):
    fig4=plt.figure()
    ax = Axes3D(fig4)
    ax.scatter(score[PC1],score[PC2],score[PC3],alpha=0.5,c='pink')
    for i, n in enumerate(loadings.columns):
        ax.quiver(loadings.loc[PC1, n]*7, loadings.loc[PC2, n]*7,loadings.loc[PC3, n]*7,loadings.loc[PC1, n]*7, loadings.loc[PC2, n]*7,loadings.loc[PC3, n]*7 ,color='blueviolet', alpha=0.5,arrow_length_ratio=0.15,length=5)
        if loadings.columns[i] in y_offsets_3:
            ax.text(loadings.loc[PC1, n] * 7+y_offsets_3[n], loadings.loc[PC2, n] * 7+y_offsets_3[n], loadings.loc[PC3, n] * 7+y_offsets_3[n], n)
        else:
            ax.text(loadings.loc[PC1, n]*7, loadings.loc[PC2, n]*7,loadings.loc[PC3, n]*7,n)
    ax.set_title('Tri-plot for PCA score')
    ax.set_xlabel('{}'.format(PC1))
    ax.set_ylabel('{}'.format(PC2))
    ax.set_zlabel('{}'.format(PC3))

tri_plot(rv['score'],rv['loadings'])
tri_plot(rb['score'],rb['loadings'])



