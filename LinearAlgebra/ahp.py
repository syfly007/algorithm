
# coding: utf-8

# 层次分析法

from __future__ import division
import numpy as np
import time

# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.platypus import Table,TableStyle


class AHP:
    def __init__(self):
        self.variable = {}

    def calculate_weight(self, columns_names, judgment_matrix):
        '''
        和法求权重
        columns_names:a list of data names used
        judgment_matrix:the judgment_matrix of AHP given by expert
        '''
        ########basic parameters of input######
        nrow, ncol = judgment_matrix.shape
        if nrow != ncol:
            print ("the matrix is NOT square")
            return
        if len(columns_names) != nrow:
            print ("columns_names NOT MATCH the shape of judgment_matrix")
            return
        ####string version of judgment matrix####
        str_matrix = []
        for i in range(nrow):
            str_i = []
            for j in range(ncol):
                p = judgment_matrix[i, j]
                if judgment_matrix[i, j] >= 1:
                    str_i.append(str(int(p)).center(5))
                else:
                    str_i.append(('1/' + str(int(1.0 / p))).center(5))
            str_matrix.append(str_i)
        #########Judgment of consistency#######
        val, vec = np.linalg.eig(judgment_matrix)
        val_list = list(abs(val))
        max_val = max(val_list)
        # CI
        CI = 1.0 * (max_val - nrow) / (nrow - 1)
        # RI:it is hard to give a proper weight matrix if n>=11
        RI = dict([(1, 0), (2, 0), (3, 0.58), (4, 0.90), (5, 1.12),
                   (6, 1.24), (7, 1.32), (8, 1.41), (9, 1.45), (10, 1.49)])
        # CR
        CR = 1.0 * CI / RI[nrow]
        if CR < 0.1:
            # normalize each columns
            M = np.zeros((nrow, ncol))
            for j in range(ncol):
                col_sum = np.sum(judgment_matrix[:, j])
                M[:, j] = 1.0 * judgment_matrix[:, j] / col_sum
            # mean each row
            C = []
            for i in range(nrow):
                C.append(np.mean(M[i, :]))
            C = C / sum(C)
            self.variable = {"method": "AHP",
                             "columns": columns_names,
                             "judgment_matrix": judgment_matrix,
                             "max_val": max_val,
                             "wide": ncol,
                             "CI": CI,
                             "RI": RI[ncol],
                             "CR": CR,
                             "weight": C}


import pandas as pd
input_table_path = 'ahp-data.xlsx'
# input_table_path:为excel的存储路径和名称
# 输入数据需为数值型数据
data = pd.read_excel(input_table_path)
# 获取列名称，即变量名称
col_names = list(data.columns)
print(col_names)
# col_names 为需要做层次分析的变量名称，例如：col_names=['旅游收入增长指数','旅游收入GDP占比指数','旅游扶贫贡献指数','旅游投资增值指数','旅游就业增长指数']
m = np.array(data)
a = AHP()
a.calculate_weight(col_names, m)
b = a.variable
print (b['columns'], '的权重(w1,w2,....)分别为：', b['weight'])
# t = np.array([147.96, 91.85, 57.4, 136.8, 58.8])
# print(np.dot(t, np.array(b['weight'])))
