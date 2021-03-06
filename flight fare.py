# -*- coding: utf-8 -*-
"""B20CS046, Bonos project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kIb3eljzYd8jgo1qi_-Fa7MLLaivFLJJ
"""

from google.colab import drive
drive.mount('/content/drive')

from google.colab import files
uploaded=files.upload()

import pandas as pd

import IPython
import numpy as np
import wave
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sklearn
from sklearn.preprocessing  import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.compose import ColumnTransformer
from pandas.core.internals.managers import T

d=pd.read_csv(r"Dataset.xlsx - Sheet1.csv")
d.head()
d.shape

cat_cols = d.select_dtypes(include=['object']).columns.tolist()
cat_cols

t=list(d["Date_of_Journey"])
t
d["date"]=d["Date_of_Journey"]
d["month"]=d["Date_of_Journey"]
j=0
for i in range(d.shape[0]):
    d["date"][i]=d["date"][i].split('/')[0]
    d["month"][i]=d["month"][i].split('/')[1]
   
d.head()

d["dep_hr"]=pd.to_datetime(d["Dep_Time"]).dt.hour
d["dep_min"]=pd.to_datetime(d["Dep_Time"]).dt.minute

d["arrival_hr"]=pd.to_datetime(d["Arrival_Time"]).dt.hour
d["arrival_min"]=pd.to_datetime(d["Arrival_Time"]).dt.minute
#d.drop(["Arrival_Time"],axis=1,inplace=True)

duration = list(d["Duration"])

for i in range(len(duration)):
    if len(duration[i].split()) != 2:    # Check if duration contains only hour or mins
        if "h" in duration[i]:
            duration[i] = duration[i].strip() + " 0m"   # Adds 0 minute
        else:
            duration[i] = "0h " + duration[i]

#duration_hours = []
#duration_mins = []
#for i in range(len(duration)):
#    duration_hours.append(int(duration[i].split(sep = "h")[0]))    # Extract hours from duration
#    duration_mins.append(int(duration[i].split(sep = "m")[0].split()[-1]))

#d["duration_hours"] = duration_hours
#d["duration_mins"] = duration_mins

d["duration_hour"]=d["Duration"]
#d["duration_mins"]=d["Duration"]

for i in range(d.shape[0]):
    d["duration_hour"][i]=d["Duration"][i].split(sep = "h")[0]
#    d["duration_mins"][i]=d["Duration"][i].split(sep = "m")[0].split()[-1]
#d.drop(['duration_mins'],axis=1,inplace=True)

d.head()

"""#EDA"""

import seaborn as sb

plt.subplot(331)

d['Airline'].value_counts().plot(kind='bar', title='Airline ', figsize=(110,20))
plt.xticks(rotation=0)

sb.countplot(x='Source',data=d)

sb.countplot(x='Destination',data=d)

plt.subplot(331)

d['Additional_Info'].value_counts().plot(kind='bar', title='Additional_Info ', figsize=(110,20))
plt.xticks(rotation=0)

sb.countplot(x='Total_Stops',data=d)

plt.figure(figsize=(20,10))
sb.countplot(x='duration_hour',data=d)
plt.grid()

#plt.figure(figsize=(20,10))
#sb.countplot(x='duration_mins',data=d)
#plt.grid()

sb.countplot(x='date',data=d)

sb.countplot(x='month',data=d)

sb.displot(d['Price'],kde='False')

"""Comparision"""

import seaborn as sns

#fig, axes = plt.subplots(2,2, figsize=(50,9))
plt.figure(figsize=(30,10))
sns.boxplot( y="Price", x= "Airline", data=d, orient='v')
plt.figure(figsize=(30,10))
sns.boxplot( y="Price", x= "Destination", data=d, orient='v')
plt.figure(figsize=(30,10))
sns.boxplot( y="Price", x= "Source", data=d, orient='v' )
plt.figure(figsize=(30,10))
sns.boxplot( y="Price", x= "Total_Stops", data=d, orient='v')
plt.show()

plt.figure(figsize=(30,10))
sns.boxplot( y="Price", x= "duration_hour", data=d, orient='v')
plt.show()
#plt.figure(figsize=(30,10))
#sns.boxplot( y="Price", x= "duration_mins", data=d, orient='v')
#plt.show()

d['Date_of_Journey'].unique()

d['Dep_Time'].unique()

d['Duration'].unique()

print(d["Source"].unique())
print(d["Destination"].unique())

d.head()

d['Route'].unique()

#select categorical variables from then dataset, and then implement categorical encoding for nominal variables

t1=d[['Airline']]
t1=pd.get_dummies(t1, drop_first=True)

t2=d[['Source']]
t2=pd.get_dummies(t2, drop_first= True)

t3=d[['Destination']]
t3=pd.get_dummies(t3, drop_first= True)


# Concatenate dataset with Airline, Source, Destination, Additional_Info
d= pd.concat([d, t1, t2, t3], axis = 1)

l=LabelEncoder()
d['Route']=l.fit_transform(d['Route'])
d['Total_Stops']=l.fit_transform(d['Total_Stops'])
d['Additional_Info']=l.fit_transform(d['Additional_Info'])
d['number_stops']=d['Total_Stops']
d['route']=d['Route']
d['info']=d['Additional_Info']

d['Total_Stops'].unique()

#d["source"]=d["Source"]
##d.replace({"Banglore":1,"Kolkata":2,"Delhi":3,"Chennai":4,"Mumbai":5},inplace=True)
#d.head()
#d["destination"]=d["Destination"]
#d.replace({"Banglore":1,"Kolkata":2,"Delhi":3,"Chennai":4,"Mumbai":5,"New Delhi":6,"Cochin":7,"Delhi":8,"Hyderabad":9},inplace=True)

#d["journey_data"]=d["Date_of_Journey"] /////////////////////////
d.drop(["Airline"],axis=1,inplace=True)
d.drop(["Date_of_Journey"],axis=1,inplace=True)
d.drop(["Source"],axis=1,inplace=True)
d.drop(["Destination"],axis=1,inplace=True)
d.drop(["Route"],axis=1,inplace=True)
d.drop(["Dep_Time"],axis=1,inplace=True)
d.drop(["Duration"],axis=1,inplace=True)
d.drop(["Total_Stops"],axis=1,inplace=True)
d.drop(["Arrival_Time"],axis=1,inplace=True)
d.drop(["Additional_Info"],axis=1,inplace=True)

d.head()

x=d.iloc[:,1:]
y=d.iloc[:,0]
x.isna().sum()

d.info()

c=d.select_dtypes(include=['object']).columns.tolist()
c
#for i in c:
#  d[i]=d[i].astype(str).astype(int)
for i in c:
  #l=LabelEncoder()
  d[i]=l.fit_transform(d[i])
  #d[i]=d[i].astype(str)#.astype(int)
d.head()

x=d.iloc[:,1:]
y=d.iloc[:,0]
#x.isna().sum()

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=10)
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

"""#Modules"""

# Importing different models

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBClassifier

from pandas.core.strings.accessor import forbid_nonstring_types
import IPython
import pandas as pd
import numpy as np
import matplotlib.pyplot as mp
import sklearn
from sklearn.preprocessing  import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.compose import ColumnTransformer
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis 
from sklearn import datasets
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import impute 

#import libraries
import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_breast_cancer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.metrics import plot_roc_curve, plot_confusion_matrix,classification_report
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import mean_squared_error

"""#KNN means"""

from sklearn.preprocessing import StandardScaler
s = StandardScaler()
x_train = s.fit_transform(x_train)
x_test = s.transform(x_test)

"""Grid search to get best value of k"""

# Commented out IPython magic to ensure Python compatibility.
#import required packages
from sklearn import neighbors
from sklearn.metrics import mean_squared_error 
from math import sqrt
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.model_selection import GridSearchCV
params = {'n_neighbors':[2,3,4,5,6,7,8,9]}

knn = neighbors.KNeighborsRegressor()

m = GridSearchCV(knn, params, cv=5)
m.fit(x_train,y_train)
m.best_params_

from sklearn.neighbors import KNeighborsClassifier
knc = KNeighborsClassifier(n_neighbors = 3)
knc.fit(x_train, y_train)
knc

# Predicting the Test set results
y_pred1 = knc.predict(x_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix, accuracy_score
conf = confusion_matrix(y_test, y_pred1)
accu1 = accuracy_score(y_test, y_pred1)
print("confusion matrix:",conf)
print("accuracy:",accu1*100)

from sklearn.metrics import f1_score
f1=f1_score(y_test,y_pred1 ,average='macro')
print("f1_score:",f1)

from sklearn.metrics import classification_report, confusion_matrix  
print(classification_report(y_test, y_pred1))

mse1 =mean_squared_error(y_test,y_pred1)
print('MSE : ',mse1)
r2_1= metrics.r2_score(y_test, y_pred1)
print('r2_score :',r2_1)
rmse1=np.sqrt(mean_squared_error(y_test,y_pred1))
print('RMSE : ', rmse1)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib.pyplot as plt

"""#Linear regression"""

from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import mean_squared_error
kfold = StratifiedKFold(n_splits=20)

#Linear Regression
from sklearn.linear_model import LinearRegression
lr=LinearRegression()
lr.fit(x_train, y_train)
y_pred2=lr.predict(x_test)

#training score
print("Linear Regression Score for training set ",lr.score(x_train, y_train))
#test score
print("Linear Regression Score for test Set ",lr.score(x_test, y_test))

acc = cross_val_score(lr, x_train, y_train, cv = kfold)
#print(accuracies)
print("Accuracy: {:.2f} %".format(acc.mean()*100))

mse2 =mean_squared_error(y_test,y_pred2)
print('MSE : ',mse1)
r2_2= metrics.r2_score(y_test, y_pred2)
print('r2_score :',r2_2)
rmse2=np.sqrt(mean_squared_error(y_test,y_pred2))
print('RMSE : ', rmse2)

"""#Decision tree classifier"""

from sklearn.tree import DecisionTreeRegressor

dt = DecisionTreeRegressor(random_state=44)
dt.fit(x_train, y_train)
y_pred3 = dt.predict(x_test)

from sklearn.tree import plot_tree
plt.figure(figsize=(50,15), dpi=150)
plot_tree(dt, feature_names=x.columns);

#Training Accuracy
print("Decision Tree Score on Training set is",dt.score(x_train, y_train))
#Testing Accuracy
print("Decision Tree Score on Test Set is",dt.score(x_test, y_test))

acc3 = cross_val_score(dt, x_train, y_train, cv = kfold)
#print(acc)
print("Accuracy: {:.2f} %".format(acc3.mean()*100))
print("Standard Deviation: {:.2f} %".format(acc3.std()*100))

mse3 =mean_squared_error(y_test,y_pred3)
print('MSE : ',mse3)
r2_3= metrics.r2_score(y_test, y_pred3)
print('r2_score:',r2_3)
rmse3=np.sqrt(mean_squared_error(y_test,y_pred3))
print('RMSE : ', rmse3)

"""#Random regression model"""

from sklearn.ensemble import RandomForestRegressor
 
 # create regressor object
rg = RandomForestRegressor(n_estimators = 100, random_state = 0)
 
# fit the regressor with x and y data
rg.fit(x_train, y_train)

y_pred4 = rg.predict(x_test)
y_pred4

acc4 = cross_val_score(dt, x_train, y_train, cv = kfold)
#print(acc)
print("Accuracy: {:.2f} %".format(acc4.mean()*100))
print("Standard Deviation: {:.2f} %".format(acc4.std()*100))

mse4 =mean_squared_error(y_test,y_pred4)
print('MSE : ',mse4)
r2_4= metrics.r2_score(y_test, y_pred4)
print('r2_score:',r2_4)
rmse4=np.sqrt(mean_squared_error(y_test,y_pred4))
print('RMSE : ', rmse4)

"""Model comparission"""

x = ['knc','lr','dt','rg']
from sklearn.metrics import accuracy_score as ac
from sklearn.metrics import precision_score as ps
from sklearn.metrics import recall_score as rs

y1 = [np.sqrt(mean_squared_error(y_test,y_pred1)),np.sqrt(mean_squared_error(y_test,y_pred2)),np.sqrt(mean_squared_error(y_test,y_pred3)),np.sqrt(mean_squared_error(y_test,y_pred4))]


plt.plot(x,y1,color = 'red', marker = 'o', label = ' Root mean square error')


plt.legend(loc = "best")
plt.ylim(1500,3250)

from matplotlib.pyplot import figure
plt.rcParams['figure.figsize'] = [10,10]

plt.show()

x = ['knn','linear reg','decision tree','random reg']
y2 = [mean_squared_error(y_test,y_pred1),mean_squared_error(y_test,y_pred2),mean_squared_error(y_test,y_pred3),mean_squared_error(y_test,y_pred4)]
plt.plot(x,y2,color = 'red', marker = 'o', label = ' mean square error')


plt.legend(loc = "best")
plt.ylim(2700000,10000000)

from matplotlib.pyplot import figure
plt.rcParams['figure.figsize'] = [10,10]

plt.show()

y3 = [metrics.r2_score(y_test, y_pred1),metrics.r2_score(y_test, y_pred2),metrics.r2_score(y_test, y_pred3),metrics.r2_score(y_test, y_pred4)]
#y4 = [f1_score(y_test, y_pred1),accuracy_score(y_test, y_pred2),accuracy_score(y_test, y_pred3),accuracy_score(y_test, y_pred4) ]
plt.plot(x,y3,color = 'red', marker = 'o', label = ' r2 score')
#plt.plot(x,y3,color = 'blue', marker = 'o', label = 'Accuracy')

plt.legend(loc = "best")
plt.ylim(0.5,1)

from matplotlib.pyplot import figure
plt.rcParams['figure.figsize'] = [10,10]

plt.show()


#metrics.r2_score(y_test, y_pred1)