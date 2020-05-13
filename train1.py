import numpy as np
Des=[]
BallPosX=[]
BallPosY=[]
BallDirection=[]
Player=[]
for x in range(0,200,5):
    for y in range(50,420,5):
        for direction in range(0,4):
            Player.append(1)
            BallPosX.append(x)
            BallPosY.append(y)
            BallDirection.append(direction)
            if direction== 1 or direction == 3:
                des_x=100
            else:
                if direction==0:#右下
                    des_x=(420-y)+x
                else:#左下
                    des_x=x-(420-y)
                while des_x>200 or des_x<0:
                    if des_x>200:
                        des_x=(200-(des_x-200))
                    else:
                        des_x=-des_x 
            Des.append(des_x)
for x in range(0,200,5):
    for y in range(50,420,5):
        for direction in range(0,4):
            Player.append(2)
            BallPosX.append(x)
            BallPosY.append(y)
            BallDirection.append(direction)
            if direction== 0 or direction == 2:
                des_x=100
            else:
                if direction==1:
                    des_x=(y-80)+x
                else:
                    des_x=x-(y-80)
                while des_x>200 or des_x<0:
                    if des_x>200:
                        des_x=(200-(des_x-200))
                    else:
                        des_x=-des_x 
            Des.append(des_x)
BallPosX=np.array(BallPosX)
BallPosY=np.array(BallPosY)
BallDirection=np.array(BallDirection)
Des=np.array(Des)
Player=np.array(Player)
BallPosX=BallPosX.reshape(len(BallPosX),1)
BallPosY=BallPosY.reshape(len(BallPosY),1)
BallDirection=BallDirection.reshape(len(BallDirection),1)
Des=Des.reshape(len(Des),1)
Player=Player.reshape(len(Player), 1)
features=np.hstack((BallPosX, BallPosY, BallDirection, Player, Des))

v0 = []
v1 = []
v2 = []
v3 = []

for i in range(len(features)):
    if features[i,2] == 0:
        v0.append(1)
        v1.append(0)
        v2.append(0)
        v3.append(0)
    elif features[i,2] == 1:
        v0.append(0)
        v1.append(1)
        v2.append(0)
        v3.append(0)
    elif features[i,2] == 2:
        v0.append(0)
        v1.append(0)
        v2.append(1)
        v3.append(0)
    else :
        v0.append(0)
        v1.append(0)
        v2.append(0)
        v3.append(1)
    
v0=np.array(v0)
v0 = v0.reshape(len(v0),1)
v1=np.array(v1)
v1 = v1.reshape(len(v1),1)
v2=np.array(v2)
v2 = v2.reshape(len(v2),1)
v3=np.array(v3)
v3 = v3.reshape(len(v3),1)

features=np.hstack((features, v0, v1, v2, v3))
print(features[0])
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics

mask = [0,1,3,5,6,7,8]
X = features[:, mask]
Y = features[:, 4]

x_train , x_test,y_train,y_test = train_test_split(X,Y,test_size=0.2)

forest_reg = RandomForestRegressor(random_state=0)
forest_reg.fit(x_train, y_train)
yt=forest_reg.predict(x_test)
print(len(yt))
print(len(y_test))

yt = yt.astype(np.int32)

import pickle

with open('save/forest_reg.pickle', 'wb') as f:
    pickle.dump(forest_reg, f)

acc=metrics.accuracy_score(yt, y_test)
print(acc)