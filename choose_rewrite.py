import gensim

from bs4 import BeautifulSoup
import codecs
import sys
import re
import numpy as np

topic_filename=sys.argv[1]
soup = BeautifulSoup(codecs.open(topic_filename, "r"), "lxml")

def compareVectors(model, words1, words2, perc):
    scores = []
    for w1 in words1:
        if w1 not in model:
            continue

        for w2 in words2:
            if w2 not in model:
                continue

            if w1 != w2:
                scores += [model.similarity(w1, w2)]

    if len(scores) > 0:
        if perc > 0:
            return np.percentile(scores, perc)
        else:
            return np.mean(scores)
    return 0.0


model = gensim.models.KeyedVectors.load_word2vec_format('./GoogleNews-vectors-negative300.bin', binary=True)

strategy = "mean_word2vec"
#strategy = "80_word2vec"
#strategy = "fifo"
scores = {}
print "<topics>"
for topic in soup.find_all("topic"):

    num = int(topic.find("num").getText())
    desc = topic.find("desc").getText()
    query = topic.find("query").getText()
    cat = topic.find("cat").getText()

    scores[num] = []

    print "<topic num='%d'>" % (num)
    print "<cat>%s</cat>" % (cat)
    print "<query>%s</query>" % (query)
    print "<desc>%s</desc>" % (desc)

    print "<sections>"
    for result in topic.find_all("result"):
        #print "Wikipedia Page:", result.page.getText()
        fifo = 100

        for section in result.find_all("section"):
            if not section.secname:
                continue

            sec_name = section.secname.getText()
            sec_text = section.sectext.getText()
            #print "Sec: %s" % (sec_text)
            #print "Desc: %s" % (desc)
            #print "Score: ", score

            if strategy == "mean_word2vec":
                score = compareVectors(model, sec_text, desc, -1)
            elif strategy == "80_word2vec":
                score = compareVectors(model, sec_text, desc, 80)
            elif strategy == "fifo":
                fifo -= 1
                score = fifo

            scores[num].append([sec_name, score])

    for sec in sorted(scores[num], key=lambda x: x[1], reverse=True)[:5]:
        print "<section>%s</section>" % (sec[0])
    print "</sections>"
    print "</topic>"
print "</topics>"


