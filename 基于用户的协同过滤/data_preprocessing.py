"""
@author: LiShiHang
@software: PyCharm
@file: user_cf.py
@time: 2019/4/10 21:12
@desc:
"""
import pandas as pd
import numpy as np

np.set_printoptions(threshold=np.inf)


def read_data(dir="./data/ml-1m/"):
    """
    将data/ml-1m文件夹中的dat文件转化为csv
    :param dir:
    :return:
    """
    ####################################
    f_users = pd.read_table(
        dir + "users.dat",
        engine="python",
        sep="::",
        names=[
            'userID',
            'Gender',
            'Age',
            'Occupation',
            'Zip-code'])
    f_users.to_csv("users.csv", index=False)
    f_users.info()
    ###########################################

    f_ratings = pd.read_table(dir + "ratings.dat", engine="python", sep="::",
                              names=['UserID', 'MovieID', 'Rating', 'Timestamp'])
    f_ratings.to_csv("ratings.csv", index=False)
    f_ratings.info()

    ################################################
    f_movies = pd.read_table(dir + "movies.dat", engine="python", sep="::",
                             names=['MovieID', 'Title', 'Genres'])
    f_movies.to_csv("movies.csv", index=False)
    f_movies.info()

    print("finish.")
read_data(dir="./data/ml-1m/")