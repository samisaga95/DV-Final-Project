import os
import csv
import json

rowSize =2
directory = "/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Data"

with open('/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Output/data.csv', mode='w') as file:
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    file_writer.writerow(['row', 'column', 'dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average'])

i = 1
j = 1
for filename in os.listdir(directory):
    if j==rowSize+1:
        i += 1
        j = 1
    if filename.endswith(".json") or filename.endswith(".py"):
         count5 = 0
         count4 = 0
         count3 = 0
         count2 = 0
         count1 = 0

         runningSum = 0

         with open(os.path.join(directory, filename), 'r') as json_file:
             for review in json_file:
                 line = json.loads(review)
                 runningSum = runningSum + line["overall"]
                 if line["overall"] == 1:
                     count1+=1
                 if line["overall"] == 2:
                     count2+=1
                 if line["overall"] == 3:
                     count3+=1
                 if line["overall"] == 4:
                     count4+=1
                 if line["overall"] == 5:
                     count5+=1
             average = runningSum / (count1+count2+count3+count4+count5)

         with open('/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Output/data.csv',
                  mode='a') as file:
             file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

             file_writer.writerow([i,j,"",filename[8:-7], count5, count4, count3, count2, count1, (count1+count2+count3+count4+count5), average, "",""])
             j += 1



