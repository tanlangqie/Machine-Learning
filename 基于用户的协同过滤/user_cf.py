"""
@author: LiShiHang
@software: PyCharm
@file: user_cf.py
@time: 2019/4/4 8:31
@desc:
"""
import math
import data_preprocessing
import pandas as pd


class UserCF():

    def __init__(self, path_rating):

        self.data_rating = pd.read_csv(path_rating)

    def calc_user_sim(self, item1, item2):
        """
        计算相似度
        :param item1:
        :param item2:
        :return:
        """
        cosine = len(set(item1) & set(item2)) / math.sqrt(len(item1) * len(item2))
        return cosine

    def get_users_topN(self, source_user_id, N):
        """
        得到N个相似用户
        :param source_user_id:
        :param topN:
        :return: [[用户ID，相似度]]
        """

        source_user_movies = self.data_rating[self.data_rating['UserID']== source_user_id]["MovieID"]  # 目标用户看过的电影ID

        others_id = [
            i for i in set(
                self.data_rating['UserID']) if i != source_user_id]  # 其他用户ID

        others_movies = [
            self.data_rating[self.data_rating['UserID'] == i]["MovieID"] for i in others_id]  # [[其他用户看的电影ID] 其他用户ID]

        sim_list = [
            self.calc_user_sim(
                source_user_movies,
                movies) for movies in others_movies]  # 根据目标用户和其他用户 看过的电影ID计算相似度

        sim_list = sorted(zip(others_id, sim_list),
                          key=lambda x: x[1], reverse=True)

        return sim_list[:N]

    def get_candidate(self, source_user_id,top_n_id ):
        """
        得到候选电影清单
        :param source_user_id:
        :return:
        """

        source_user_movies = set(
            self.data_rating[self.data_rating['UserID'] == source_user_id]["MovieID"])  # 目标用户看过的电影ID
        others_movies = []#set([])
        for i in top_n_id:
            others_movies.extend(list(self.data_rating[self.data_rating['UserID'] == i ]["MovieID"]))
        import pandas as pd
        others_movies = set(others_movies)

        candidate_movies = others_movies - source_user_movies

        return candidate_movies

    def get_item_topN(self, top_n_users, candidate_movies, topN):
        """
        得到推荐电影列表
        :param top_n_users:
        :param candidate_movies:
        :param topN:
        :return:
        """
        print(top_n_users)
        top_n_users_data = [self.data_rating[self.data_rating['UserID'] == i] for i, _ in top_n_users]  # 相似用户数据
        # print(type(top_n_users_data))   #list
        # print(type(top_n_users_data[0]))   #<class 'pandas.core.frame.DataFrame'>

        interest_item = []             #存放候选电影以及最相似的N个人对他的综合评分

        for cm in candidate_movies:    # 对每一个候选电影
            tmp = []                   #存放最相似的N个人对候选电影的喜爱程度，长度为N
            for user_data in top_n_users_data:  # 对相似用户a的所有数据来说，（pandas）
                if cm in user_data["MovieID"].values:    #相似用户a看过此电影，则记录评分，没看过则记录0分
                    tmp.append(user_data[user_data["MovieID"]== cm]['Rating'].values[0] / 5.0)
                else:
                    tmp.append(0)

            interest = sum([top_n_users[i][1] * tmp[i] for i in range(len(top_n_users))])  # 相似用户对每个候选电影的感兴趣度（评分）
            interest_item.append((cm, interest))

        interest_item = sorted(interest_item, key=lambda x: x[1], reverse=True)

        return interest_item[:topN]


if __name__ == '__main__':

    #data_preprocessing.read_data()

    ucf = UserCF("ratings.csv")

    ui = 1
    top_n_users = ucf.get_users_topN(ui, 10)         #得到相似度排行前10的人的ID以及相似度
    top_n_id = []                                    #存放前10人的ID
    for i in top_n_users:
        top_n_id.append(i[0])

    candidate = ucf.get_candidate(ui,top_n_id)   #从相似度排行前10的人中选出候选电影

    top_n_movies = ucf.get_item_topN(top_n_users, candidate, 10)

    print(top_n_movies)  # 推荐的电影ID，推荐程度

    # 显示电影名
    movies = pd.read_csv("movies.csv")
    # print("*" * 20)
    # for i in ucf.data_rating[ucf.data_rating["UserID"]==ui]["MovieID"]: # 目标用户看过的电影名称
    #     print(*movies[movies["MovieID"]==i].values[0])
    print("*" * 20)
    for i, j in top_n_movies:  # 推荐看的电影名称
        print(*movies[movies["MovieID"] == i].values[0], j)
