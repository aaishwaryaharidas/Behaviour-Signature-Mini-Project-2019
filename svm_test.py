import  os
import  gc
import numpy as np
import  csv

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import svm
def list_to_csv(datas,path):
    import csv
    with open(path + "/keystrokes.csv", "a+") as my_csv:
        csvWriter = csv.writer(my_csv, delimiter=',')
        csvWriter.writerows(datas)
        del csvWriter;

def save_csv(data,path):
    f = open(path + "/keystrokes.csv", "a+")
    f.write(data + os.linesep)  # Give your csv text here.

    f.close()

def test(path, datas):
    # Read dataset to pandas dataframe
    import pandas as pd
    clf = svm.SVC(kernel='linear')  # Linear Kernel
    dataset = pd.read_csv(path, header=None)
    print('all data')
    print(dataset)
    X = dataset.iloc[:, 0:360].values
    y = dataset.iloc[:, -1].values
    print(X)
    print(y)
    # print('all data')
    # print(X)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    # scaler = StandardScaler()
    # scaler.fit(X_train)
    #
    # X_train = scaler.transform(X_train)
    # X_test = scaler.transform(X_test)
    # # Create a svm Classifier
    # clf = svm.SVC(kernel='linear')  # Linear Kernel
    #
    # # Train the model using the training sets
    # print("Train data")
    # print(X_train)
    # print(np.unique(y_train))
    clf.fit(X, y)

    # Predict the response for test dataset
    print("before prediction :")
    y_pred = clf.predict(datas)

    del pd;
    print("prediction :" + y_pred)
    return y_pred

import math

def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

# names = ['flytime', 'dweltime', 'avgTL', 'avgDur', 'Class']
# path = r"C:\Users\sujit\Desktop\test\keystrokes.csv";
# #
# print(test(path,[[200.65722222110102,0.06277777777777777,62.77777777777778,59020305945697290]]))

