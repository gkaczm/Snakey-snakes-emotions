import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import _pickle as cPickle
from sklearn.svm import LinearSVC

# the main preprocessing pipeline
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
svm_model = LinearSVC(random_state=0)


def contractions(s):
    s = re.sub(r"won't", "will not", s)
    s = re.sub(r"would't", "would not", s)
    s = re.sub(r"could't", "could not", s)
    s = re.sub(r"\'d", " would", s)
    s = re.sub(r"can\'t", "can not", s)
    s = re.sub(r"n\'t", " not", s)
    s = re.sub(r"\'re", " are", s)
    s = re.sub(r"\'s", " is", s)
    s = re.sub(r"\'ll", " will", s)
    s = re.sub(r"\'t", " not", s)
    s = re.sub(r"\'ve", " have", s)
    s = re.sub(r"\'m", " am", s)
    return s


def preprocess(sentence):
    sentence = contractions(sentence.lower())
    sentence = ' '.join(''.join(' ' if c in string.punctuation else c for c in sentence).split())
    sentence = re.sub(' +', ' ', sentence)
    stop = stopwords.words('english')
    sentence = ' '.join([word for word in sentence.split() if word not in stop])
    lemmatizer = WordNetLemmatizer()
    sentence = ' '.join([lemmatizer.lemmatize(w) for w in nltk.word_tokenize(sentence)])
    return sentence


def classify(sentence: str):
    with open('vectorizer.pkl', 'rb') as fid:
        vectorizer = cPickle.load(fid)
    with open('svm_classifier.pkl', 'rb') as fid:
        svm_model = cPickle.load(fid)
    sentence = preprocess(sentence)
    print(sentence)
    x_test_ = vectorizer.transform([sentence])
    y_test_pred_ = svm_model.predict(x_test_)
    return y_test_pred_[0]
