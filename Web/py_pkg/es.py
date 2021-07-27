import os
from elasticsearch import Elasticsearch

class ES():
    def __init__(self, host, port):
        self.es=Elasticsearch([{'host':host, 'port':port}], timeout=30)
    
    def call_data_from_elasticsearch(self):
        query={"query": {'match_all':{}}}
        return self.es.search(index='urls', body=query, size=100)

    def get_wordfrequency_by_url(self):
        result=self.call_data_from_elasticsearch()
        res={ urlitem['_source']['url']: {word:freq for word, freq in zip(urlitem['_source']['words'], urlitem['_source']['frequencies'])} for urlitem in result['hits']['hits']}
        return res
if __name__=="__main__":
    es_host=os.environ['ELASTICSEARCH_URL']; es_port='9200'
    es=ES(es_host, es_port)
    for url in es.get_wordfrequency_by_url():
        print(url)