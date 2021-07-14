import math
class TFIDF():
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

