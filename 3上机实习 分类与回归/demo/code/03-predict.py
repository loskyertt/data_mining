#-*- coding: utf-8 -*-

# 代码6-5

import sys
sys.path.append('../code')  # 设置路径
import numpy as np
import pandas as pd
from GM11 import GM11  # 引入自编的灰色预测函数

inputfile1 = '3上机实习 分类与回归/demo/tmp/new_reg_data.csv'  # 输入的数据文件
inputfile2 = '3上机实习 分类与回归/demo/data/data.csv'  # 输入的数据文件
new_reg_data = pd.read_csv(inputfile1)  # 读取经过特征选择后的数据
data = pd.read_csv(inputfile2)  # 读取总的数据
new_reg_data.index = range(1994, 2014)
new_reg_data.loc[2014] = None
new_reg_data.loc[2015] = None
l = ['x1', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x13']
for i in l:
  f = GM11(new_reg_data.loc[range(1994, 2014),i].values)[0]
  new_reg_data.loc[2014,i] = f(len(new_reg_data)-1)  # 2014年预测结果
  new_reg_data.loc[2015,i] = f(len(new_reg_data))  # 2015年预测结果
  new_reg_data[i] = new_reg_data[i].round(2)  # 保留两位小数
outputfile = '3上机实习 分类与回归/demo/tmp/new_reg_data_GM11.csv'  # 灰色预测后保存的路径
y = list(data['y'].values)  # 提取财政收入列，合并至新数据框中
y.extend([np.nan,np.nan])
new_reg_data['y'] = y
new_reg_data.to_csv(outputfile)  # 结果输出
print('预测结果为：\n',new_reg_data.loc[2014:2015,:])  # 预测结果展示



# 代码6-6

# import matplotlib.pyplot as plt
# from sklearn.svm import LinearSVR

# inputfile = '3上机实习 分类与回归/demo/tmp/new_reg_data_GM11.csv'  # 灰色预测后保存的路径
# data = pd.read_csv(inputfile)  # 读取数据
# feature = ['x1', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x13']  # 属性所在列
# # data_train = data.loc[range(1994,2014)].copy()  # 取2014年前的数据建模
# data_train = data.iloc[:20].copy()  # 取前20行数据，相当于取1994到2013年的数据
# data_mean = data_train.mean()
# data_std = data_train.std()
# data_train = (data_train - data_mean)/data_std  # 数据标准化
# x_train = data_train[feature].values  # 属性数据
# y_train = data_train['y'].values  # 标签数据

# linearsvr = LinearSVR()  # 调用LinearSVR()函数
# linearsvr.fit(x_train,y_train)
# x = ((data[feature] - data_mean[feature])/data_std[feature]).values  # 预测，并还原结果。
# data['y_pred'] = linearsvr.predict(x) * data_std['y'] + data_mean['y']
# outputfile = '3上机实习 分类与回归/demo/tmp/new_reg_data_GM11_revenue.csv'  # SVR预测后保存的结果
# data.to_csv(outputfile)

# print('真实值与预测值分别为：\n',data[['y','y_pred']])

# fig = data[['y','y_pred']].plot(subplots = True, style=['b-o','r-*'])  # 画出预测结果图
# plt.show()

import matplotlib.pyplot as plt
from sklearn.svm import LinearSVR
import pandas as pd

inputfile = '3上机实习 分类与回归/demo/tmp/new_reg_data_GM11.csv'  # 灰色预测后保存的路径
data = pd.read_csv(inputfile)  # 读取数据
feature = ['x1', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x13']  # 属性所在列
data_train = data.iloc[:20].copy()  # 取前20行数据，相当于取1994到2013年的数据
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean)/data_std  # 数据标准化
x_train = data_train[feature].values  # 属性数据
y_train = data_train['y'].values  # 标签数据

linearsvr = LinearSVR()  # 调用LinearSVR()函数
linearsvr.fit(x_train, y_train)
x = ((data[feature] - data_mean[feature])/data_std[feature]).values  # 预测，并还原结果
data['y_pred'] = linearsvr.predict(x) * data_std['y'] + data_mean['y']

outputfile = '3上机实习 分类与回归/demo/tmp/new_reg_data_GM11_revenue.csv'  # SVR预测后保存的结果
data.to_csv(outputfile)

print('真实值与预测值分别为：\n', data[['y', 'y_pred']])

# 绘制预测结果图
plt.figure(figsize=(10, 6))
years = list(range(1994, 2014)) + [2014, 2015]
plt.plot(years, data['y'], 'b-o', label='真实值')
plt.plot(years, data['y_pred'], 'r-*', label='预测值')

plt.xlabel('年份')
plt.ylabel('财政收入')
plt.title('真实值与预测值对比')
plt.legend()
plt.grid(True)
plt.show()
