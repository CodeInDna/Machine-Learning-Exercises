import nltk
nltk.download(['punkt', 'wordnet', 'averaged_perceptron_tagger'])

import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin

url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


def tokenize(text):
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens


class StartingVerbExtractor(BaseEstimator, TransformerMixin):
    '''
    You don't need to put __init__ in your Class.

    You will need it if you want things to happen automatically to your object when it is instantiated, 
    e.g. have assignments that want to carry on inside the program.
    
    class A(object):
    def f():
        print 'foo'
    And you can of course use it, in this manner:
    a = A()
    a.f()
    
    otherwise:
    class A(object):
        def __init__(self,input):
            self.input=input
        def f(self,sub):
            
            print (self.input-sub)
    And you can of course use it, in this manner:
    a = A(10)
    a.f(5)=> 5
    
    '''

    def starting_verb(self, text):
        sentence_list = nltk.sent_tokenize(text)
        for sentence in sentence_list:
            pos_tags = nltk.pos_tag(tokenize(sentence))
            first_word, first_tag = pos_tags[0]
            if first_tag in ['VB', 'VBP'] or first_word == 'RT':
                return True
        return False

    def fit(self, x, y=None):
        return self

    def transform(self, X):
        X_tagged = pd.Series(X).apply(self.starting_verb)
        return pd.DataFrame(X_tagged)