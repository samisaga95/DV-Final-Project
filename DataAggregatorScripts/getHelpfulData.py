import glob

import json
import codecs


mylist = [f for f in glob.glob("*.JSON")]
list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

for file in mylist:
    help_1 = []
    help_2 = []
    help_3 = []
    help_4 = []
    help_5 = []
    counter_1 = 0
    counter_2 = 0
    counter_3 = 0
    counter_4 = 0
    counter_5 = 0
    counter = 0
    with codecs.open(file,'rU','utf-8') as f:
        for line in f:
            print str(counter) + ", 1 : "+str(counter_1) +" , 2 : "+str(counter_2)+" , 3 : "+str(counter_3)+" , 4 : "+str(counter_4)+" , 5 :"+str(counter_5)
            counter +=1
            # if counter_1 >= 5 and counter_2  >=5 and counter_3 >= 5 and counter_4 >=5 and counter_5 >= 5:
            #     break
            l = json.loads(line)
            print l;
            help = l["helpful"]
            print help

            if int(help[0]) == 0:
                continue
            if float(l["overall"]) == 1:
                counter_1+=1
                help_1.append([l["reviewText"],l["asin"],float(float(help[0])/float(help[1]))])
            if  float(l["overall"]) == 2:
                counter_2 += 1
                help_2.append([l["reviewText"],l["asin"],float(float(help[0])/float(help[1]))])
            if float(l["overall"]) == 3:
                counter_3 += 1
                help_3.append([l["reviewText"],l["asin"],float(float(help[0])/float(help[1]))])
            if  float(l["overall"]) == 4:
                counter_4 += 1
                help_4.append([l["reviewText"],l["asin"],float(float(help[0])/float(help[1]))])
            if float(l["overall"]) == 5:
                counter_5 += 1
                help_5.append([l["reviewText"],l["asin"],float(float(help[0])/float(help[1]))])


    help_1.sort(key = lambda x: x[2])
    help_2.sort(key = lambda x: x[2])
    help_3.sort(key = lambda x: x[2])
    help_4.sort(key = lambda x: x[2])
    help_5.sort(key = lambda x: x[2])
    dat = []
    output = {}

    output["review_1"] = [help_1[0][0],help_1[1][0],help_1[2][0],help_1[3][0]]
    output["review_2"] = [help_2[0][0],help_2[1][0],help_2[2][0],help_2[3][0]]
    output["review_3"] = [help_3[0][0],help_3[1][0],help_3[2][0],help_3[3][0]]
    output["review_4"] = [help_4[0][0],help_4[1][0],help_4[2][0],help_4[3][0]]
    output["review_5"] = [help_5[0][0],help_5[1][0],help_5[2][0],help_5[3][0]]

    output["product_1"] = [help_1[0][1],help_1[1][1],help_1[2][1],help_1[3][1]]
    output["product_2"] = [help_2[0][1],help_2[1][1],help_2[2][1],help_2[3][1]]
    output["product_3"] = [help_3[0][1],help_3[1][1],help_3[2][1],help_3[3][1]]
    output["product_4"] = [help_4[0][1],help_4[1][1],help_4[2][1],help_4[3][1]]
    output["product_5"] = [help_5[0][1],help_5[1][1],help_5[2][1],help_5[3][1]]

    output["score_1"] = [help_1[0][2],help_1[1][2],help_1[2][2],help_1[3][2]]
    output["score_2"] = [help_2[0][2],help_2[1][2],help_2[2][2],help_2[3][2]]
    output["score_3"] = [help_3[0][2],help_3[1][2],help_3[2][2],help_3[3][2]]
    output["score_4"] = [help_4[0][2],help_4[1][2],help_4[2][2],help_4[3][2]]
    output["score_5"] = [help_5[0][2],help_5[1][2],help_5[2][2],help_5[3][2]]

    dat.append(output)

    with open('help_'+file, 'w') as fout:
        json.dump(dat , fout)
