import Tkinter as tk
from simulator import gui as simulatorGui
from simulator import communication as c

# def simpleCallback(object, robotId)

def main():
    gui = tk.Tk()
    app = simulatorGui.Window(gui)

    # Initialization
    # TODO: do after obtaining parameters from controller
    gui.window.addBoard(20)
    gui.window.board.setBase([7,10],[12,10])
    # gui.window.board.setBase([5,5],[6,5])

    # Init robots
    # gui.window.board.addRobot(0, 7, 10)
    # gui.window.board.addRobot(1, 9, 10)
    # gui.window.board.addRobot(2, 11, 10)
    # gui.window.board.refresh()
    # Example how to move robots
    # gui.window.moveRobot(0, 7, 11)

    com = c.Communication()
    time = 1
    gui.after(time, com.recv_msg, gui, time)
    gui.after(time, com.recv_event, gui, time)
    gui.mainloop()

if __name__ == '__main__':
    main()  # This is executed if file is not imported
