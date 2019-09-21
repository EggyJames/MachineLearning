from math import sqrt
from random import randint

#创建kd树
def createTree(dataSet,layer = 0,feature = 2):  #feature值为特征的值
    length = len(dataSet)   #数据集的长度
    dataSetCopy = dataSet[:] #不能直接赋值，会指向同一段代码
    featureNum = layer % feature    #所在特征值的位数
    dataSetCopy.sort(key = lambda x : x[featureNum])    #对那层特征进行排序 key = lambda x : x[n]为固定格式
    layer+=1
    if length == 0:
        return None
    elif length == 1:
        return{'Value':dataSet[0],'Layer':layer,'Feature':featureNum,'Left':None,'Right':None}
    elif length != 1:
        midNum = length // 2    # //整数除法
        dataSetLeft = dataSetCopy[:midNum]
        dataSetRight = dataSetCopy[midNum+1:]
        return{'Value':dataSetCopy[midNum],'Layer':layer,'Feature':featureNum,'Left':createTree(dataSetLeft,layer)
        ,'Right':createTree(dataSetRight,layer)}
    
#计算距离
def calDistance(sourcePoint,targetPoint):
    length = len(targetPoint)   #计算特征数
    sum = 0.0
    for i in range(length):
        sum+=(sourcePoint[i] - targetPoint[i])**2   #幂运算
    sum = sqrt(sum)
    return sum

#DFS算法
def dfs(kdTree,target,tracelist=[]):
    tracelistCopy = tracelist[:]
    if not kdTree:
        return None,tracelistCopy
    elif not kdTree['Left']:        #kd树是个平衡搜索树
        tracelistCopy.append(kdTree['Value'])
        return kdTree['Value'],tracelistCopy
    elif kdTree["Left"]:
        pointValue = kdTree['Value']
        feature = kdTree['Feature']
        tracelistCopy.append(pointValue)
        if target[feature] <= pointValue[feature]:
            return dfs(kdTree['Left'],target,tracelistCopy)
        elif target[feature] > pointValue[feature]:
            return dfs(kdTree['Right'],target,tracelistCopy)

def findPoint(Tree,value):
    if Tree != None and Tree['Value'] == value:
        return Tree
    else:
        if Tree['Left'] != None:
            return findPoint(Tree['Left'],value) or findPoint(Tree['Right'],value)

#kd查找
def kdTreeSearch(tracelist,target,usedPoint=[],minDistance=float('inf'),minDistancePoint=None):
    tracelistCopy = tracelist[:]
    usedPointCopy = usedPoint[:]

    if not minDistancePoint:
        minDistancePoint = tracelistCopy[-1]
    
    if len(tracelistCopy) == 1:
        return minDistancePoint
    else:
        point = findPoint(kdTree,tracelist[-1])
        
        if calDistance(point['Value'], target) < minDistance:
            minDistance = calDistance(point['Value'],target)
            minDistancePoint = point['Value']
        fatherPoint = findPoint(kdTree,tracelistCopy[-2])
        fatherPointVal = fatherPoint['Value']
        fatherPointFea = fatherPoint['Feature']

        if calDistance(fatherPoint['Value'],target) < minDistance:
            minDistance = calDistance(fatherPoint['Value'],target)
            minDistancePoint = fatherPoint['Value']
        
        if point == fatherPoint['Left']:
            anotherPoint = fatherPoint['Right']
        elif point == fatherPoint['Right']:
            anotherPoint = fatherPoint['Left']

        if anotherPoint == None or anotherPoint['Value'] in usedPointCopy or abs(fatherPointVal[fatherPointFea] - target[fatherPointFea]) > minDistance:
            usedPoint = tracelistCopy.pop()
            usedPointCopy.append(usedPoint)
            return kdTreeSearch(tracelistCopy,target,usedPointCopy,minDistance,minDistancePoint)
        else:
            usedPoint = tracelistCopy.pop()
            usedPointCopy.append(usedPoint)
            subvalue,subtrackList = dfs(anotherPoint,target)
            tracelistCopy.extend(subtrackList)
            return kdTreeSearch(tracelistCopy,target,usedPointCopy,minDistance,minDistancePoint)

trainningSet = [(2,3),(5,4),(9,6),(4,7),(8,1),(7,2)]
kdTree = createTree(trainningSet)
target = eval(input('input target point:'))     #eval可以用来提取用户输入的多个值
value,tracklist = dfs(kdTree,target)
nnPoint = kdTreeSearch(tracklist,target)
print(nnPoint)
            
