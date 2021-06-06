#@Time:2021/6/5 10:33
#@Author: 戴 妍 晴
#@File:5.py
#@Software:PyCharm
import pandas as pd
global N
Available = []
Max = []
Allocation = []
Need = []
m = 3

#读取表格中的进程数据
def inputFromTable():
    global N
    Data = pd.read_excel(r'5.xlsx',header=1)  #读入表格数据
    N = Data.shape[0]   #获取进程数
    x = 0
    for row in Data.itertuples():   #循环表格的每一行
        x += 1
        Max.append(list(map(int,row[2].split(" "))))
        Allocation.append(list(map(int,row[3].split(" "))))
        Need.append(list(map(int,row[4].split(" "))))
        if x==1:
            tempa = row[5].split(" ")
            for i in tempa:
                Available.append(int(i))  # 各类资源的实例个数


def outputStatus(Max=Max,Allocation=Allocation,Need=Need,Available=Available):
    """
    显示当前时间内系统的状态
    """
    print("资源情况     Max     Allocation     Need      Available")
    print("进程      A  B  C     A  B  C     A  B  C     A  B  C")
    print("P0       %d  %d  %d     %d  %d  %d     %d  %d  %d     %d  %d  %d "
          %(Max[0][0],Max[0][1],Max[0][2],
                 Allocation[0][0],Allocation[0][1],Allocation[0][2],
                 Need[0][0],Need[0][1],Need[0][2],
                Available[0],Available[1],Available[2]
            )
        )
    for i in range(1,len(Max)):
        print("P%d       %d  %d  %d     %d  %d  %d     %d  %d  %d    "
              % (i,Max[i][0],Max[i][1],Max[i][2],
                 Allocation[i][0],Allocation[i][1],Allocation[i][2],
                 Need[i][0],Need[i][1],int(Need[i][2])))

def safety(Available=Available,Need=Need,Allocation=Allocation):
    """
    判断当前状态是否安全,并显示详细结果
    """
    global N
    tempAvailable = [i for i in Available]
    order = []
    Work = []
    WorkAllocation = []
    finish = 0  #已完成数
    while finish < N:
        flag = 0
        for i in range(N):  #循环所有进程
            if i not in order:
                x = 0
                for j in range(m):   #循环每个类型的资源
                    if Need[i][j] <= tempAvailable[j]:
                        x += 1
                    else:
                        break
                if x == m:  #==资源种类数
                    flag = 1
                    finish += 1
                    Work.append([i for i in tempAvailable])
                    order.append(i)
                    for j in range(m):
                        tempAvailable[j] += Allocation[i][j]
                    WorkAllocation.append([i for i in tempAvailable])
        if flag == 0:  #循环一遍找不到可运行的
            break
    if finish == N:
        outputSafeOrder(order,Work,WorkAllocation)
        print("security sequence：",end="")
        for i in order:
            print("P%d"%(i),end=",")
        print()
        return True
    else:
        print("该序列不安全")
        outputSafeOrder(order, Work, WorkAllocation)
        return False


def outputSafeOrder(order,Work,WorkAllocation):
    """
    输出安全序列
    """
    print("资源情况     Work       Need      Allocation  Work+Allocation   Finish")
    print("进程      A  B  C     A  B  C     A  B  C      A  B  C")
    for i in range(len(order)):
        print("P%d       %d  %d  %d     %d  %d  %d     %d  %d  %d        %d  %d  %d        true"
              % (order[i],Work[i][0], Work[i][1], Work[i][2],
                 Need[order[i]][0], Need[order[i]][1], Need[order[i]][2],
                 Allocation[order[i]][0], Allocation[order[i]][1], Allocation[order[i]][2],
                 WorkAllocation[i][0], WorkAllocation[i][1], WorkAllocation[i][2]
                 )
              )


def changeResource(n,request):
    """
    调用资源请求算法来分配进程请求的资源
    :param n:Who makes a further request (the number of the process)
    :param request:The request
    """
    global N
    tempAvailable = [i for i in Available]
    tempNeed = [[j for j in i] for i in Need]
    tempAllocation = [[j for j in i] for i in Allocation]
    for i in range(m):
        tempAllocation[n][i] += request[i]
        tempNeed[n][i] -= request[i]
        tempAvailable[i] -= request[i]
    return tempAvailable,tempNeed,tempAllocation

if __name__ == '__main__':
    inputFromTable()  # 输入所需的信息和系统的当前状态
    print("T0时间内系统的状态:")
    outputStatus()  # 显示T0时间内系统的状态
    print()
    safety()  # 调用安全算法以查看当前状态是否安全，并显示详细结果
    # # T1时刻请求
    # P = 1  # 发出请求的进程编号
    # request = [1, 0, 2]  # 请求的资源情况
    while 1:
        print("输入新请求")
        P = int(input("进程号："))
        request = list(map(int,input("请求的资源情况：").split(" ")))
        for i in request:
            if request[i] > Need[P][i] or request[i] > Available[P][i]:
                print("请求的资源不正确，请重试")
        tempAvailable,tempNeed,tempAllocation = changeResource(P,request)
        outputStatus(Max,tempAllocation,tempNeed,tempAvailable)    #显示当前时间内系统的状态
        status = safety(tempAvailable,tempNeed,tempAllocation)     #调用安全算法以查看当前状态是否安全，并显示详细结果
        if status:
            print("当前状态安全,请求能被批准")
            print("安全序列为",status)  #输出进程的安全顺序
        else:
            print("当前状态不安全,请求不能被批准")
            break
        x = input("是否有新请求？")
        if x == "":
            break
