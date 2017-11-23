# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:59:35 2017

@author: admin
"""
import numpy as np
import pandas as pd
def PCA(dataMat):
    meanVals = np.mean(dataMat, axis=0)
    meanRemoved = dataMat-meanVals
    ##相关系数矩阵
    covMat = np.cov(meanRemoved, rowvar=0)
    ##特征分解
    eigVals, eigVets = np.linalg.eig(np.mat(covMat))
    pricWeig = eigVals/ np.sum(eigVals)
    aa = np.mat(eigVets.T)*np.mat(np.array(pricWeig)).T
    pcaWeight = (aa-np.min(aa))/(np.max(aa)-np.min(aa))
    pricScore = np.dot(dataMat, pcaWeight)
    pricScore1=(pricScore)/pricScore[0]
    return pricScore1

input_table_path = 'pca-data.xlsx'
#input_table_path:为excel的存储路径和名称
#输入数据需为数值型数据
data=pd.read_excel(input_table_path)
dataMat=np.array(data)
#dataMat 为要做主成分赋权的数据
weight=PCA(dataMat)
print('指数为：',weight)