# coding:UTF-8
import time,os
import xlrd,xlwt
import csv
import math
import pandas as pd
import numpy as np
#np.set_printoptions(threshold = np.inf) 
def prim(graph, vertex_num):
    INF = 9999+1        # 更改最大权重值
    visit = [False] * vertex_num
    dist = [INF]*vertex_num
    for i in range(vertex_num):
        dist[i] = graph[0][i]#[INF] * vertex_num    from scatter 0
    cloest = [0] * vertex_num

    #preIndex = [0] * vertex_num
    #对所有的顶点进行循环，首先是确定头结点
    #找到当前无向图的最小生成树
    weight = 0
    #minDist = INF 
    #nextIndex = 0
    for i in range(vertex_num):

        minDist = INF 
        nextIndex = 0
        #第一次循环时，nextIndex就是头结点
        #所以要把minDIst加上1，之后这个循环
        #的功能是找到基于当前i，邻接矩阵中i行到哪一行距离最小的那个位置作为下一个结点，当然前提是那个结点没有去过
        for j in range(vertex_num):
            if dist[j] < minDist and not visit[j]:
                
                minDist = dist[j]
                nextIndex = j
                #print(minDist,"#",nextIndex,"#",j)
                #input()
                #print(minDist,nextIndex)
        #print("##########")      
        weight += minDist
        #print (nextIndex)
        visit[nextIndex] = True
        
        #由于前面已经找到了下一个结点了，现在就要构建再下一个结点的dist矩阵了，这就要看当前这个nextIndex这一行了
        for j in range(vertex_num):
            if dist[j] > graph[j][nextIndex] and not visit[j]:
                dist[j] = graph[j][nextIndex]
                cloest[j] = nextIndex + 1
                #preIndex[j] = nextIndex
    for i in range(vertex_num):
        if(cloest[i] == 0):
            cloest[i] = 1
    return dist,cloest,weight #preIndex

def csv_rd(path):
    
    data = pd.read_csv(path,usecols=[1,2,3])#['IN_FID','NEAR_FID','距离']
    data_array = np.array(data)
    y,x = data_array.shape
    count = 0
    for i in range(y):
        #print(math.isnan(data_array[i][0]))
        if(math.isnan(data_array[i][0]) == False):
            count += 1
    IN = data_array[0:count,0]
    NEAR = data_array[0:count,1]
    DIST = data_array[0:count,2]
    return IN,NEAR,DIST

def csv_xy(path):
    data = pd.read_csv(path,usecols=[3,4])
    data_array = np.array(data)
    y,x = data_array.shape
    count = 0
    for i in range(y):
        #print(math.isnan(data_array[i][0]))
        if(math.isnan(data_array[i][0]) == False):
            count += 1
    x_list = data_array[0:count,0]
    y_list = data_array[0:count,1]
    return x_list,y_list
        
def excel_make(cloest,x_list,y_list,path):
    xl = xlwt.Workbook(encoding='utf-8')
    sheet = xl.add_sheet('sheet1', cell_overwrite_ok=False)
    head = ["线名称","序号","X","Y"]
    for i in range(4):
        sheet.write(0,i,head[i])##绘制表头
    lenth = len(x_list)
    pointer = 0
    for i in range(lenth):
        sheet.write(i*2+1,0,i+1)
        sheet.write(i*2+2,0,i+1)
        sheet.write(i*2+1,1,i*2+1)
        sheet.write(i*2+2,1,i*2+2)
        sheet.write(i*2+1,2,x_list[i])
        sheet.write(i*2+2,2,x_list[int(cloest[i])-1])
        sheet.write(i*2+1,3,y_list[i])
        sheet.write(i*2+2,3,y_list[int(cloest[i])-1])
    xl_path = os.path.dirname(path)
    xl.save(xl_path + "\prim_result.xls")
    print("结果保存在近邻点加权文件同一上级路径下！")
        
if __name__ == '__main__':

    path = input("输入近邻点加权文件路径：")
    #path = "C:\\Users\\13216\\Desktop\\近邻表.csv"
    a = os.path.dirname(path)
    path_1 = input("输入点坐标文件路径：")
    IN,NEAR,DIST = csv_rd(path)
    number = len(IN)
    print(IN,NEAR,DIST)
    print("总点数：",number)
    #N = int(input("输入点的数目："))
    #print("其实输不输都无所谓 ‘(‵▽′)’,按ENTER键继续：")

    _ = 9999
    N = 696
    if(number == N*N):
        print("数据正常，开始导入邻接矩阵......")
    else:
        y_n = input("数据异常，是否继续？(y/n)")
        if(y_n == "n" or y_n == "N"):
            exit(0)
        print("开始导入邻接矩阵......")
    start = time.perf_counter()
    ################################  开始运算  ##########################
    v_graph = np.full((N,N),_)
    ######### 构建邻接矩阵 #########
    for i in range(len(IN)):
        v_graph[int(IN[i])-1][int(NEAR[i])-1] = DIST[i]
        #v_graph[int(x[i])-1][int(y[i])-1] = near_dist[i]
        v_graph[int(IN[i])-1][int(IN[i])-1] = 0
    print("邻接矩阵shape:",v_graph.shape)
    #print(v_graph)
    #input()
    dist, cloest, weight = prim(v_graph, N)
    print(cloest)
    print(len(cloest))
    chang = len(cloest)
    print("加权总和：",weight)
    x_list,y_list = csv_xy(path_1)
    excel_make(cloest,x_list,y_list,path)
    end = time.perf_counter()
    print('计算用时总计：',str(end - start),'秒')      
    input()


















    
