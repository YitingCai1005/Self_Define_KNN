from __future__ import division
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import scipy.spatial
import math
from collections import Counter
from functools import partial

CD=pd.read_csv('Q4(1)/Q4/credit_risk_data_balanced.csv')
CD=CD[CD['Num Employees']<=10]
test_percentage=0.2
train_data,test_data,train_label,test_label=train_test_split(CD.drop('Delinquency',axis=1),CD['Delinquency'],test_size=test_percentage,random_state=42)

###########Basic distance methods##################

Manhattan=lambda row,test:abs(row-test).sum()
Euclidean=lambda row,test:math.sqrt(((row-test)**2).sum())
Correlation=lambda row,test:scipy.spatial.distance.correlation(row,test)

######################################################
def basic(testing,training,train_label,k=3,algorithm=Euclidean,weights='uniform'):
    predicted_label=[]

    if weights.lower()=='uniform':
        for index, row in testing.iterrows():
            k_chosen=training.apply(algorithm,args=(row,),axis=1).sort_values()[:k].rename('distance')
            k_index=k_chosen.index
            data = Counter(train_label.loc[k_index])  # calculate count
            if np.sum([i==np.max(data.values()) for i in data.values()])==1: #not tie vote
                predicted_label.append( data.most_common()[0][0])
            else:
                predicted_label.append( train_label.loc[k_index[0]])  # nearest label

    elif weights.lower()=='distance':
        for index, row in testing.iterrows():
            k_chosen = training.apply(algorithm, args=(row,), axis=1).sort_values()[:k].rename('distance')
            label=train_label[k_chosen.index]
            Process_result = pd.concat((1 / k_chosen,label ), axis=1).groupby('Delinquency').sum()
            predicted_label.append(Process_result.idxmax()['distance'])

    return predicted_label


class knn_selfdefine:
    def __init__(self,k=3,algorithm=Euclidean,weights='uniform'):
        'paramters for knn'
        self.k=k
        self.algorithm=algorithm
        self.weights=weights
    def fit(self,training,train_label):
        'training data and train label for knn model'
        self.knn=partial(basic,training=training,train_label=train_label,k=self.k,algorithm=self.algorithm,weights=self.weights)
    def predict(self,test_data):
        'prediction function'
        self.prediction=self.knn(test_data)
        return self.prediction


KNC=knn_selfdefine(k=5,algorithm=Manhattan)
KNC.fit(train_data,train_label)
KNC.predict(test_data[:3])
