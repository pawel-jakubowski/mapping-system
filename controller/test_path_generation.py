# Table from tinker
from Tkinter import *

rows = []

yMax=20
xMax=20
n_robots=5

r1_state0=[7,10]
r2_state0=[8,10]
base=[r1_state0,r2_state0,[9,10],[10,10],[11,10]]
#0 1 2 3
#1
#2
#3
path=[]
path_temp=[]

for n in range(0,n_robots):
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

for n in range(0,n_robots):
    print path[n]







for y in range(yMax):
    cols = []

    for x in range(xMax):
        if [y,x] in path[0]:
            e = Entry(relief=RIDGE, bg = 'black', justify = 'center',width=3)
        elif[y,x] in path[1]:
            e = Entry(relief=RIDGE, bg = 'green', justify = 'center',width=3)
        elif[y,x] in path[2]:
            e = Entry(relief=RIDGE, bg = 'red', justify = 'center',width=3)
        elif[y,x] in path[3]:
            e = Entry(relief=RIDGE, bg = 'blue', justify = 'center',width=3)
        elif[y,x] in path[4]:
            e = Entry(relief=RIDGE, bg = 'yellow', justify = 'center',width=3)
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