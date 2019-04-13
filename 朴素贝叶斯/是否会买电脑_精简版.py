'''
手动实现贝叶斯
数据采用课本中的购买电脑的数据
'''
import pandas as pd

#计算p(X\yi)，其中yi为要分类的每个类别，X为所有的特征的集合{x1,x2,,,,xn}
def calPxy(feature,label,pX0,pX1):
    # index_0 = []
    # print(index_0)
    # index_1 = [label==1]

    union_fes = set(feature)
    for fe in list(union_fes):
        pX0[fe] = list(feature[label==0]).count(fe)/(len(feature)-sum(data_y))
        pX1[fe] = list(feature[label==1]).count(fe)/sum(data_y)
    # print(p0)
    # print(p1)


if __name__ == "__main__":
    data = pd.read_csv(r'data.csv', sep='\t')
    print(data)
    data_x = data.iloc[:, :-1]
    data_y = data.iloc[:, -1]
    # print(sum(data_y))
    print(data_y[data_y == 0])
    pX0 = {}  # 存放y=0的数据中每个属性的后验概率p(X\yi)
    pX1 = {}  # 存放y=1的数据中每个属性的后验概率p(X\yi)
    # print(list(data_x['income'][data_y == 0]).count('high'))

    for i in range(len(data_x.iloc[0,:])):
        calPxy(data_x.iloc[:,i], data_y,pX0,pX1)
    print(pX0)
    print(pX1)

    p_1 = sum(data_y)/len(data)               #相当于p(y0)
    p_0 = 1 - p_1                             #相当于p(y1)

    in_x = ['youth','medium','yes','fair']
    pre0 = 1*p_0
    pre1 = 1*p_1

    for fes in in_x:
        pre0 *= pX0[fes]
        pre1 *= pX1[fes]
    print(pre0)
    print(pre1)







