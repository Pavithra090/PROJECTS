import numpy as np
 import pandas as pd
 import warnings
 warnings.filterwarnings('ignore’)
 from sklearn.model_selection import train_test_split
 from sklearn import svm
 from sklearn.metrics
 import accuracy_score, precision_score, recall_score, f1_score
 heart_data = pd.read_csv('heart.csv’)
 heart_data.head()
 heart_data.info()
 heart_data.shape
 heart_data.describe().T
 heart_data['target'].value_counts()
 heart_data.groupby('target').mean()
 9
X = heart_data.drop(columns='target', axis=1)y = heart_data['target’]
 print(X)
 print(y)
 X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, stratify=y, 
random_state=2)print(X.shape, X_train.shape, X_test.shape)
 classifier = svm.SVC(kernel='linear’)
 classifier.fit(X_train, y_train)
 # Accuracy on train datatrain_pred = classifier.predict(X_train)
 acc = accuracy_score(y_train, train_pred) 
print("Training accuracy of SVM Model is {}".format(acc)) 
# Accuracy on test 
dataprediction = classifier.predict(X_test)
 acc = accuracy_score(y_test, prediction) 
print("Accuracy of SVM Model is {}".format(acc)) 
prec = precision_score(y_test, prediction) 
print("Precision of Model is {}".format(prec))  
rec = recall_score(y_test, prediction)
 print("Recall of Model is {}".format(rec)) 
f1 = f1_score(y_test, prediction)
 print("F1-Score of Model is {}".format(f1))
 10
# use any data instance from heart disease dataset
 input_data = (58, 1, 1, 160, 225, 1, 1, 146, 0, 2.8, 0, 2, 0)
 # changing the input_data to numpy array
 input_numpy_array = np.asarray(input_data)
 # reshape the array for predicting one instance  input_data_reshaped = 
input_numpy_array.reshape(1,-1)
 prediction=classifier.predict(input_data_reshaped)
 print("Predicted Label: ", prediction)
 if (prediction[0] == 0):   
print('The person does not have a heart disease’)
 else:   
print('The person have a heart disease')
