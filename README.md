# mapping-system
Event based controller for scalable robotic swarm that map given area

## Requirements
Python 2.7.10 with following packages:
* argparse (1.2.1)
* enum (0.4.6)
* protobuf (2.6.1)
* pyzmq (15.1.0)
* wheel (0.24.0)

## Controller
To run controller just call `python controller.py` from root repository directory.

:exclamation: Remember to start simulator first.

    usage: controller.py [-h] [-s SPEED]

    optional arguments:
    -h, --help            show this help message and exit
    -s SPEED, --speed SPEED
                        robots speed


## Simulator
To run simulator just call `python simulator.py` from root repository directory.

    usage: simulator.py [-h] [-t]

    optional arguments:
      -h, --help  show this help message and exit
      -t, --test  test mode (without communication)
