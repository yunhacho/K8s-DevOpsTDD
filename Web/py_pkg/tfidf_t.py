import math
from elasticsearch import Elasticsearch

class TF_IDF():
    def __init__(self, url, entireWordFrequency):
        self.url=url
        self.entireWordFrequency=entireWordFrequency

    def compute_TF(self):
        wordfrequency=self.entireWordFrequency[self.url]
        return {word: frequency/float(len(wordfrequency.keys())) for word, frequency in wordfrequency.items()}
    
    def compute_IDF(self):
        IDF={}
        countOfURLs=len(self.entireWordFrequency)
        uniqueWord=set([word for url in self.entireWordFrequency.keys() for word in url.keys()])
        for word in uniqueWord:
            countOfWord=0
            for url in self.entireWordFrequency.keys(): if word in url.keys(): countOfWord+=1
            IDF[word]=math.log(countOfURLs/float(countOfWord))
        return IDF

    def compute_TFIDF(self):
        TF=self.compute_TF(); IDF=self.compute_IDF()
        return {word: tfvalue*IDF[word] for word, tfvalue in TF.items()}

    def get_Top10_TFIDF_words(self):
        TFIDF=self.compute_TFIDF()
        TFIDF=sorted(TFIDF.items(), reverse=True, key=lambda item: item[1])
        return TFIDF[:10]