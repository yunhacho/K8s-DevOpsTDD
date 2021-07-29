'''
TDD Cosine Similarity FUNCTION
'''
from py_pkg.cosinesimilarity import CosineSimilarity

def test_cosine_similarity():
    document_1 = {'I':1, 'love':1, 'banana':1}
    document_2 = {'I':1, 'love':1, 'banana':1, 'hate': 1, 'apple': 1}
    true=0.7745966692414834
    assert true == CosineSimilarity().get_CosineSimilarity(document_1, document_2)

def test_top3_consine_similarity():
    documents={
        'document_1' : {'I':1, 'love':1, 'banana':1},
        'document_2' : {'I':1, 'love':1, 'banana':1, 'hate': 1, 'apple': 1},
        'document_3' : {'I':1, 'hate':1, 'banana':1},
        'document_4' : {'I':1, 'hate':1, 'banana':1, 'and': 1, 'apple': 1}
    }
    
    true_1=[('document_2', 0.7745966692414834), ('document_3', 0.6666666666666667), ('document_4', 0.5163977794943222)]
    true_2=[]
    true_3=[]

    assert true_1 == CosineSimilarity().get_Top3_ConsineSimilarity('document_1', documents)
    assert true_2 == CosineSimilarity().get_Top3_ConsineSimilarity('document_5', documents)
    assert true_3 == CosineSimilarity().get_Top3_ConsineSimilarity('document_1', documents['document_1'])
    
    del documents['document_4']
    true_4=[('document_2', 0.7745966692414834), ('document_3', 0.6666666666666667)]
    assert true_4 == CosineSimilarity().get_Top3_ConsineSimilarity('document_1', documents)

    