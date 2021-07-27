import math
import os
from elasticsearch import Elasticsearch
#from es import ES

class TF_IDF():
    def __init__(self, url, entireWordFrequency):
        self.url=url
        self.entireWordFrequency=entireWordFrequency

    def compute_TF(self):
        wordfrequency=self.entireWordFrequency[self.url]
        return {word: frequency/float(len(wordfrequency.keys())) for word, frequency in wordfrequency.items()}
    
    def compute_IDF(self):
        IDF={}; uniqueWord=set()
        countOfURLs=len(self.entireWordFrequency)
        for url in self.entireWordFrequency.values(): uniqueWord.update(list(url.keys()))
        for word in uniqueWord:
            countOfWord=0
            for url in self.entireWordFrequency.values(): 
                if word in url.keys(): countOfWord+=1
            IDF[word]=math.log(countOfURLs/float(countOfWord))
        return IDF

    def compute_TFIDF(self):
        TF=self.compute_TF(); IDF=self.compute_IDF()
        return {word: tfvalue*IDF[word] for word, tfvalue in TF.items()}

    def get_Top10_TFIDF_words(self):
        TFIDF=self.compute_TFIDF()
        TFIDF=sorted(TFIDF.items(), reverse=True, key=lambda item: item[1])
        return TFIDF[:10]

if __name__=="__main__":
    url = "http://cassandra.apache.org/"
    host=os.environ['ELASTICSEARCH_URL']; port='9200'
    es=ES(host, port)
    entireWordFrequency=es.get_wordfrequency_by_url()
    tf=TF_IDF(url, entireWordFrequency)
    print(tf.compute_IDF())