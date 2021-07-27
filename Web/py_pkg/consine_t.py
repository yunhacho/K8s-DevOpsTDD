import sys
import os
import numpy as np
from es import ES

class Cosine_Similarity():
    def __init__(self, url, entireWordFrequency):
        self.url=url
        self.entireWordFrequency=entireWordFrequency
        self.wordFrequency=entireWordFrequency[url]
    
    def get_Top3_cosine_similarity_url(self):
        entire_cosine_similarity=self.get_cosine_similarity_of_all_url()
        result=sorted(entire_cosine_similarity.items(), reverse=True, key=lambda item: item[1])        
        return result[0:3]

    def get_cosine_similarity_of_all_url(self):
        return {url:self.compute_cosinesimilarity(url) for url in self.entireWordFrequency.keys() if url!=self.url}
    def compute_cosinesimilarity(self, other_url):
        self_vector, other_vector=self.make_vector(other_url)
        dotpro=np.dot(self_vector,other_vector)
        return dotpro/(np.linalg.norm(self_vector)*np.linalg.norm(other_vector))

    def make_vector(self, other_url):
        other_wordfreq=self.entireWordFrequency[other_url] 
        sef_of_words=list(set().union(self.wordFrequency.keys(), self.entireWordFrequency[other_url].keys()))
        
        self_vector=[0]*len(sef_of_words); other_vector=[0]*len(sef_of_words)
        for idx, word in enumerate(sef_of_words):
            if word in self.wordFrequency.keys(): self_vector[idx]= self.wordFrequency[word]
            if word in other_wordfreq.keys(): other_vector[idx]=other_wordfreq[word]
        return self_vector, other_vector

if __name__ =="__main__":
        url = "http://cassandra.apache.org/"
        host=os.environ['ELASTICSEARCH_URL']; port='9200'
        es=ES(host, port)
        entireWordFrequency=es.get_wordfrequency_by_url()

        cos = Cosine_Similarity(url, entireWordFrequency)
        for tup in cos.get_Top3_cosine_similarity_url():
             print("url: %-30s\tCosineSimilarity: %.10f" %(tup[0], tup[1]))

