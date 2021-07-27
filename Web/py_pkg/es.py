import os
from elasticsearch import Elasticsearch

class ES():
    def __init__(self, host, port):
        self.es=Elasticsearch([{'host':host, 'port':port}], timeout=30)
    
    def call_data_from_elasticsearch(self):
        query={ "query":{"bool":{"must":[{"match_all":{}}]}}}
        return self.es.search(index='urls', body=query)

    def get_wordfrequency_by_url(self):
        result=self.call_data_from_elasticsearch()
        return { urlitem['_source']['url']: {word:freq for word, freq in zip(urlitem['_source']['words'], urlitem['_source']['frequencies'])} for urlitem in result['hits']['hits']}

if __name__=="__main__":
    host=os.environ['ELASTICSEARCH_URL']; port='9200'
    es=ES(host, port)
    print(es.get_wordfrequency_by_url())