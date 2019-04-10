import os
import csv
import json

directory = "/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Data/Entertainment"

jsonData = []


for filename in os.listdir(directory):
    count = 0
    runningSum = 0

    if filename.endswith(".json") or filename.endswith(".py"):
         with open(os.path.join(directory, filename), 'r') as json_file:
             for review in json_file:
                 line = json.loads(review)
                 runningSum = runningSum + line["overall"]
                 count += 1
         average = runningSum / count
         jsonData.append({"Category" :filename[8:29], "Count" : count, "Average" : average })

with open('/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Output/'+directory[69:]+'.json', 'w') as outfile:
     json.dump(jsonData, outfile)
     print("Wrote to file")



