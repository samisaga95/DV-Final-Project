import glob
from textblob import TextBlob
import json
import codecs
import pandas as pd
from collections import defaultdict

mylist = [f for f in glob.glob("*.JSON")]
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
    defdict = defaultdict(int)
    sentimentDict = {}
    overallDict = {}
    wordReviews = {}
    summaryReviews = {}
    productIDS = {}
    defdict = defaultdict(int)

    print "*****************************running "+file
    counter = 1
    with codecs.open(file,'rU','utf-8') as f:
        for line in f:
            print counter
            if counter == 1000:
                break
            counter = counter +1
            l = json.loads(line)
            analysis = TextBlob(l["reviewText"])
            polarity = analysis.sentiment.polarity
            for word in l["reviewText"].split():
                if word.upper() in dictionary:
                    if word.lower() not in list:
                        defdict[word]+=1
                        if word not in sentimentDict:
                            sentimentDict[word] = polarity
                        else:
                            sentimentDict[word]+=polarity
                        if word not in wordReviews:
                            wordReviews[word] = [l["reviewText"]]
                            productIDS[word] = [l["asin"]]
                        else:
                            if len(wordReviews[word]) < 5:
                                if l["reviewText"] not in wordReviews[word]:
                                    wordReviews[word].append(l["reviewText"])
                                    productIDS[word].append(l["asin"])
    count = 0
    dat = []
    for w in sorted(defdict, key=defdict.get, reverse=True):
        count+=1
        # print w, defdict[w], sentimentDict[w]/defdict[w], wordReviews[w]
        output = {}
        output["word"] = w
        output["frequency"] = defdict[w]
        output["sentiment"] = sentimentDict[w]/defdict[w]
        output["topReviews"] = wordReviews[w]
        output["productIDS"] = productIDS[w]
        dat.append(output)
        if count == 50:
            break

    with open('output_'+file, 'w') as fout:
        json.dump(dat , fout)





