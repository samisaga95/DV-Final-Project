import glob
from textblob import TextBlob
import json
import codecs
import pandas as pd
from collections import defaultdict


mylist = [f for f in glob.glob("*.JSON")]
# mylist = ['Baby_5.json']
list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

dictionary = []
sentiment = []
defdict = defaultdict(int)
sentimentDict = {}
overallDict ={}
wordReviews ={}
summaryReviews ={}
productIDS = {}
defdict = defaultdict(int)

dictionary_filename = 'dictionary.csv'
df = pd.read_csv(dictionary_filename, names=['Words'])
dic = df['Words']
for d in dic:
    dictionary.append(d)

for file in mylist:
    sentiment = []
    defdict_positive = defaultdict(int)
    defdict_negative = defaultdict(int)

    sentimentDict_positive = {}
    sentimentDict_negative = {}
    overallDict = {}
    wordReviews_positive = {}
    wordReviews_negative = {}
    ratings_positive = {}
    ratings_negative = {}
    summaryReviews = {}
    productIDS_positive = {}
    productIDS_negative = {}
    defdict = defaultdict(int)
    print "*****************************running "+file
    counter = 1
    counter_positive = 0
    counter_negative = 0
    with codecs.open(file,'rU','utf-8') as f:
        for line in f:
            print "+: "+str(counter_positive)+" , - : "+str(counter_negative)
            l = json.loads(line)
            analysis = TextBlob(l["reviewText"])
            polarity = analysis.sentiment.polarity
            if polarity > 0:
                counter_positive +=1

                for word in l["reviewText"].split():
                    if word.upper() in dictionary:
                        if word.lower() not in list:
                            defdict_positive[word] += 1
                            if word not in sentimentDict_positive:
                                sentimentDict_positive[word] = polarity
                            else:
                                sentimentDict_positive[word] += polarity
                            if word not in wordReviews_positive:
                                wordReviews_positive[word] = [l["reviewText"]]
                                productIDS_positive[word] = [l["asin"]]
                                ratings_positive[word] = [l["overall"]]
                            else:
                                if len(wordReviews_positive[word]) < 5:
                                    if l["reviewText"] not in wordReviews_positive[word]:
                                        wordReviews_positive[word].append(l["reviewText"])
                                        productIDS_positive[word].append(l["asin"])
                                        ratings_positive[word].append(l["overall"])
            if polarity < 0:
                counter_negative +=1

                for word in l["reviewText"].split():
                    if word.upper() in dictionary:
                        if word.lower() not in list:
                            defdict_negative[word] += 1
                            if word not in sentimentDict_negative:
                                sentimentDict_negative[word] = polarity
                            else:
                                sentimentDict_negative[word] += polarity
                            if word not in wordReviews_negative:
                                wordReviews_negative[word] = [l["reviewText"]]
                                productIDS_negative[word] = [l["asin"]]
                                ratings_negative[word] = [l["overall"]]
                            else:
                                if len(wordReviews_negative[word]) < 5:
                                    if l["reviewText"] not in wordReviews_negative[word]:
                                        wordReviews_negative[word].append(l["reviewText"])
                                        productIDS_negative[word].append(l["asin"])
                                        ratings_negative[word].append(l["overall"])


    count_positive = 0
    dat = []
    for w in sorted(defdict_positive, key=defdict_positive.get, reverse=True):
        count_positive+=1
        # print w, defdict[w], sentimentDict[w]/defdict[w], wordReviews[w]
        output = {}
        output["word"] = w
        output["frequency"] = defdict_positive[w]
        output["sentiment"] = sentimentDict_positive[w]/defdict_positive[w]
        output["topReviews"] = wordReviews_positive[w]
        output["productIDS"] = productIDS_positive[w]
        output["ratings"] = ratings_positive[w]
        dat.append(output)
        if count_positive == 20:
            break
    count_negative =0
    for w in sorted(defdict_negative, key=defdict_negative.get, reverse=True):
        count_negative+=1
        # print w, defdict[w], sentimentDict[w]/defdict[w], wordReviews[w]
        output = {}
        output["word"] = w
        output["frequency"] = defdict_negative[w]
        output["sentiment"] = sentimentDict_negative[w]/defdict_negative[w]
        output["topReviews"] = wordReviews_negative[w]
        output["productIDS"] = productIDS_negative[w]
        output["ratings"] = ratings_negative[w]
        dat.append(output)
        if count_negative == 10:
            break

    with open('output_'+file, 'w') as fout:
        json.dump(dat , fout)





