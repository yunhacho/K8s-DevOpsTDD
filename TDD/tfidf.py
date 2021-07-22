import math
class TFIDF():
    def __init__(self, url, es_host, es_port):
        self.es=Elasticsearch([{'host':es_host, 'port':es_port}], timeout=30)
        self.url=url

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

    def compute_ObjectURL_from_ElasticSearch(self):
        Query ={
            "query":{"bool":{"must":{"match":{"url": self.url}}}},
            "_source":["url", "words", "frequencies"]
            }
        resultFromQuery=self.es.search(index="urls", body=query, size=1)
        self.size=resultFromQuery['hits']['total']['value']
        for url in resultFromQuery['hits']['hits']:
            self.id=res['_id']
            self.word_list.append(res['_source']['words'])
            self.freq_list.append(res['_source']['frequencies'])
        pass

    def compute_ComparisonTargetURLs_from_ElasticSearch(self):
        pass

    def compute_Top10_words(self):
        pass
    
    def 