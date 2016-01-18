# mapping-system
Event based controller for scalable robotic swarm that map given area

## Controller

## Simulator
To run simulator just call `python simulator.py` from root repository directory.
:exclamation: Due to issue [#1](../../issues/1) GUI runs really slow. If you want to test GUI itself it is recommended to comment line 12 (`gui.after(time, com.recv_msg, gui, time)`) in simulator.py.
