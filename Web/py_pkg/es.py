from elasticsearch import Elasticsearch


class ES():
    def __init__(self, host, port):
        self.elasticsearch=Elasticsearch([{'host':host, 'port':port}], timeout=30)
    
    def call_data_from_elasticsearch(self):
        query={ "query":{"bool":{"must":[{"match_all":{}}]}}}
        return self.elasticsearch(index='urls', body=query)

    def get_wordfrequency_by_url(self):
        result=self.call_data_from_elasticsearch()
        return { urlitem['_source']['utl']: {word:freq for word, freq in zip(urlitem['_source']['words'], urlitem['_source']['frequencies'])} for urlitem in result['hits']['hits']}

if __name__=="__main__":
    es=ES(host, port)
    print(es.get_wordfrequency_by_url())