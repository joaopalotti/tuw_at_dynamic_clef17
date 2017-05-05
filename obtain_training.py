from trectools import TrecQrel
from elasticsearch import Elasticsearch, NotFoundError
import os
import codecs

es = Elasticsearch(["40.68.209.241:9200"])
qrels = TrecQrel("./data/clef-dynamic-topic-subset-click-data.txt")

nmissing = 0
npages = 0

for topic in qrels.topics():
    if not os.path.exists(os.path.join("data", "topic%d" % (topic))):
        os.makedirs(os.path.join("data", "topic%d" % (topic)))
        os.makedirs(os.path.join("data", "topic%d" % (topic), "pos"))
        os.makedirs(os.path.join("data", "topic%d" % (topic), "neg"))

    for docid in qrels.get_document_names_for_topic(topic):
        npages += 1

        print "Downloading %s" % (docid)
        try:
            r = es.get(index="clueweb12_docs", id=docid)
        except NotFoundError:
            print "Missing: %s"% (docid)
            nmissing += 1
            continue

        if qrels.get_judgement(docid, topic):
            outpath = os.path.join("data", "topic%d" % (topic), "pos", docid)
        else:
            outpath = os.path.join("data", "topic%d" % (topic), "neg", docid)

        content = r["_source"]["title"].strip() + " " + r["_source"]["body"].strip()
        print "Saving doc in %s" % (outpath)
        with codecs.open(outpath, "w", encoding="utf-8") as f:
            f.write(content)

print "Total missing files is %d out of %d" % (nmissing, npages)

