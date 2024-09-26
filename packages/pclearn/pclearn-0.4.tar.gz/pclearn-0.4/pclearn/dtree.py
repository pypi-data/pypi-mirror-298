import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn .model_selection import train_test_split 
from sklearn import metrics 
from matplotlib import pyplot as plt
from sklearn import tree

col_names = ['Reservation', 'Raining', 'BadService','Saturday','Result']
hoteldata = pd.read_csv("dtree.csv", header=None, names=col_names)
feature_cols = ['Reservation', 'Raining', 'BadService','Saturday']
X = hoteldata[feature_cols] 
y = hoteldata.Result 
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.3, random_state=1)
print(hoteldata)
print("x train data: ", X_train)
print("y train data: ",y_train)
print("x test data: ", X_test)
print("y test data: ",y_test)

clf = DecisionTreeClassifier(criterion="entropy", max_depth=5)
clf = clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
print("ytest = ", X_test)
print("ypred = ", y_pred)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
fig = plt.figure(figsize=(25,20))
t = tree.plot_tree(clf,feature_names=feature_cols,class_names=['Leave','Wait'],filled=True)
fig.savefig("decistion_tree.png")

