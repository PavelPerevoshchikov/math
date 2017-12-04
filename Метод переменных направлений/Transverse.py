import math
def init():
    global hX,hT,hY,maxX,maxY,maxT,sigmaX,sigmaY,Temp
    lX = 2 * math.pi
    lY = 2 * math.pi
    lT = 10
    hX = hY = math.pi / 20
    hT = 0.25/4
    maxX = int(lX / hX)
    maxY = int(lY/ hY)
    maxT = int(lT / hT)
    sigmaX = hT / hX**2
    sigmaY = hT / hY**2
    startConditionTemp = [ [startCondition(i*hX,j*hY) for i in range(maxX+1)] for j in range(maxY+1) ]
    Temp = [[[0 for i in range(maxX+1)] for i in range(maxY+1)] for i in range(maxT+1)]
    Temp[0] = startConditionTemp.copy()
def startCondition(x,y):
    return math.sin(x + y)
def mu1(indexY,indexT):
    y = indexY * hY
    t = indexT * hT
    return math.sin(y) + math.log(t ** 2 + 1)
def mu2(indexY,indexT):
    y = indexY * hY
    t = indexT * hT
    return math.sin(y) + math.log(t**2 + 1)
def _mu1(indexY,indexT):
    valueTop = _L2(mu1(indexY - 1, indexT + 1), mu1(indexY, indexT + 1), mu1(indexY + 1, indexT + 1))
    value = _L2(mu1(indexY - 1, indexT), mu1(indexY, indexT), mu1(indexY + 1, indexT))
    return (mu1(indexY,indexT) + mu1(indexY,indexT+1)) / 2 - (hT/4)*(valueTop - value)
def _mu2(indexY,indexT):
    valueTop = _L2(mu2(indexY - 1, indexT + 1),mu2(indexY, indexT + 1),mu2(indexY + 1, indexT + 1))
    value = _L2(mu2(indexY - 1, indexT),mu2(indexY, indexT),mu2(indexY + 1,indexT))
    return (mu2(indexY, indexT) + mu2(indexY, indexT + 1)) / 2 - (hT / 4) * (valueTop - value)
def mu3(indexX,indexT):
    return math.sin(indexX*hX) + math.log((indexT*hT)**2 + 1)
def mu4(indexX,indexT):
    return math.sin(indexX * hX) + math.log((indexT * hT) ** 2 + 1)
def F(indexX,indexY,indexT):
    x = indexX * hX
    y = indexY * hY
    t = indexT * hT
    return 2*math.sin(x + y) + 2*t/(t**2 + 1)
def analiticT(indexX, indexY, indexT):
    x = indexX * hX
    y = indexY * hY
    t = indexT * hT
    return math.sin(x + y) + math.log(t**2 + 1)
def L1(indexX,indexY,mas):
    return (mas[indexY][indexX - 1] - 2*mas[indexY][indexX] + mas[indexY][indexX + 1])/hX**2
def _L2(value1,value2,value3):
    return (value1 - 2*value2 + value3)/hY**2
def L2(indexX,indexY,mas):
    return (mas[indexY - 1][indexX] - 2*mas[indexY][indexX] + mas[indexY + 1][indexX])/hY**2
def CalculateTemp():
    alfa = []
    beta = []
    for time in range(maxT):
        intermediateTemp = [[0 for i in range(maxX + 1)] for i in range(maxY + 1)]
        for m in range(1,maxY):
            alfa.clear()
            beta.clear()
            alfa.append(0)
            alfa.append(0)
            beta.append(0)
            beta.append(_mu1(m,time))
            intermediateTemp[m][0] = _mu1(m,time)
            intermediateTemp[m][maxX] = _mu2(m,time)
            A = B = -sigmaX
            C = 2 * (1 + sigmaX)
            for n in range(1,maxX):
                D = 2*Temp[time][m][n] + hT * L2(n,m,Temp[time]) + hT *F(n, m, time + 0.5)
                alfa.append(-B / (A*alfa[n] + C))
                beta.append((D - A * beta[n]) / (A*alfa[n] + C))
            for n in range(maxX-1,0,-1):
                intermediateTemp[m][n] = alfa[n+1] * intermediateTemp[m][n+1] +beta[n+1]
        for m in range(maxY+1):
            Temp[time+1][m][0] = mu1(m,time+1)
            Temp[time+1][m][maxX] = mu2(m,time+1)
        for n in range(1,maxX):
            alfa.clear()
            beta.clear()
            alfa.append(0)
            alfa.append(0)
            beta.append(0)
            beta.append(mu3(n,time+1))
            Temp[time+1][0][n] = mu3(n,time+1)
            Temp[time + 1][maxY][n] = mu4(n, time + 1);
            A = B = -sigmaY
            C = 2*(1+sigmaY)
            for m in range(1,maxY):
                D = 2 * intermediateTemp[m][n] + hT * L1(n,m,intermediateTemp) + hT *F(n, m, time + 0.5)
                alfa.append(-B / (A * alfa[m] + C))
                beta.append((D - A * beta[m]) / (A * alfa[m] + C))
            for m in range(maxY - 1,0,-1):
                Temp[time + 1][m][n] = alfa[m + 1] * Temp[time + 1][m + 1][n] + beta[m + 1]
def CalculateError():
    init()
    CalculateTemp()
    realtemperature = [[[analiticT(indexX,indexY,indexT) for indexX in range(maxX + 1)] for indexY in range(maxY + 1)] for indexT in range(maxT + 1)]
    error = max( [math.fabs(Temp[t][y][x] - realtemperature[t][y][x]) for x in range (maxX+1) for y in range(maxY+1) for t in range(maxT+1 )])
    return error
print(CalculateError())