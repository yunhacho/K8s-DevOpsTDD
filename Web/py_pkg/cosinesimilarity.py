import numpy as np
class CosineSimilarity():
    def get_CosineSimilarity(self, document_1, document_2):
        vector_1, vector_2= self.make_vector(document_1, document_2)
        dot=np.dot(vector_1, vector_2)
        return dot/(np.linalg.norm(vector_1)*np.linalg.norm(vector_2))
        
    def make_vector(self, target, compare):
        words_in_target=target.keys()
        words_only_in_compare=compare.keys()-words_in_target

        target_vector=list(target.values())
        target_vector.extend([0]*len(words_only_in_compare))

        compare_vector=[0]*len(words_in_target)
        for i, word in enumerate(words_in_target): 
            if word in compare.keys(): compare_vector[i]=compare[word] 
        compare_vector.extend([compare[word] for word in words_only_in_compare])
        
        return target_vector, compare_vector

    def get_Top3_ConsineSimilarity(self, url, documents):
        try:
            cosinesimilarity={other:self.get_CosineSimilarity(documents[url], documents[other]) for other in documents.keys() if url!=other}
            return sorted(cosinesimilarity.items(), reverse=True, key=lambda item: item[1])[0:3]
        except KeyError as e:
            return []

