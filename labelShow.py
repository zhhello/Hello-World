#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
71-build a tool to compare the labeling results from different judges
"""

import cv2
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt

import urllib2
from PIL import Image
import cStringIO



def readImage(url):
    file = cStringIO.StringIO(urllib2.urlopen(url).read())
    imgOri = Image.open(file)
    img = cv2.cvtColor(np.array(imgOri),cv2.COLOR_RGB2BGR)
    return img


#plot only one box in a particular image
def printBox(img,leftTop,rightBottom):
    rows = img.shape[0]
    cols = img.shape[1]
    assert(leftTop[0]<rows and leftTop[0]<rightBottom[0] and leftTop[1]<cols and rightBottom[1]<cols and leftTop[1]<rightBottom[1])
    cv2.rectangle(img,leftTop,rightBottom,(0,0,255),2)
    cv2.namedWindow('Fig',cv2.WINDOW_NORMAL)
    cv2.imshow('Fig',img)
    cv2.waitKey(0)

#plot multiple boxes in a image
def printBoxInSameImage(img,leftTopList,rightBottomList,i):
    rows = img.shape[0]
    cols = img.shape[1]
    assert( len(leftTopList)==len(rightBottomList) )
    for ix in range(len(leftTopList)):
        leftTop = leftTopList[ix]
        rightBottom = rightBottomList[ix]
        #assert(leftTop[0]<rows and leftTop[0]<rightBottom[0] and leftTop[1]<cols and rightBottom[1]<cols and leftTop[1]<rightBottom[1])
        cv2.rectangle(img,leftTop,rightBottom,(255,0,255),3)
    cv2.namedWindow('Fig'+str(i),cv2.WINDOW_NORMAL)
    cv2.imshow('Fig'+str(i),img)
    
    

def processOneImage(index):
#    index = 100 
    imageName = label.ix[index]['ImageName']
    img= readImage(imageName)
    rows = img.shape[0]
    cols = img.shape[1]
    pos = label.ix[index]['PointsJson']
    pos = eval(pos)
    topleft = (int(pos['topleft']['x']*cols),int(pos['topleft']['y']*rows))
    bottomright = (int(pos['bottomright']['x']*cols),int(pos['bottomright']['y']*rows))
    printBox(img,topleft,bottomright)
    
    

def processSameImage(index,i):
    startIndex = index
    stopIndex = index
    goal = label.ix[startIndex]['ImageID']
    while startIndex > 0:
        if label.ix[startIndex-1]['ImageID'] == goal:
            startIndex = startIndex - 1
        else:
            break
    
    goal = label.ix[stopIndex]['ImageID']
    while stopIndex < label.shape[0]-1:
        if label.ix[stopIndex+1]['ImageID'] == goal:
            stopIndex = stopIndex + 1
        else:
            break
        
    imageName = label.ix[index]['ImageName']
    img= readImage(imageName)
    rows = img.shape[0]
    cols = img.shape[1]
    
    topLeftList=[]
    bottomRightList=[]
    for index in range(startIndex,stopIndex+1):
        pos = label.ix[index]['PointsJson']
        pos = eval(pos)
        topLeft = (int(pos['topleft']['x']*cols),int(pos['topleft']['y']*rows))
        bottomRight = (int(pos['bottomright']['x']*cols),int(pos['bottomright']['y']*rows))
        topLeftList.append(topLeft)
        bottomRightList.append(bottomRight)
      
    printBoxInSameImage(img,topLeftList,bottomRightList,i)




# plot box in image
def printBoxInSameImage2(img,leftTopList,rightBottomList,i,num,figNum):
    assert( len(leftTopList)==len(rightBottomList) )
    for ix in range(len(leftTopList)):
        leftTop = leftTopList[ix]
        rightBottom = rightBottomList[ix]
        cv2.rectangle(img,leftTop,rightBottom,(255,0,255),3)
        
    (r, g, b)=cv2.split(img)  
    img=cv2.merge([b,g,r])  
    #figName = 'Fig'+str(i)
    plt.subplot(1,figNum,i+1)
    plt.xticks([],[])#do not show ticks
    plt.yticks([],[])
    plt.title('User'+str(num))
    plt.imshow(img)


# process image with the same imageID
# index: the row index of image in dataFrame
# i: for plotting index
# num : the user
# figNum : the total figure to be plotted
def processSameImage2(index,i,num,figNum):
    startIndex = index
    stopIndex = index
    goal = label.ix[startIndex]['ImageID']
    while startIndex > 0:
        if label.ix[startIndex-1]['ImageID'] == goal:
            startIndex = startIndex - 1
        else:
            break
    
    goal = label.ix[stopIndex]['ImageID']
    while stopIndex < label.shape[0]-1:
        if label.ix[stopIndex+1]['ImageID'] == goal:
            stopIndex = stopIndex + 1
        else:
            break
        
    imageName = label.ix[index]['ImageName']
    img= readImage(imageName)
    rows = img.shape[0]
    cols = img.shape[1]
    
    topLeftList=[]
    bottomRightList=[]
    for index in range(startIndex,stopIndex+1):
        pos = label.ix[index]['PointsJson']
        pos = eval(pos)
        topLeft = (int(pos['topleft']['x']*cols),int(pos['topleft']['y']*rows))
        bottomRight = (int(pos['bottomright']['x']*cols),int(pos['bottomright']['y']*rows))
        topLeftList.append(topLeft)
        bottomRightList.append(bottomRight)
      
    printBoxInSameImage2(img,topLeftList,bottomRightList,i,num,figNum)




#find Last Image With particular ImageID And UserID, return the Row Index of labels(dataFrame) 
def findLastImageWithImageIDAndUserID(targetImageID,targetUserID,indexList):
    index = 0
    while index < len(imageIDList):
        if imageIDList[index] == targetImageID and userIDList[index] == targetUserID:
            while imageIDList[index] == targetImageID and userIDList[index] == targetUserID and index < len(imageIDList)-1 :
                index = index+1
            indexList.append(index-1)
        else:
            index = index + 1
        
        
    
def showImageWithNumK(i):
    targetImageID = list(imageIDSet)[i]
    #targetUserID = list(label['UserID'])[imageIDList.index(targetImageID)]
    indexList = []
    for userIDPar in userIDSet:
        findLastImageWithImageIDAndUserID(targetImageID,userIDPar,indexList)
     
    for i in range(len(indexList)):
        processSameImage(indexList[i],i)
    cv2.waitKey(0)
    
    
def showImageWithNumK2(i):
    targetImageID = list(imageIDSet)[i]
    indexList = []
    for targetUserID in userIDSet:
        findLastImageWithImageIDAndUserID(targetImageID,targetUserID,indexList)
    
    #print indexList
    for i in range(len(indexList)):
        emailAddress = label.ix[indexList[i]]['Email']
        num = mapEmailToUserID(emailAddress)
        processSameImage2(indexList[i],i,num,len(indexList))
    plt.show()
    

def mapEmailToUserID(email):
    if email=='user1@cc.com':
        return 1
    elif email=='user2@cc.com':
        return 2
    elif email=='user3@cc.com':
        return 3
    else:
        pass


def statsAboutPerson():
    #userDict = dict.fromkeys(('user1','user2','user3'),0)
    #stats: user 1
    totalFig = 0
    totalBox = 0
    totalArea = 0.0
    userImageIDSet=set()
    for index in range(label.shape[0]):
        if label.ix[index]['Email'] == 'user1@cc.com':
            userImageIDSet.add(label.ix[index]['ImageID'])
            pos = label.ix[index]['PointsJson']
            pos = eval(pos)
            area = abs(pos['topleft']['x']-pos['bottomright']['x'])*abs(pos['topleft']['y']-pos['bottomright']['y'])
            totalArea += area
            totalBox += 1
    totalFig = len(userImageIDSet)
    print "user1: totalFig: %d, totalBox: %d, totalArea: %f"%(totalFig,totalBox,totalArea)
    print "user1: averageBox: %f, averageArea: %f"%(totalBox*1.0/totalFig,totalArea*1.0/totalFig)
    print
    #stats: user 2
    totalFig = 0
    totalBox = 0
    totalArea = 0.0
    userImageIDSet=set()
    for index in range(label.shape[0]):
        if label.ix[index]['Email'] == 'user2@cc.com':
            userImageIDSet.add(label.ix[index]['ImageID'])
            pos = label.ix[index]['PointsJson']
            pos = eval(pos)
            area = abs(pos['topleft']['x']-pos['bottomright']['x'])*abs(pos['topleft']['y']-pos['bottomright']['y'])
            totalArea += area
            totalBox += 1
    totalFig = len(userImageIDSet)
    print "user2: totalFig: %d, totalBox: %d, totalArea: %f"%(totalFig,totalBox,totalArea)
    print "user2: averageBox: %f, averageArea: %f"%(totalBox*1.0/totalFig,totalArea*1.0/totalFig)
    print
    #stats: user 3
    totalFig = 0
    totalBox = 0
    totalArea = 0.0
    userImageIDSet=set()
    for index in range(label.shape[0]):
        if label.ix[index]['Email'] == 'user3@cc.com':
            userImageIDSet.add(label.ix[index]['ImageID'])
            pos = label.ix[index]['PointsJson']
            pos = eval(pos)
            area = abs(pos['topleft']['x']-pos['bottomright']['x'])*abs(pos['topleft']['y']-pos['bottomright']['y'])
            totalArea += area
            totalBox += 1
    totalFig = len(userImageIDSet)
    print "user3: totalFig: %d, totalBox: %d, totalArea: %f"%(totalFig,totalBox,totalArea)
    print "user3: averageBox: %f, averageArea: %f"%(totalBox*1.0/totalFig,totalArea*1.0/totalFig)
    
    
    
    
def statsAboutImage():
    totalBox = pd.DataFrame(columns=['user1','user2','user3'],index=imageIDSet,data=0.0)
    totalArea = pd.DataFrame(columns=['user1','user2','user3'],index=imageIDSet,data=0.0)
    for index in range(label.shape[0]):
        imageID = label.ix[index]['ImageID']
        
        userID = 'user1'
        if label.ix[index]['Email'] == 'user1@cc.com':
            userID = 'user1'
        elif label.ix[index]['Email'] == 'user2@cc.com':
            userID= 'user2'
        elif label.ix[index]['Email'] == 'user3@cc.com':
            userID = 'user3'
        else:
            pass
        
        pos = label.ix[index]['PointsJson']
        pos = eval(pos)
        area = abs(pos['topleft']['x']-pos['bottomright']['x'])*abs(pos['topleft']['y']-pos['bottomright']['y'])
        totalBox.ix[imageID][userID] += 1
        totalArea.ix[imageID][userID] += area 
    
    #return totalBox,totalArea
    optimalUserIDForImage = pd.Series(index=imageIDSet)
    for imageID in imageIDSet:
        s = totalArea.ix[imageID]
        sIndex = list(s.index)
        sValue = list(s.values)
        minIx = sValue.index(min(sValue))
        sIndex.pop(minIx)
        #leaving 2 users
        s2 = totalBox.ix[imageID]
        if s2[sIndex[0]] > s2[sIndex[1]]:
            optimalUser = sIndex[0]
        else:
            optimalUser = sIndex[1]
        optimalUserIDForImage[imageID] = optimalUser
                             
    return totalBox,totalArea,optimalUserIDForImage
    
    
    


if __name__ == '__main__': 
    label = pd.read_csv('labels.csv')
    imageIDSet = set(label['ImageID'])
    imageIDList = list(label['ImageID'])
    userIDSet = set(label['UserID'])
    userIDList = list(label['UserID'])
    emailSet = set(label['Email'])
    '''
    userIDEmailSet = set()
    for i in range(label.shape[0]):
        userIDEmailSet.add((label.ix[i]['UserID'],label.ix[i]['Email']))
    '''
    
    
    num = raw_input("Select Image Num from 0 to %d:\n"%(len(imageIDSet)-1))
    num = int(num)
    #showImageWithNumK2(num)
    
    
    #statsAboutPerson()
    #totalBox,totalArea = statsAboutImage()
    
    
    
    
