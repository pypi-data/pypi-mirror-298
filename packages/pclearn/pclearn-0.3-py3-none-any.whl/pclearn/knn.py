from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
dataset = load_iris()
x , y = dataset.data,dataset.target
knn = KNeighborsClassifier(n_neighbors = 5)
x_train , x_test , y_train , y_test = train_test_split(x,y , test_size =0.4,random_state = 42)
print(f"XTrain: {x_train}")
print(f"XTest: {x_test}")
print(f"yTrain: {y_train}")
print(f"y test:{y_test}")
knn.fit(x_train,y_train)
y_pred = knn.predict(x_test)
print(f"y_pred:{y_pred}")      
accuracy = metrics.accuracy_score(y_test,y_pred)
print(f"Accuracy :{round(accuracy*100,2)}%")
cm = metrics.confusion_matrix(y_test,y_pred)
print("Confusion Matrix")
print(cm)

