# Table from tinker
from Tkinter import *

rows = []

yMax=20
xMax=20
n_robots=7

r1_state0=[7,10]
r2_state0=[8,10]
base=[r1_state0,r2_state0,[9,10],[10,10],[11,10],[12,10],[13,10]]
#0 1 2 3
#1
#2
#3
path=[]
path_temp=[]

for n in range(0,n_robots-1):
    for i in range(0,base[n][1]+1-n):  #czyli od punktu bazowego do zera
        path_temp.append([base[n][0],base[n][1]-i]) #x sie nie zmienia

    lastX=path_temp[-1][0]
    lastY=path_temp[-1][1]
    for i in range (1,(xMax)-path_temp[-1][0]-n):
        path_temp.append([lastX+i,lastY])


    lastX=path_temp[-1][0]
    lastY=path_temp[-1][1]
    for i in range (1,yMax-path_temp[-1][1]-n):
        path_temp.append([lastX,lastY+i])

    lastX=path_temp[-1][0]
    lastY=path_temp[-1][1]
    for i in range (1,xMax-2*n):
        path_temp.append([lastX-i,lastY])

    lastX=path_temp[-1][0]
    lastY=path_temp[-1][1]
    for i in range (1,yMax-2*n):
        path_temp.append([lastX,lastY-i])

    lastX=path_temp[-1][0]
    lastY=path_temp[-1][1]
    for i in range (1,1+base[n][0]-n):
        path_temp.append([lastX+i,lastY])

    lastX=path_temp[-1][0]
    lastY=path_temp[-1][1]
    for i in range (1,1+base[n][1]-n):
        path_temp.append([lastX,lastY+i])
    path.append(path_temp)
    path_temp=[]
n=n+1
path_temp.append([base[n][0],base[n][1]])
for z in range(0,base[n][0]-base[0][0]+1):
    for i in range(1,yMax-base[n][1]):  #czyli od punktu bazowego do samego dolu
        path_temp.append([path_temp[-1][0],path_temp[-1][1]+1]) #x sie nie zmienia
    path_temp.append([path_temp[-1][0]-1,path_temp[-1][1]]) #x sie nie zmienia
    for i in range(0,yMax-base[n][1]-1):  #czyli od punktu bazowego do samego dolu
        path_temp.append([path_temp[-1][0],path_temp[-1][1]-1]) #x sie nie zmienia
for i in range(0,yMax-path_temp[-1][1]):
    path_temp.append([path_temp[-1][0],path_temp[-1][1]-1]) #x sie nie zmienia
for i in range(0,base[n][0]-path_temp[-1][0]):
    path_temp.append([path_temp[-1][0]+1,path_temp[-1][1]]) #x sie nie zmienia
for i in range(0,base[n][1]-path_temp[-1][1]):
    path_temp.append([path_temp[-1][0],path_temp[-1][1]+1]) #x sie nie zmienia


path.append(path_temp)

# #for last robot diffrent:
# for x in range(0,xMax):    #trick to fill all the cells
#     for y in range(0,yMax):
#         if not(([x,y] in path[0])or([x,y] in path[1])or([x,y] in path[2])or([x,y] in path[3])or([x,y] in path[4])or([x,y] in path[5])):
#             path_temp.append([x,y])


last_robot=[]
same_x=[]
flag=0;
# last_robot.append(min(path_temp))
# for i in range(1, len(path_temp)-1):
#     # if flag==0:
#         if path_temp[i][0]-path_temp[i-1][0]==0:
#             last_robot.append(path_temp[i])
#         else:
#             for z in range(0, len(path_temp)):
#                 if path_temp[i][0]==path_temp[z][0]: #got same X
#                     same_x.append(path_temp[z])
#             print same_x
#             # for z in range(0, len(same_x)):
#             #     if same_x[z][1]==path_temp[i-1][1]: #look for same Y
#             #         last_robot.append(same_x[z])
#             #         # same_x.remove(same_x[z])
#             for z in range(0, len(same_x)):
#                 last_robot.append(max(same_x))
#                 path_temp.remove(max(same_x))
#                 same_x.remove(max(same_x))
#             same_x=[]
#             flag=1
#         if i>=len(path_temp):
#             break
#
# last_robot.append(min(path_temp))
# for n in range(0,len(path_temp)):
#     for z in range(0,len(path_temp)):      #scan through
#         if last_robot[-1][0]-path_temp[z][0]==0: #this mean they have same X
#              for i in range(0,len(path_temp)):   #scan through Y
#                  if last_robot[-1][0]-path_temp[i][0]==0:
#                     if last_robot[-1][1]-path_temp[i][1]==-1: # this mean they Y has been incresed by one
#                         last_robot.append(path_temp[i])
#         elif last_robot[-1][1]-path_temp[z][1]==0:   #if we are here they have diffrent X so we look for same Y
#              for i in range(0,len(path_temp)):   #scan through Y
#                 if last_robot[-1][1]-path_temp[i][1]==0:
#                     if last_robot[-1][0]-path_temp[i][0]==-1: # Y is the same so X shouldnt diffre more then one
#                         last_robot.append(path_temp[i])
    # elif last_robot[-1][1]-path_temp[z][1]==-1:      #this one acctualy should not be true but added to be sure (result should be something like going on the bias)
    #      for i in range(0,len(path_temp)):   #scan through Y
    #        if last_robot[-1][1]-path_temp[i][1]==-1:
    #         if last_robot[-1][0]-path_temp[i][0]==-1:
    #            last_robot.append(path_temp[i])







path.append(path_temp) #adding last robot path



for n in range(0,n_robots):
    print path[n]


#






for y in range(yMax):
    cols = []

    for x in range(xMax):
        if [y,x] in path[6]:
            e = Entry(relief=RIDGE, bg = 'black', justify = 'center',width=3)
        elif[y,x] in path[1]:
             e = Entry(relief=RIDGE, bg = 'green', justify = 'center',width=3)
        elif[y,x] in path[2]:
            e = Entry(relief=RIDGE, bg = 'red', justify = 'center',width=3)
        elif[y,x] in path[3]:
            e = Entry(relief=RIDGE, bg = 'blue', justify = 'center',width=3)
        elif[y,x] in path[4]:
            e = Entry(relief=RIDGE, bg = 'yellow', justify = 'center',width=3)
        elif[y,x] in path[5]:
            e = Entry(relief=RIDGE, bg = 'magenta', justify = 'center',width=3)
        elif[y,x] in path[0]:
            e = Entry(relief=RIDGE, bg = 'cyan', justify = 'center',width=3)

        else:
            e = Entry(relief=RIDGE, justify = 'center',width=3)
        e.grid(row=x, column=y, sticky=NSEW)
        cols.append(e)
    rows.append(cols)

mainloop()



