import Tkinter as tk
import gui

def main():
    rootFrame = tk.Tk()
    app = gui.Window(rootFrame)
    rootFrame.mainloop()

if __name__ == '__main__':
    main()  # This is executed if file is not imported
