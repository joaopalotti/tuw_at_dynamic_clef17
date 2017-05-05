import glob
import os
import re
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_selection import SelectKBest, chi2

topics = glob.glob("topic*/")
regex = re.compile('[^a-z]')

def getcontent(path):

    files = glob.glob(path)
    content = []
    for doc in files:
        with open(doc) as f:
            fcontent = f.read().lower().strip()
            fcontent = regex.sub(' ', fcontent)
            content.append(fcontent)
    return content


for top in topics:
    print top
    pos = getcontent(os.path.join(top, "pos", "*")) #[:10]
    neg = getcontent(os.path.join(top, "neg", "*")) #[:10]
    y = [1] * len(pos) + [0] * len(neg)

    count_vect = CountVectorizer()
    counts = count_vect.fit_transform(pos + neg)
    tfidf_transformer = TfidfTransformer(use_idf=True, sublinear_tf=True)
    tfidf = tfidf_transformer.fit_transform(counts)

    ch2 = SelectKBest(chi2, k=200)
    X = ch2.fit_transform(tfidf, y)

    clf = MultinomialNB(fit_prior=False).fit(X, y)

    with open("%s.pickle" % (top.strip("/")), "w") as ofile:
        pickle.dump( [clf, count_vect, tfidf_transformer, ch2], ofile)

