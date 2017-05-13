# -*- coding: utf-8 -*-
#!/usr/bin/env python
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
import copy

#Load image from URL
def readImage(url):
    file = cStringIO.StringIO(urllib2.urlopen(url).read())
    imgOri = Image.open(file)
    img = cv2.cvtColor(np.array(imgOri),cv2.COLOR_RGB2BGR)
    return img


# Analyze label-dataFrame
def readLabel():
    emailImageIDList = zip(emailList,imageIDList)
    emailImageIDSet = set(emailImageIDList)
    infoDict=dict.fromkeys(emailImageIDSet)
    dictKeys = infoDict.keys()
    for item in dictKeys:
        infoDict[item] = []
    for index in range(label.shape[0]):
        pos = label.ix[index]['PointsJson']
        pos = eval(pos)
        listTemp=[]
        listTemp.append(pos['topleft']['x'])
        listTemp.append(pos['topleft']['y'])
        listTemp.append(pos['bottomright']['x'])
        listTemp.append(pos['bottomright']['y'])
        keyVal = (label.ix[index]['Email'],label.ix[index]['ImageID'])
        infoDict[keyVal].append(listTemp)
    
    infoDictOri = copy.deepcopy(infoDict)
    for key in infoDict:
        popIndex = []
        valueL = infoDict[key]
        thresh = 0.02
        for index in range(len(valueL)):
            if index in popIndex:
                continue
            for secondIndex in range(index+1,len(valueL)):
                firstBoxCenterX = (valueL[index][0]+valueL[index][2])/2.0
                firstBoxCenterY = (valueL[index][1]+valueL[index][3])/2.0
                secondBoxCenterX = (valueL[secondIndex][0]+valueL[secondIndex][2])/2.0
                secondBoxCenterY = (valueL[secondIndex][1]+valueL[secondIndex][3])/2.0
                centerDiff = np.sqrt((firstBoxCenterX-secondBoxCenterX)**2 + (firstBoxCenterY-secondBoxCenterY)**2 )
                if centerDiff < thresh:
                    popIndex.append(secondIndex)
        popIndex = list(set(popIndex))
        base = 0
        for i in popIndex:
            valueL.pop(i-base)
            base = base + 1
        infoDict[key] = valueL
    
    infoDictPop = infoDict      
    
    return infoDictOri,infoDictPop


#Plot boxes on everay image for every user
def plotBox(dictItem,i):
    targetImageID = list(imageIDSet)[i]
    for index in range(label.shape[0]):
        if label.ix[index]['ImageID'] == targetImageID:
            imageURL =  label.ix[index]['ImageName'] 
            break
    
    img= readImage(imageURL)
    img2 = copy.deepcopy(img)
    img3 = copy.deepcopy(img)
    rows = img.shape[0]
    cols = img.shape[1]
    user1Flag = False
    user2Flag = False
    user3Flag = False
    if ('user1@cc.com',targetImageID) in dictItem.keys():
        user1Flag = True
        user1BoxList = dictItem[('user1@cc.com',targetImageID)]
        
    if ('user2@cc.com',targetImageID) in dictItem.keys():
        user2Flag = True
        user2BoxList = dictItem[('user2@cc.com',targetImageID)]
        
    if ('user3@cc.com',targetImageID) in dictItem.keys():
        user3Flag = True
        user3BoxList = dictItem[('user3@cc.com',targetImageID)]
    
    #user1
    totalSubFig = user1Flag + user2Flag + user3Flag
    beginIndex = 0
    subplotIndexList = range(1,totalSubFig+1) 
    if user1Flag:
        for posList in user1BoxList:
            leftTop = (int(posList[0]*cols),int(posList[1]*rows))
            rightBottom = (int(posList[2]*cols),int(posList[3]*rows))
            cv2.rectangle(img,leftTop,rightBottom,(255,0,255),3)
            
        (r, g, b)=cv2.split(img)  
        img=cv2.merge([b,g,r])  
        plt.subplot(1,totalSubFig,subplotIndexList[beginIndex])
        beginIndex = beginIndex + 1
        plt.xticks([],[])#do not show ticks
        plt.yticks([],[])
        plt.title('User'+str(1))
        plt.imshow(img)
    
    #user2
    if user2Flag:
        for posList in user2BoxList:
            leftTop = (int(posList[0]*cols),int(posList[1]*rows))
            rightBottom = (int(posList[2]*cols),int(posList[3]*rows))
            cv2.rectangle(img2,leftTop,rightBottom,(255,0,255),3)
            
        (r, g, b)=cv2.split(img2)  
        img2=cv2.merge([b,g,r])  
        plt.subplot(1,totalSubFig,subplotIndexList[beginIndex])
        beginIndex = beginIndex + 1
        plt.xticks([],[])#do not show ticks
        plt.yticks([],[])
        plt.title('User'+str(2))
        plt.imshow(img2)
    
    #user3
    if user3Flag:
        for posList in user3BoxList:
            leftTop = (int(posList[0]*cols),int(posList[1]*rows))
            rightBottom = (int(posList[2]*cols),int(posList[3]*rows))
            cv2.rectangle(img3,leftTop,rightBottom,(255,0,255),3)
            
        (r, g, b)=cv2.split(img3)  
        img3=cv2.merge([b,g,r])  
        plt.subplot(1,totalSubFig,subplotIndexList[beginIndex])
        beginIndex = beginIndex + 1
        plt.xticks([],[])#do not show ticks
        plt.yticks([],[])
        plt.title('User'+str(3))
        plt.imshow(img3)
    
    plt.show()
        



# stats about every user
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
    
    
    
# stats about every image   
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
    #optimalUserIDForImage = pd.DataFrame(columns=['user'],index=imageIDSet)
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
    
    totalBox.index.name = 'ImageID'
    totalArea.index.name = 'ImageID'
    optimalUserIDForImage.index.name = 'ImageID'
    
    totalBox.to_csv('imageStas_totalBox.csv')
    totalArea.to_csv('imageStas_totalArea.csv')
    optimalUserIDForImage.to_csv('optimalUserIDForImage.csv')
    
    return totalBox,totalArea,optimalUserIDForImage
       
    
def stats():
    statsAboutPerson()
    
    totalBox,totalArea,optimalUserIDForImage = statsAboutImage()
    return totalBox,totalArea,optimalUserIDForImage
        
        

if __name__ == '__main__': 
    label = pd.read_csv('labels.csv')
    imageIDSet = set(label['ImageID'])
    imageIDList = list(label['ImageID'])
    userIDSet = set(label['UserID'])
    userIDList = list(label['UserID'])
    emailSet = set(label['Email'])
    emailList = list(label['Email'])
    infoDict,infoDictPop = readLabel()
    

    #statsAboutPerson()
    totalBox,totalArea,optimalUserIDForImage = stats()
    
    '''
    while(True):
        num = raw_input("Select Image Num from 0 to %d:\n"%(len(imageIDSet)-1))
        num = int(num)
        if num < 0:
            break
        plotBox(infoDictPop,num)
    '''
