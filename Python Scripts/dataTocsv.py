import os
import csv
import json

directory = "/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Data/Entertainment"

with open('/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Output/'+ directory[69:] +'.csv', mode='w') as file:
    file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    file_writer.writerow(['Category', 'Count', 'Average'])


for filename in os.listdir(directory):
    if filename.endswith(".json") or filename.endswith(".py"):
         count = 0
         runningSum = 0

         with open(os.path.join(directory, filename), 'r') as json_file:
             for review in json_file:
                 line = json.loads(review)
                 runningSum = runningSum + line["overall"]
                 count += 1
             average = runningSum / count
             print (average)

         with open('/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Output/' + directory[69:] + '.csv',
                  mode='a') as file:
             file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

             file_writer.writerow([filename[8:29], count, average])


