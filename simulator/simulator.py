import Tkinter as tk
import gui


def main():
    gui, app = initGui()
    time = 1
    for robot in app.board.robots:
        gui.after(time, robot.animate, gui, time)
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
