 # Importing Necessary Modules
import pandas as pd
import numpy as np
import openpyxl

#Reading Emp_Details.txt
with open("Emp_Details.txt") as textFile1:
    lines1 = np.array([line.strip().split() for line in textFile1])

titles1 = lines1[0]
data1 = np.delete(lines1, 0, 0)


#Reading Emp_Master.txt
with open("Emp_Master.txt") as textFile2:
    lines2 = np.array([line.strip().split() for line in textFile2])

titles2 = lines2[0]
data2 = np.delete(lines2, 0, 0)


#Defining Datatypes as per columns
convert_dict1 = {'EmpdID': int, 
                'Name': str,
                'LOC': str,
                'Phone': int
               }

convert_dict2 = {'EmpdID': int, 
                'Dept': str,
                'Sal': float
               }


#Converting Numpy array to Pandas Dataframe
df1 = pd.DataFrame(data1, columns=titles1)
df2 = pd.DataFrame(data2, columns=titles2)


#Chaning datatypes as per Convert_Dict
df1 = df1.astype(convert_dict1)
df2 = df2.astype(convert_dict2)


#Dropping rows if it contains any NaN (Missing data or blank data)
df1.dropna(inplace=True)
df2.dropna(inplace=True)

#Printing datasets for data observations
print(df1)
print(df2)



#########################################
## EX1 Employee who didnt get Dept yet ##
#########################################

ex1 = df1.merge(df2,indicator = True, how='left').loc[lambda x : x['_merge']!='both']

print("Employee who didnt get a Dept yet:\n")

print(ex1[['EmpdID', 'Name']])

# Writing fetched data to file
ex1[['EmpdID', 'Name']].to_excel('ex1_emp_without_dept.xlsx', index=False)



#################################################
## EX2 Dept which is drawing the highest Salary #
#################################################

maxid = df2['Sal'].idxmax()

print("Dept which is Drawing highest salary\n")

print(df2.iloc[maxid:maxid+1][['Dept','Sal']])

# Writing fetched data to file
df2.iloc[maxid:maxid+1][['Dept','Sal']].to_excel("ex2A_highest_sal_one_dept.xlsx", index=False)



#############################
## EX2 Avg Sal of Each Dept #
#############################

avg_sal = df2.groupby(by="Dept").mean().astype(np.float32)

print(avg_sal[['Sal']])

# Writing fetched data to file
avg_sal['Sal'].to_excel('ex2B_avgsal_eachdept.xlsx')
 


####################################################################
## Give name and mno of employee with highest salary for each dept #
#################################################################### 

df1_df2_merged = df1.merge(df2).copy()

idx = df1_df2_merged.groupby(['Dept'])['Sal'].transform(max) == df1_df2_merged['Sal']

print("Name and Mobile numbers of employees who are drawing the highest salaries in each department:\n")

print(df1_df2_merged[idx])

# Writing fetched data to file
df1_df2_merged[idx].to_excel('ex3_highest_sal_all_dept.xlsx', index=False)