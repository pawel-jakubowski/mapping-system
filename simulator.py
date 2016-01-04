import Tkinter as tk
from simulator import gui
from simulator import communication as c


def main():
    gui, app = initGui()
    com = c.Communication()
    time = 1
    for robot in app.board.robots:
        gui.after(time, robot.animate, gui, time)
    gui.after(time, com.recv_msg, gui, time)
    gui.mainloop()


def initGui():
    rootFrame = tk.Tk()
    app = gui.Window(rootFrame)
    print "Board size: %d" % app.board.size
    print "Robots: %d" % app.board.robots_count
    print "Robots coordinates:"
    print app.board.robots
    return rootFrame, app

if __name__ == '__main__':
    main()  # This is executed if file is not imported
