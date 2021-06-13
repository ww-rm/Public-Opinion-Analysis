import json
# 遍历文档用的
import os
import pandas as pd
# 提取关键词用的
import yake
# 将中文符号转换成英文符号
import unicodedata
# 分句、分词
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re
import numpy as np
# 下载文件
import wget
# 训练本地vector
from gensim.models import Word2Vec
# dataframe中的list转list
from ast import literal_eval
import sys
from .glove_vec import PretrainedVector

def load_json_data_from_dir(dirname):
    """

    Parameters
    ----------
    dirname : str
        directory that keeps your news json files

    Returns
    -------
    text : list[str]
        data extracted from jsons including time, headline, text, url, source and filename
    data : pd.DataFrame
        dataframe of text

    """
    text = []
    # 遍历文档
    for root, dirs, files in os.walk(dirname):
        for file in files:
            try:
                # 获取文件名
                filename = os.path.splitext(file)[0]\
                # 读取文件
                content = json.load(open(root + '/' + file, 'r', encoding = 'utf-8-sig'))
                # 去除无效文件
                if content['Text'] == '' or content['Headline'] == '':
                    continue
                # 文件名添加到文件中，方便后续生成中间件
                content['FileName'] = filename
                # 文本统一编码
                content['Text'] = unicodedata.normalize('NFKC', content['Text'])
                content['Text'] = re.sub(u"[\u4e00-\u9fa5]", "", content['Text'])
                # 中英文标点切换
                table = {ord(f):ord(t) for f,t in zip('，、。！？【】（）“”‘’',
                                                      ',,.!?[]()""\'\'')}
                content['Text'] = content['Text'].translate(table)
                # 文本全小写
                content['Text'] = content['Text'].lower()
                # 将句子隔开
                content['Text'] = content['Text'].replace('.', '. ')
                # 去除换行符
                content['Text'] = content['Text'].replace(' - ', ' ')
                # 标题统一编码
                content['Headline'] = unicodedata.normalize('NFKC', content['Headline'])
                content['Headline'] = re.sub(u"[\u4e00-\u9fa5]", "", content['Headline'])
                # 去除报刊标记
                split_punc = [' -', ' –', ' |']
                for punc in split_punc:
                    content['Headline'] = content['Headline'].split(punc)[0]
                    if content['Headline'][-1] != '.':
                        content['Headline'] += '.'
                text.append(content)
            except:
                continue
    print(text)
    # 讲读取的数据放入dataframe，去除不必要的信息
    data = pd.DataFrame(text)
    drop_list = ['Type', 'Section', 'Writers', 'MainKeyWord', 'AdditionalKeyWord']
    data = data.drop(columns=drop_list)
    return text, data
    
def json_print(text):
    # 格式化输出json文件，缩进4个单位
    print(json.dumps(text, sort_keys = True, indent = 4))
    
def yake_it(text):
    """

    Parameters
    ----------
    text : str
        text of an article

    Returns
    -------
    keywords : list[str]
        keywords of an article

    """
    language = "en"
    max_ngram_size = 3
    deduplication_thresold = 0.9
    deduplication_algo = 'seqm'
    windowSize = 1
    numOfKeywords = 10

    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, 
                                                dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, 
                                                windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(text)
    return keywords
    
def extract_key_phrases_from_doc(docs):
    """

    Parameters
    ----------
    docs : list[str]
        list of articles

    Returns
    -------
    phrases_list : list[turple]
        list of phrases turple

    """
    # doc_phrases用来存储一篇文档的所有关键词
    # phrases_list用来存储所有文档的所有关键词
    phrases_list = []
    for doc in docs:
        # 提取关键词
        key_phrases_dict = yake_it(doc['Text'])
        phrases_list.append(key_phrases_dict)
    return phrases_list
    

def list_to_dict(phrases):
    """

    Parameters
    ----------
    phrases : list[str]
        list of phrases

    Returns
    -------
    phrases_dict : dict
        {phrase1: number1, phrase2: number2}
        dict of numberize phrases

    """
    # 去重，编号
    phrases = list(set(phrases))
    num_phrases = len(phrases)
    phrases_dict = {}
    for i in range(num_phrases):
        phrases_dict[phrases[i]] = i
    return phrases_dict

def sentences_tokenize(text):
    """

    Parameters
    ----------
    text : pd.DataFrame
        raw_data

    Returns
    -------
    sentences : list
        tokenized sentences

    """
    sentences = []
    for raw_data in text:
        sentences.append(sent_tokenize(raw_data['Text']))
    return sentences

def words_tokenize(text): 
    """

    Parameters
    ----------
    text : pd.DataFrame
        raw_data

    Returns
    -------
    words : list
        tokenized words

    """
    words = []
    for raw_data in text:
        # 将符号替换成空格
        data = re.sub('[^\w ]', ' ', raw_data['Text'])
        word = word_tokenize(data)
        words.append(word)
    return words


def load_glove(glove_dir) -> PretrainedVector:
    """
        
    Parameters
    ----------
    glove_dir : str
        the path of glove

    Returns
    -------
    glove: dict like object
        can use `get` or `__getitem__` like a normal dict
       {'word1': vec1, 'word2': vec2, ...}
    """
    return PretrainedVector(glove_dir)

def _load_glove(glove_dir) -> dict:
    """
        
    Parameters
    ----------
    glove_dir : str
        the path of glove

    Returns
    -------
    glove: dict
        {'word1': vec1, 'word2': vec2, ...}

    """
    if not os.path.exists(glove_dir):
        wget.download('http://downloads.cs.stanford.edu/nlp/data/glove.840B.300d.zip', glove_dir)
    # 获取词向量
    # 该词向量文件形式为：词 空格 词向量，然后换行
    glove = {}
    with open(glove_dir, encoding = 'utf-8') as f:
        for line in f:
            values = line.split()
            try:
                word = values[0]
                coefs = np.asarray(values[1:], dtype = 'float32')
                glove[word] = coefs
            except:
                continue
    return glove

def get_doc_vector(words, glove, alpha=0.2, model_path='local.model', stopwords_path='stopwords.txt'):
    """

    Parameters
    ----------
    words : list[str]
        to train the word2vec
    glove : GloVe
       
    alpha : int, optional
        decide the fusion rate. The default is 0.2.

    model_path: str
        path to save or load model
    stopwords_path: str
        path for stopwords.txt

    Returns
    -------
    doc_vector : list[int]
        vector of document

    """
    if os.path.exists(model_path):
        # 若存在训练过的model，直接载入
        print('Loading model...')
        model = Word2Vec.load(model_path)
        # # 添加语料
        # model.build_vocab(words, update=True)
        # # 增量训练
        # model.train(words, total_examples=model.corpus_count, epochs=model.epochs)
        # 保存模型
        model.save(model_path)
        print('saving model...')
    else:
        # 若不存在，则生成
        print('training model...')
        # 用skip-grams模型，CBOW会导致向量过大
        model = Word2Vec(words, sg=1, min_count=0, size=300)
        # 保存模型
        model.save(model_path)
        print('saving model...')
    
    print('generating vectors...')
    stopwords = open(stopwords_path, 'r').read().split('\n')
    doc_vector = []
    for doc in words:
        vector = np.array([0.0 for _ in range(300)])
        word_count = 0
        for word in doc:
            if word not in stopwords:
                if word not in glove:
                    # glove里没有，则直接用训练出的word2vec
                    vector += model.wv[word]
                    word_count += 1
                else:
                    # glove里有，则与本地vec以一定比例融合
                    vector += model.wv[word] * alpha + glove[word] * (1 - alpha)
                    word_count += 1
        # 求平均
        vector /= word_count
        doc_vector.append(vector)
        
    return doc_vector

def dataframe_list_to_list(data):
    """

    Parameters
    ----------
    data : pd.Series

    Returns
    -------
    list_data : list
        to transfrom the list stored as string in the pd

    """
    list_data = []
    for i in range(data.shape[0]):
        list_data.append(literal_eval(data.iloc[i]))
    return list_data

def sentences_to_words(sentences):
    """

    Parameters
    ----------
    sentences : pd.Series

    Returns
    -------
    words : list[str]
        all the tokenized sentences in a list

    """
    sentences = dataframe_list_to_list(sentences)
    words = []
    for doc in sentences:
        for sentence in doc:
            no_punc_sentence = re.sub('[^\w ]', ' ', sentence)
            words.append(word_tokenize(no_punc_sentence))
    return words

def build_knowledge_graph(data, n_clusters, today, save_dir='data/hotspot/'):
    """

    Parameters
    ----------
    data : processed_data
    
    n_clusters : int
    
    today : datetime

    save_dir: str

    Returns
    -------
    make txt files and write setences in the same cluster into

    """
    save_dir = os.path.join(save_dir, 'knowledge/')
    os.makedirs(save_dir, exist_ok=True)
    for i in range(n_clusters):
        # 获取同一聚类下的数据
        chosen_data = data.loc[data.Cluster == i]
        print(chosen_data.info())
        
        # 集合所有句子
        sentences = dataframe_list_to_list(chosen_data.Sentences)
        # 展开成一维
        sentences = [j for i in sentences for j in i]
        print(sentences[0:1])
        print('cluster ', i, ' sentences number:', len(sentences))
        
        # 文件操作
        time = today.strftime("%Y-%m-%d")

        filename = save_dir + time + '-' + str(i) + '.txt'
        print(filename)
        
        f = open(filename, "w", encoding='utf-8')
        f.write(chosen_data.iloc[0].Summary + '\n')
        for line in sentences:
            f.write(line + '\n')
        f.close()
        
def build_keywords_cloud(data):
    """

    Parameters
    ----------
    data : pd.DataFrame
        data in the same cluster

    Returns
    -------
    keywords_cloud : list[tuple]
        [(keyword1, score), (keyword2, score), ...]

    """
    # 取出keywords，转为list
    keywords = dataframe_list_to_list(data.Keywords)
    keywords = [x for y in keywords for x in y]

    keywords_dict = {}
    for tur in keywords:
        if tur[0] not in keywords_dict:
            # 不存在就新建，以空字典为默认值，方便后续扩展
            keywords_dict.setdefault(tur[0], []).append(tur[1])
        else:
            # 存在就将值放入
            keywords_dict[tur[0]].append(tur[1])

    keywords_cloud = {}
    for key, value in keywords_dict.items():
        # 合并得分
        score = sum(value) / len(value) * len(value)
        keywords_cloud[key] = score
    # 转为(key, value)的tuple，并存储在list中
    keywords_cloud = list(zip(keywords_cloud.keys(), keywords_cloud.values()))
    return keywords_cloud
        
def build_topic(data, n_clusters, today, hotscore, save_dir='data/hotspot/'):
    """

    Parameters
    ----------
    data : processed_data
    
    n_clusters : int
    
    today : datetime
    
    hotscore : list[int]

    save_dir: str
        where to save

    Returns
    -------
    make json files and write detail,topic,hotscore,hotscore_time
    in the same cluster into

    """
    save_dir = os.path.join(save_dir, 'topic/')
    os.makedirs(save_dir, exist_ok=True)
    for i in range(n_clusters):
        # 获取统一聚类下的数据
        chosen_data = data.loc[data.Cluster == i]
        print(chosen_data.Summary)
        # 生成detail
        detail = 'Related news:'
        for j in range(chosen_data.shape[0]):
            # 合并headline和url两项
            detail += '<br><a href = "' + chosen_data.iloc[j].URL + \
            '" target="_black">Headline: ' + chosen_data.iloc[j].Headline + '</a>'
        # 生成词云
        keywords_cloud = build_keywords_cloud(chosen_data)
        # 转换成json格式
        hotscore_time = today.strftime("%Y-%m-%d")
        json_data = [{'topic': chosen_data.iloc[0].Summary, 'detail': detail,
                      'hotscore_time': hotscore_time, 'hotscore': hotscore[i],
                      'keywords_cloud': keywords_cloud}]
        
        #文件操作
        filename = save_dir + hotscore_time + '-' + str(i) + '.json'
        print(filename)
        json.dump(json_data, open(filename, 'w', encoding='utf-8'))
