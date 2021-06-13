import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
# 聚类
from sklearn.cluster import SpectralClustering
from sklearn import metrics
from sklearn.cluster import DBSCAN
# 文本摘要
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
# 热度指数
import datetime
from . import pre
# 计算余弦相似度
from sklearn.metrics.pairwise import cosine_similarity


class HotSpot():
    def __init__(self, data, vector):
        self.data = data
        self.vector = vector
        self.doc_number = data.shape[0]
        #self.n_clusters, self.data['Cluster'] = self.dbscan()
        self.n_clusters, self.data['Cluster'] = self.spectral_cluster()
        self.summary = self.summarize()
        self.timestamp = self.time_process()
        self.hotscore = self.compute_hotscore()
    
    def spectral_cluster(self):
        """

        Returns
        -------
        n_clusters: int
            number of clusters
        
        cluster : list[int]
            list of numbers of the same cluster articles

        """
        # 参数初始化，分别代表种类数，最大CH，最小DBI
        n_clusters, ch_max, db_min = 0, 0.0, 100
        similarity = self.vector
        # print(similarity.shape)

        for num in range(10, 20):
            # 聚类
            cluster = SpectralClustering(n_clusters=num, affinity='nearest_neighbors', n_neighbors=5).fit_predict(similarity)
            # 评估
            CH = metrics.calinski_harabasz_score(similarity, cluster)
            DB = metrics.davies_bouldin_score(similarity, cluster)
            # 择优
            if CH > ch_max and DB < db_min:
                ch_max = CH
                db_min = DB
                n_clusters = num
        # 重新聚类
        cluster = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors', n_neighbors=5).fit_predict(similarity)
                    
        return n_clusters, cluster
    
    def dbscan(self): 
        """

        Returns
        -------
        n_clusters : int
            number of clusters
            
        cluster : list[int]
            list of numbers of the same cluster articles

        """
        # 参数初始化，分别代表种类数，最大CH分数，最小DBI，密度半径
        n_clusters, ch_max, db_min, eps = 0, 0.0, 100, 0.0
        sites = self.vector
        for i in np.arange(0.01, 2, 0.01):
            # 聚类
            cluster = DBSCAN(eps=i).fit_predict(sites)
            # 只有一个类则继续
            if len(set(cluster)) == 1:
                continue
            # 计算CH和DBI
            CH = metrics.calinski_harabasz_score(sites, cluster)
            DB = metrics.davies_bouldin_score(sites, cluster)
            # 选最优方案
            if CH > ch_max and DB < db_min:
                ch_max = CH
                db_min = DB
                eps = i
                n_clusters = len(set(cluster))
        # 重新聚类
        cluster = DBSCAN(eps=eps).fit_predict(sites)
        cluster[cluster == -1] = n_clusters - 1
        
        return n_clusters, cluster
    
    def summarize(self):
        """

        Returns
        -------
        summary : list[str]
            list of summaries coresponding to clusters

        """
        summary = []
        for i in range(self.n_clusters):
            # 获取同类文章的标题
            data = self.data.loc[self.data.Cluster == i].Headline
            if data.shape[0] > 1:
                # 文章数足够多则拼接起来
                data = ' '.join(x for x in list(data))
            else:
                # 只有一个文章则data设为字符串格式
                data = list(data)[0]
                
            # 单文本摘要
            parser = PlaintextParser.from_string(data, Tokenizer('english'))
            # 设置语言
            stemmer = Stemmer('english')
            # 摘要
            summarizer = Summarizer(stemmer)
            # 设置停用词
            summarizer.stop_words = get_stop_words('english')
            # 取一个标题
            for sentence in summarizer(parser.document, 1):
                summary.append(str(sentence))
        return summary
    
    def time_process(self):
        """

        Returns
        -------
        timestamp : np.array
            mean time distance from today of each cluster

        """
        # 转格式为datetime
        time = []
        for i in range(self.data.shape[0]):
            time.append(datetime.datetime.strptime(self.data.iloc[i].Time, '%Y-%m-%d'))
        time = np.array(time)
        
        # 计算类别下平均时间跨度
        timestamp = []
        date = datetime.datetime.now()
        for i in range(self.n_clusters):
            # 计算时间跨度
            delta = date - time[self.data.loc[self.data.Cluster == i].index]
            # 获取天数差
            time_dist = []
            for j in range(len(delta)):
                time_dist.append(delta[j].days)
            # 计算平均值
            time_dist = np.array(time_dist).mean()
            timestamp.append(time_dist)
        timestamp = np.array(timestamp)
        return timestamp
    
    def compute_score(self, x, y):
        """

        Parameters
        ----------
        x : float
        y : float

        Returns
        -------
        percentage score

        """
        return np.log(1 + x) / np.log(1 + y)
    
    def time_score(self, cluster, bias=1.1):
        """

        Parameters
        ----------
        cluster : int
        bias : int, optional
            The default is 1.1.

        Returns
        -------
        time score according to the time from now

        """
        return 2 /(1 + np.power(self.timestamp[cluster], bias))
    
    def number_score(self, cluster):
        """

        Parameters
        ----------
        cluster : int

        Returns
        -------
        number score according to the number of articles

        """
        # 找类别下新闻数目最多的种类
        max_n = 0
        for i in range(self.n_clusters):
            if len(self.data.loc[self.data.Cluster == i]) > max_n: 
                max_n = len(self.data.loc[self.data.Cluster == i])
        return self.compute_score(len(self.data.loc[self.data.Cluster == cluster]), max_n)
    
    def source_score(self, cluster):
        """

        Parameters
        ----------
        cluster : int

        Returns
        -------
        source score accoding to the source number of the cluster

        """
        return self.compute_score((len(set(self.data.loc[self.data.Cluster == cluster].Source))), len(set(self.data.Source)))
    
    def compute_hotscore(self):
        """

        Returns
        -------
        hotscore : list[int]
            hot score of each cluster

        """
        hotscore = np.zeros(self.n_clusters)
        # 评分部分的权重参数
        alpha_t, alpha_n, alpha_s = 0.4, 0.5, 0.1
        for i in range(self.n_clusters):
            hotscore[i] = (alpha_t * self.time_score(i) + alpha_n * self.number_score(i) + alpha_s * self.source_score(i)) * 100
        return hotscore
