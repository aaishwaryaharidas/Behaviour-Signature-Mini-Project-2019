"""
feature 1 (avgTime):calculates average time between moves
feature 2 (avgSpeed):calculates a value similar to average speed of user moves
feature 3 (TimeSpent):calculates time duration user spends online
feature 4 (avgMoves):calculates avg number of by mouse movements per second
feature 5 (avgx):avg x coordinate of mouse pointer
feature 6 (avgy):avg y coordinate of mouse pointer
feature 7 (numberOfClicks):number of mouse clicks in the session
feature 8 (drags):number of mouse drags in the session
"""
from IPython.display import display, HTML
import pandas as pd
# For now only 8 naive features have been extracted for now, more features to be added and the existing ones are to
# be improved.

FileList = ["session_0041905381", "session_1060325796", "session_3320405034", "session_3826583375",
            "session_6668463071", "session_8961330453", "session_9017095287"]

# FileList=["session_0041905381"]
import numpy as np

featureVector = [None] * 8

for fileName in FileList:

    data = np.genfromtxt("user7/" + fileName, dtype=None, delimiter=',')
    data = data[1:]
    rows = data.shape[0]
    avgSpeed = 0
    meanx = 0
    meany = 0
    numberOfClicks = 0
    drags = 0
    TimeSpent = data[rows - 1, 0].astype(np.float) - data[0, 0].astype(np.float)
    for i in range(1, rows):
        timeT = data[i, 0].astype(np.float) - data[i - 1, 0].astype(np.float)
        avgSpeed = avgSpeed + ((np.linalg.norm([data[i, 4].astype(np.float) - data[i - 1, 4].astype(np.float),
                                                data[i, 5].astype(np.float) - data[i - 1, 5].astype(np.float)])) / (
                                       timeT * rows + 1))
        # to avoid NaN, 1 is added in the denominator
        meanx = meanx + ((data[i, 0].astype(np.float) - data[i - 1, 0].astype(np.float)) * (
            data[i - 1, 4].astype(np.float))) / TimeSpent
        meany = meany + ((data[i, 0].astype(np.float) - data[i - 1, 0].astype(np.float)) * (
            data[i - 1, 5].astype(np.float))) / TimeSpent
        if (data[i - 1, 3] != "Drag") and (data[i, 3] == "Drag"):
            drags = drags + 1
        if data[i - 1, 2] != data[i, 2]:
            numberOfClicks = numberOfClicks + 1

    avgMoves = (rows / TimeSpent)
    avgTime = (TimeSpent / rows)
    features = np.array([avgTime, avgSpeed, TimeSpent, avgMoves, meanx, meany, numberOfClicks, drags])
    featureVector = np.column_stack((featureVector, features))

featureVector = featureVector[:, 1:]

df = pd.DataFrame(data=featureVector,
                  index=["avgTime", 'avgSpeed', 'TimeSpent', 'avgMoves', 'meanx', 'meany', 'numberOfClicks', 'drags'])

display(df)
