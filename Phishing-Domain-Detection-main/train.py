from scipy.io import arff
import pandas as pd
import clean
import pickle

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

data = arff.loadarff("data/dataset.arff")
df = pd.DataFrame(data[0])

df = clean.cleanDataframe(df)

y = df['Result']
X = df.drop('Result', axis=1)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42)

# Classification and Regression Tree (CART)
classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

# Perceptron
prcp = Perceptron(max_iter=1000, eta0=0.005, random_state=0)
prcp.fit(X_train, y_train)
y_pred = prcp.predict(X_test)
#print(round(accuracy_score(y_test, y_pred)*100, 2))

#print(confusion_matrix(y_test, y_pred))
#print(classification_report(y_test, y_pred))

# Logistic Regression
lgst_reg = LogisticRegression()
lgst_reg.fit(X_train, y_train)
y_pred = lgst_reg.predict(X_test)
#print(round(accuracy_score(y_test, y_pred)*100, 2))

# Random Forest
rndm_frst = RandomForestClassifier(
    n_estimators=900, criterion='gini', random_state=0)
rndm_frst.fit(X_train, y_train)
y_pred = rndm_frst.predict(X_test)
print(round(accuracy_score(y_test, y_pred)*100, 2))

# Export this model to a pickle file
filename = 'model.sav'
pickle.dump(rndm_frst, open(filename, 'wb'))

results = pd.DataFrame({'Model': ['Logistic Regression',
                                  'Random Forest', 'Perceptron', 'CART']})
for i in range(5, 0, -1):
    col = "Split= " + str((10-i)*10) + ':' + str(i*10)
    tmp = []
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=i/10)
    lgst_reg.fit(X_train, y_train)
    y_pred = lgst_reg.predict(X_test)
    tmp.append(round(accuracy_score(y_test, y_pred.round())*100, 2))
    rndm_frst.fit(X_train, y_train)
    y_pred = rndm_frst.predict(X_test)
    tmp.append(round(accuracy_score(y_test, y_pred)*100, 2))
    prcp.fit(X_train, y_train)
    y_pred = prcp.predict(X_test)
    tmp.append(round(accuracy_score(y_test, y_pred.round())*100, 2))
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    tmp.append(round(accuracy_score(y_test, y_pred)*100, 2))
    results[col] = tmp

print(results)
