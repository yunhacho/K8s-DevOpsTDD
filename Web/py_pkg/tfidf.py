import sys
from elasticsearch import Elasticsearch
import math
class TFIDF():
    def __init__(self, url, es_host="elastic-dev-svc.dev.svc.cluster.local", es_port="9200"):
        self.es=Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
        self.url=url
        self.compute_WordFreq_from_ObjectURL()
        
    def compute_WordFreq_from_ObjectURL(self):
        query ={
            "query":{"bool":{"must":{"match":{"url": self.url}}}},
            "_source":["url", "words", "frequencies"]
            }
        result=self.es.search(index="urls", body=query, size=1)

        self.size=result['hits']['total']['value']; self.id=result['hits']['hits'][0]['_id']

        self.wordsOfURLs=[result['hits']['hits'][0]['_source']['words']]
        self.freqOfURLs=[result['hits']['hits'][0]['_source']['frequencies']]

        self.entire_wordfreq={ word: frequency for word, frequency in zip(self.wordsOfURLs[0], self.freqOfURLs[0])}
        return self.wordsOfURLs[0], self.freqOfURLs[0]

    def select_ComparisonTargetURLs_from_ElasticSearch(self):
        query={ 
            "query":{"bool":{"must":[{"match_all":{}}],
            "must_not":[{"match": {"id": str(self.id)}}]}}, "size": str(self.size)}
        result=self.es.search(index="urls", body=query)
        return [ url for url in result['hits']['hits'] if url['_source']['url']!=self.url]
    
    def get_ComparisonTargetURLs_from_ElasticSearch(self):
        return [url['_source']['url'] for url in self.select_ComparisonTargetURLs_from_ElasticSearch()]

    def compute_WordFreq_from_ComparisonTargetURLs(self):
        TargetURLs=self.select_ComparisonTargetURLs_from_ElasticSearch()
        for TargetURL in TargetURLs: self.compute_WordFreq_from_ComparisonTargetURL(TargetURL)
        return self.entire_wordfreq

    def compute_WordFreq_from_ComparisonTargetURL(self, TargetURL):
        TargetWords=TargetURL['_source']['words']
        TargetFreqs=TargetURL['_source']['frequencies']
        
        for word, frequency in zip(TargetWords, TargetFreqs):
            if word not in self.entire_wordfreq.keys(): self.entire_wordfreq[word]=frequency
            else: self.entire_wordfreq[word]+=frequency
        self.wordsOfURLs.append(TargetWords); self.freqOfURLs.append(TargetFreqs)

    def computeTFIDF(self, words, frequency, wordsOfURLs):
        TFofWords=self.computeTF(words, frequency)
        IDFofWords=self.computeIDF(wordsOfURLs)
        TFIDFofWords={word: TFvalue*IDFofWords[word] for word, TFvalue in TFofWords.items()}
        return TFIDFofWords

    def computeIDF(self, wordsOfURLs):
        IDFofWords={}; countOfURLs=len(wordsOfURLs)
        setOfEntireWord=set([word for wordsOfURL in wordsOfURLs for word in wordsOfURL])
        for word in setOfEntireWord:
            countOfWord=0
            for wordsOfURL in wordsOfURLs: 
                if word in wordsOfURL: countOfWord+=1
            IDFofWords[word]=math.log(countOfURLs/float(countOfWord))
            
        return IDFofWords
    
    def computeTF(self, words, frequency):
        TFofWords={word: frequency/float(len(set(words))) for word, frequency in zip(words, frequency)}
        return TFofWords

    def compute_Top10_words(self):
        self.compute_WordFreq_from_ObjectURL()
        self.compute_WordFreq_from_ComparisonTargetURLs()
        TFIDFofWords=self.computeTFIDF(self.wordsOfURLs[0], self.freqOfURLs[0], self.wordsOfURLs)
        TFIDFofWords=sorted(TFIDFofWords.items(), reverse=True, key=lambda item: item[1])
        return TFIDFofWords[:10]

if __name__ == "__main__":

    input_urls=[
		"http://cassandra.apache.org/", # 찾고자 하는 url
    	"http://archiva.apache.org/",
   		"http://directory.apache.org/"
    ]

    instance = TFIDF(input_urls[0])
    r=instance.compute_WordFreq_from_ComparisonTargetURLs()
