import argparse
import Tkinter as tk
from simulator import gui as simulatorGui
from simulator import communication as c

# def simpleCallback(object, robotId)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="test mode (without communication)", action='store_true')
    args = parser.parse_args()

    gui = tk.Tk()
    app = simulatorGui.Window(gui)

    if args.test:
        app.testMode()
    else:
        # TODO: do after obtaining parameters from controller
        gui.window.addBoard(20)
        gui.window.board.setBase([7,10],[12,10])

        com = c.Communication()
        time = 1
        gui.after(time, com.recv_msg, gui, time)
        gui.after(time, com.recv_event, gui, time)
        
    gui.mainloop()

if __name__ == '__main__':
    main()  # This is executed if file is not imported
