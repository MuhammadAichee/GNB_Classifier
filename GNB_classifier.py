import pandas as pd
import numpy as np
import xlrd 
import math
  
def Col_max_min(sheet):
    minarray=[]
    maxarray=[]
    maximum =-99999
    minimum =99999
    for j in range(sheet.ncols):    
        maximum=-9999
        minimum=9999
        for i in range(sheet.nrows):
            if(sheet.cell_value(i, j)<minimum):
                minimum=sheet.cell_value(i, j)
            if(sheet.cell_value(i, j)>maximum):
                maximum=sheet.cell_value(i, j)     
        maxarray.append(maximum)
        minarray.append(minimum)
    return (maxarray,minarray)

def find_labels(sheet,no_of_rows,no_of_col):
    labels=[]
    for i in range(sheet.nrows): 
        if(sheet.cell_value(i, no_of_col-1) not in labels):
            labels.append(sheet.cell_value(i, no_of_col-1))
    return labels

def feature_scaling(sheet,minarray,maxarray,no_of_rows,no_of_col):
    for j in range((sheet.ncols)-1):    
        array=[]
        for i in range(sheet.nrows):
            val=0
            # print("index: ",i,j," ",sheet.cell_value(i, j)," ",minarray[j]," ",maxarray[j])
            val=(sheet.cell_value(i, j)-minarray[j])/(maxarray[j]-minarray[j])
            array.append(val)
        data[j]=array    
    array=[]    
    for i in range(sheet.nrows): 
        array.append(sheet.cell_value(i, no_of_col-1))
    data[no_of_col-1]=array
    return (data)

def label_count(data,no_of_rows,no_of_col,labels):
    count_labels=[]
    for i in range(len(labels)):
        count_labels.append(data[no_of_col-1][data[no_of_col-1] == labels[i]].count())
    return count_labels

def prior_probabilities(count_labels,total):
    prior=[]
    for i in range(len(labels)):
        prior.append(count_labels[i]/total)
    return prior

def formula(value, mean, variance):
    probabilty = (1/(math.sqrt(2*math.pi*variance))) * math.exp((-(math.pow(value-mean,2)))/(2*variance)) 
    return probabilty

# defining path
loc = ("parktraining.xlsx")

# opening and reading file
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0)

# no of columns 
no_of_col=sheet.ncols

# print(no_of_col)
# no of rows
no_of_rows=sheet.nrows

# print(no_of_rows)
# defining data frames  
data=pd.DataFrame()

# calculating minimum and maximum of each column
maxarray,minarray=Col_max_min(sheet)
# print("Maximum of Each column")
# print(maxarray)
# print("Minimum of Each column")
# print(minarray)
# finding labels
labels=find_labels(sheet,no_of_rows,no_of_col)
labels.sort()
# print("Labels: ",labels)

# labels=[0.0,1.0]
# feature scaling
data=feature_scaling(sheet,minarray,maxarray,no_of_rows,no_of_col)
# print(data)

# finding grouped mean
# data=data.groupby(no_of_col-1)
# print(data)
array=[]
data_means = data.groupby(no_of_col-1).mean()
print("Means")
print(data_means)
# for j in range(no_of_col-1):
#     print(j,data_means[j][0.0])
# for j in range(no_of_col-1):
#     print(j,data_means[j][1.0])    
# finding grouped variance

data_variance = data.groupby(no_of_col-1).var()
print("Variance")
print(data_variance)

# calculating label count
count_labels=label_count(data,no_of_rows,no_of_col,labels)

# print(count_labels)
# calculating total rows
total=data[no_of_col-1].count()

# print(total)  
# calculating prior probabilities
prior=prior_probabilities(count_labels,total)
print("\nPrior Probabilties of each label: ",prior)    
loc_testing = ("parktesting.xlsx")

# opening and reading file
wb = xlrd.open_workbook(loc_testing) 
sheet_testing = wb.sheet_by_index(0)  
no_of_col_testing=sheet_testing.ncols
# print(no_of_col_testing)

# no of rows
no_of_rows_testing=sheet_testing.nrows
maxarray_testing,minarray_testing=Col_max_min(sheet_testing)
data_testing=pd.DataFrame()

for j in range((sheet_testing.ncols)-1):    
    array=[]
    # print("index: ",j)
    for i in range(sheet_testing.nrows):
        val=0
        val=(sheet_testing.cell_value(i, j)-minarray_testing[j])/(maxarray_testing[j]-minarray_testing[j])
        # print(sheet_testing.cell_value(i, j),minarray_testing[j],maxarray_testing[j]," = ",val)
        array.append(val)
    data_testing[j]=array    

# array=[]    
# for i in range(sheet_testing.nrows): 
#     array.append(sheet_testing.cell_value(i, no_of_col_testing-1))
# data_testing[no_of_col_testing-1]=array
# print(data_testing)
Answer=[]
TotalAnswers=[]

#for all rows
for i in range((sheet_testing.nrows)):    
    Answer=[]
    # val=1
    #for all classess
    for k in range(len(labels)):
        val=1
        # for all columns
        for j in range((sheet_testing.ncols)-1):
            #multiplying partial probablities
            val=val*formula(data_testing[j][i],data_means[j][k],data_variance[j][k])
        value=val*prior[k]
        # print(prior[k],value,val)
        Answer.append(value)
    # normalizing
    Answer[:]=[x/sum(Answer) for x in Answer]    
    new=max(Answer)
    #all probabalities
    # print("index:  ",i," ",Answer,"  Sum of Probabilties: ",sum(Answer))    
    index=Answer.index(new)
    TotalAnswers.append(labels[index])    

count=0
print("\nFinal Output\n")
for i in range(len(TotalAnswers)):
    print("Index: ",i," ", "Predicted: ",TotalAnswers[i]," Actual: ",sheet_testing.cell_value(i, no_of_col_testing-1),end="\n")
    count=count+1

count=0

for i in range(no_of_rows_testing):
    if(sheet_testing.cell_value(i, no_of_col_testing-1)==TotalAnswers[i]):
       count=count+1
        
eff=(count/no_of_rows_testing)
print("Accuracy: ",eff*100,"%")  
