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

#for last robot diffrent:
for x in range(0,xMax):    #trick to fill all the cells
    for y in range(0,yMax):
        if not(([x,y] in path[0])or([x,y] in path[1])or([x,y] in path[2])or([x,y] in path[3])or([x,y] in path[4])or([x,y] in path[5])):
            path_temp.append([x,y])


last_robot=[]
same_x=[]
flag=0;
last_robot.append(min(path_temp))
for i in range(1, len(path_temp)-1):
    # if flag==0:
        if path_temp[i][0]-path_temp[i-1][0]==0:
            last_robot.append(path_temp[i])
        else:
            for z in range(0, len(path_temp)):
                if path_temp[i][0]==path_temp[z][0]: #got same X
                    same_x.append(path_temp[z])
            print same_x
            # for z in range(0, len(same_x)):
            #     if same_x[z][1]==path_temp[i-1][1]: #look for same Y
            #         last_robot.append(same_x[z])
            #         # same_x.remove(same_x[z])
            for z in range(0, len(same_x)):
                last_robot.append(max(same_x))
                path_temp.remove(max(same_x))
                same_x.remove(max(same_x))
            same_x=[]
            flag=1
        if i>=len(path_temp):
            break

print path_temp
print '\n'
print last_robot

path.append(path_temp) #adding last robot path


#
# for n in range(0,n_robots):
#     print path[n]
#
#
#






for y in range(yMax):
    cols = []

    for x in range(xMax):
        if [y,x] in path[6]:
            e = Entry(relief=RIDGE, bg = 'black', justify = 'center',width=3)
        # elif[y,x] in path[1]:
        #     e = Entry(relief=RIDGE, bg = 'green', justify = 'center',width=3)
        # elif[y,x] in path[2]:
        #     e = Entry(relief=RIDGE, bg = 'red', justify = 'center',width=3)
        # elif[y,x] in path[3]:
        #     e = Entry(relief=RIDGE, bg = 'blue', justify = 'center',width=3)
        # elif[y,x] in path[4]:
        #     e = Entry(relief=RIDGE, bg = 'yellow', justify = 'center',width=3)
        # elif[y,x] in path[5]:
        #     e = Entry(relief=RIDGE, bg = 'magenta', justify = 'center',width=3)
        # elif[y,x] in path[6]:
        #     e = Entry(relief=RIDGE, bg = 'cyan', justify = 'center',width=3)

        else:
            e = Entry(relief=RIDGE, justify = 'center',width=3)
        e.grid(row=x, column=y, sticky=NSEW)
        cols.append(e)
    rows.append(cols)

mainloop()



        #     if [y,x] in forbiden :
        #   e = Entry(relief=RIDGE, bg = 'black', justify = 'center')
        # elif ([y,x] in corrTerminal) and (U[x][y] > 0):
        #   e = Entry(relief=RIDGE, bg = 'green', justify = 'center')
        # elif ([y,x] in corrTerminal) and (U[x][y] < 0):
        #   e = Entry(relief=RIDGE, bg = 'red', justify = 'center')
        # elif ([y,x] in corrSpecial):
        #   e = Entry(relief=RIDGE, bg = 'blue', justify = 'center')
        # else:
        #   e = Entry(relief=RIDGE, justify = 'center')
        # e.grid(row=x, column=y, sticky=NSEW)
        # if [y,x] in forbiden :
        #   e.insert(END, 'X')
        # elif ([y,x] in corrTerminal) and (U[x][y] > 0):
        #   e.insert(END, '(%s)' % (U[x][y]))
        # elif ([y,x] in corrTerminal) and (U[x][y] < 0):
        #   e.insert(END, ' (%s)' % ( U[x][y]))
        # else:
        #   e.insert(END, '%s (%s)' % (Pi[x][y], U[x][y]))