import pandas as pd

data = pd.read_csv("/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Output/data.csv")
constData = data[['row', 'column']]


# Finding value of rank_average
data1 = data[['dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']]
data1 = data1.sort_values(by=['average'], ascending=False)
data1 = data1.reset_index()
data = pd.concat([constData,data1], axis=1, ignore_index=True)
data = data.drop(data.columns[[2]], axis =1)
data.columns = ['row', 'column', 'dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']
data.rank_average = [i+1 for i in range(data.shape[0])]

# Finding value of rank_average
data1 = data[['dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']]
data1 = data1.sort_values(by=['count'], ascending=False)
data1 = data1.reset_index()
data = pd.concat([constData,data1], axis=1, ignore_index=True)
data = data.drop(data.columns[[2]], axis =1)
data.columns = ['row', 'column', 'dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']
data.rank_total = [i+1 for i in range(data.shape[0])]
print (data)



# Sorting according to name
data1 = data[['dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']]
data1 = data1.sort_values(by=['department'], ascending=True)
data1 = data1.reset_index()
data1 = pd.concat([constData,data1], axis=1, ignore_index=True)
data1 = data1.drop(data1.columns[[2]], axis =1)
data1.columns = ['row', 'column', 'dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']
print (data1)
data1.to_csv('/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Sample Visualisations/dataName.csv',index=False)

# Sorting according to average
data1 = data[['dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']]
data1 = data1.sort_values(by=['rank_average'], ascending=True)
data1 = data1.reset_index()
data1 = pd.concat([constData,data1], axis=1, ignore_index=True)
data1 = data1.drop(data1.columns[[2]], axis =1)
data1.columns = ['row', 'column', 'dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']
print (data1)
data1.to_csv('/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Sample Visualisations/dataAverage.csv',index=False)

# Sorting according to total
data1 = data[['dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']]
data1 = data1.sort_values(by=['rank_total'], ascending=True)
data1 = data1.reset_index()
data1 = pd.concat([constData,data1], axis=1, ignore_index=True)
data1 = data1.drop(data1.columns[[2]], axis =1)
data1.columns = ['row', 'column', 'dept','department','Star5','Star4','Star3','Star2','Star1','count','average','rank_total','rank_average']
print (data1)
data1.to_csv('/Users/santoshkumaramisagadda/Desktop/Acads/DV/DV Final Project/Sample Visualisations/dataTotal.csv',index=False)






