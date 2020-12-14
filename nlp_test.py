from itertools import product

import spacy
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet
from fuzzywuzzy import fuzz

stemmer = SnowballStemmer("german")
from spacy.lemmatizer import Lemmatizer, ADJ, NOUN, VERB
nlp = spacy.load("de_core_news_lg")
lemmatizer = nlp.vocab.morphology.lemmatizer
from nltk.corpus import stopwords

print(lemmatizer("Blätter", NOUN))
print(lemmatizer("blätter", NOUN))
print(stemmer.stem("Blätter"))
print(stemmer.stem("blätter"))
print(lemmatizer("Übungen", NOUN))
print(stemmer.stem("Übungen"))

print(lemmatizer("Deutschaufgabe", NOUN))
print(stemmer.stem("Deutschaufgabe"))


def similarity(w1, w2):
    list1 = wordnet.synsets(w1+'.n.01')
    print(list1)
    list2 = wordnet.synset(w2+'.n.01')
    return list1.path_similarity(list2)
    allsyns1 = set(ss for word in list1 for ss in wordnet.synsets(word))
    allsyns2 = set(ss for word in list2 for ss in wordnet.synsets(word))
    return max((wordnet.wup_similarity(s1, s2) or 0, s1, s2) for s1, s2 in
                    product(allsyns1, allsyns2))

print(nlp("Übungen").similarity(nlp("Übung")))
print(fuzz.ratio("Übungen", "Übung") / 100.)
print(nlp("Mathematik").similarity(nlp("Mathe")))
print(fuzz.ratio("Mathematik", "Mathe") / 100.)
print(nlp("Mathematik").similarity(nlp("Physik")))
print(fuzz.ratio("Mathematik", "Physik") / 100.)
print(fuzz.ratio("Mathematik", "mathematik") / 100.)
