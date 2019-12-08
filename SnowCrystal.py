# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 14:07:49 2019

@author: Azumi Mamiya
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

## =====parameter settings=====
alpha=1
beta=0.75#背景パラメータ
gamma=0.1#加算パラメータ
max_t=50#最大時間
fig_interval=10#画像出力間隔
x=50#横の大きさ
y=50#縦の大きさ
## ============================
fig = plt.figure(figsize=(2,2))
ax = fig.add_subplot(111)
ims=[]# 画像保存用
cell=np.ones((x, y))*beta# セルの初期状態
cell1=np.zeros((x, y))# 次の期で氷の状態のセル
cell2=np.zeros((x, y))# それ以外のセル
cell[x//2,y//2]=1#氷を１つ置く
i_minus1,i_plus1=[],[]# for x
j_minus1,j_plus1=[],[]# for y
# 境界条件の設定
for i in range(0,x):
    i_minus1.append(i-1)
    i_plus1.append(i+1)
i_minus1[0],i_plus1[-1]=x-1,1
# 境界条件の設定
for j in range(0,y):
    j_minus1.append(j-1)
    j_plus1.append(j+1)
j_minus1[0],j_plus1[-1]=x-1,1

# main loop
for t in range(max_t):
    # 隣が氷であれば，t+1期では氷になる
    # t+1期で氷であるセルをcell1
    # それ以外はcell2
    for i in range(0,cell.shape[0]):
        for j in range(0,cell.shape[1]):
            if cell[i,j]>=1:
                cell1[i,j]=cell[i,j]
            if cell[i,j_plus1[j]]>=1:#下
                cell1[i,j]=cell[i,j]
            if cell[i,j_minus1[j]]>=1:#上
                cell1[i,j]=cell[i,j]
            if cell[i_plus1[i],j]>=1:#右
                cell1[i,j]=cell[i,j]
            if cell[i_minus1[i],j]>=1:#左
                cell1[i,j]=cell[i,j]
            
            # 配列で六方格子を表現するための処理
            if j%2==0:#偶数行
                # 右隅だけ処理
                if cell[i_minus1[i],i_plus1[j]]>=1:#左下
                    cell1[i,j]=cell[i,j]
                if cell[i_minus1[i],i_minus1[j]]>=1:#左上
                    cell1[i,j]=cell[i,j]
            else:#奇数行
                # 右隅だけ処理
                if cell[i_plus1[i],i_minus1[j]]>=1:#右上
                    cell1[i,j]=cell[i,j]
                if cell[i_plus1[i],i_plus1[j]]>=1:#右下
                    cell1[i,j]=cell[i,j]
    # cell1にgamma加える
    for i in range(0,cell.shape[0]):
        for j in range(0,cell.shape[1]):
            if cell1[i,j]!=0:
                cell1[i,j]+=gamma
    # cellをcell1とcell2に分ける
    for i in range(0,cell.shape[0]):
        for j in range(0,cell.shape[1]):
            cell2[i,j]=cell[i,j]-cell1[i,j]
    # 氷の状態のセル以外の処理
    tmp_cell2=np.zeros((x, y))
    for i in range(0,cell.shape[0]):
        for j in range(0,cell.shape[1]):
            # 上下上下の処理
            tmp=-6*cell2[i,j]+cell2[i,j_plus1[j]]+cell2[i,j_minus1[j]]+cell2[i_plus1[i],j]+cell2[i_minus1[i],j]
            # 斜め方向の処理
            if j%2==0:#偶数行
                # 右隅だけ処理
                tmp+=cell2[i_minus1[i],j_plus1[j]]+cell2[i_minus1[i],j_minus1[j]]
            else:#奇数行
                # 左隅だけ処理
                tmp+=cell2[i_plus1[i],j_minus1[j]]+cell2[i_plus1[i],j_plus1[j]]
            # cell2の完成
            tmp_cell2[i,j]=cell2[i,j]+tmp*alpha/12
    
    # 次の状態のcell完成
    for i in range(0,cell.shape[0]):
        for j in range(0,cell.shape[1]):
            cell[i,j]=cell1[i,j]+tmp_cell2[i,j]
    # fig_interval毎に画像を生成
    if t%fig_interval==0:
        im = ax.imshow(cell, interpolation='none', cmap="gist_gray")
        ims.append([im])
# 最後の画像が長めに表示されるように
for i in range(10):
    ims.append([im])

ani = animation.ArtistAnimation(fig, ims)
plt.show()
#ani.save("output.gif", writer="imagemagick")
