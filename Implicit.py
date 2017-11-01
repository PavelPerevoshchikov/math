import math
import xlrd, xlwt
import pylab
from mpl_toolkits.mplot3d import Axes3D
import numpy
def analiticT(x,t):
    return math.sin(x) + math.log(t * t + 1)
def CalculateStartCondition(x):
    return math.sin(x)
def CalculateLeftBorderCondition(t):
    return math.log(t * t + 1)
def CalculateRightBorderCondition(t):
    return math.log(t * t + 1)
def f(x,t):
    return math.sin(x) + 2*t/(t*t + 1)
def ImplicitMethod(length,h,timeEnd,tt,a):
    L = int(length / h)
    rangeTemp = int(timeEnd / tt)
    q = tt * a * a / (h * h)
    Temp = []
    Temp.append([CalculateStartCondition(i * h) for i in range(0, L + 1)])
    Temp[0][L] = CalculateStartCondition(0)
    alf = []
    bet = []
    for j in range(1, rangeTemp + 1):
        alf.append(0)
        alf.append(0)
        bet.append(0)
        bet.append(CalculateLeftBorderCondition(j * tt))
        for i in range(1, L):
            coefA = q;
            coefB = q
            coefC = -(1 + 2 * q)
            coefD = -tt * f(h * i, tt * j) - Temp[j - 1][i]
            alf.append(-coefB / (coefA * alf[i] + coefC))
            bet.append((coefD - coefA * bet[i]) / (coefA * alf[i] + coefC))
        Temp.append([0 for i in range(0, L + 1)])
        Temp[j][L] = CalculateRightBorderCondition(tt * j)
        Temp[j][0] = CalculateLeftBorderCondition(tt * j)
        for i in range(L - 1, 0, -1):
            Temp[j][i] = alf[i + 1] * Temp[j][i + 1] + bet[i + 1]
        alf.clear()
        bet.clear()
    return (Temp.copy())
def CalculateError(Method,length,h,timeEnd,tt,a):
    temperature = Method(length,h,timeEnd,tt,a)
    realtemperature = [[analiticT(i*h,t *tt ) for i in range(0,int(length/h) +1)] for t in range(0,int(timeEnd / tt) +1 )]
    error = max( [math.fabs(temperature[t][x] - realtemperature[t][x]) for x in range (0,int(length/h) +1) for t in range(0,int(timeEnd / tt) +1 )])
    return error
def PrintToFileErrors(number):
    stepT = 0.25
    stepX = math.pi / 5
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Test', cell_overwrite_ok=True)
    for i in range(0, number):
        ws.write(i + 1, 0, stepX / math.pow(2, i))
        ws.write(0, i + 1, stepT / math.pow(2, i))
    ws.write(0, 0, "Time\H")
    for i in range(0, number):
        for j in range(0, number):
            ws.write(i + 1, j + 1, CalculateError(ImplicitMethod, math.pi, stepX / pow(2, j), 10.0, stepT / math.pow(2, i), 1))
    wb.save("Implicit.xls")
def ShowTemperature(h,tt):
    x = numpy.arange(0, math.pi + h, h)
    y = numpy.arange(0, 10 + tt, tt)
    xgrid, ygrid = numpy.meshgrid(x, y)
    Temp = ImplicitMethod(math.pi,h,10,tt,1)
    zgrid1 = numpy.array(Temp)
    fig = pylab.figure()
    axes = Axes3D(fig)
    axes.set_xlabel("шаг по пространству")
    axes.set_ylabel("шаг по времени")
    axes.set_zlabel("температура")
    axes.plot_surface(xgrid, ygrid, zgrid1, rstride=1, cstride=1)
    #pylab.xlabel("Шаг по пространству")
    pylab.show()
#print(CalculateError(ImplicitMethod,math.pi,math.pi/5,10.0,0.25,1))

#вычисление начальной температуры
#PrintToFileErrors(2)
ShowTemperature(math.pi/5,0.25)