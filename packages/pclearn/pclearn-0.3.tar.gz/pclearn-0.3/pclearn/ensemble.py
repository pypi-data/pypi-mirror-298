import numpy as np
from sklearn import datasets
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.simplefilter("ignore")
iris = datasets.load_iris()
x,y = iris.data,iris.target
labels = ["Random Forest","Logistic Regression","GaussianNB","Decision Tree"]
m1 = RandomForestClassifier(random_state=42)
m2 = LogisticRegression(random_state=2)
m3 = GaussianNB()
m4 = DecisionTreeClassifier()
for m,label in zip([m1,m2,m3,m4],labels):
    scores = model_selection.cross_val_score(m,x,y,cv=10,scoring="accuracy")
    print(f"Accuracy: {scores.mean()} {label}")
voting_clf_hard = VotingClassifier(estimators=[(labels[0],m1),(labels[1],m2),(labels[2],m3),(labels[3],m4)],voting='hard')
voting_clf_soft = VotingClassifier(estimators=[(labels[0],m1),(labels[1],m2),(labels[2],m3),(labels[3],m4)],voting='soft')
scores1 = model_selection.cross_val_score(voting_clf_hard,x,y,cv=5,scoring="accuracy")
scores2 = model_selection.cross_val_score(voting_clf_soft,x,y,cv=5,scoring="accuracy")
print(f"Accuracy of the hard voting: {scores1.mean()}")
print(f"Accuracy of the soft voting: {scores2.mean()}")
