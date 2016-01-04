import zmq
import time
import model
import communication_pb2 as com


class Communication:
    port_sub = 1111  # creating robots and updating paths
    port_obs = 2222  # observable events
    port_con = 3333  # controllable events
    context = zmq.Context()
    socket_sub = context.socket(zmq.SUB)
    socket_obs = context.socket(zmq.PUB)
    socket_con = context.socket(zmq.SUB)

    def __init__(self):
        self.robots = []

        self.socket_sub.connect("tcp://localhost:%s" % self.port_sub)
        self.socket_con.connect("tcp://localhost:%s" % self.port_con)
        self.socket_obs.bind("tcp://*:%s" % self.port_obs)

        self.socket_con.setsockopt(zmq.SUBSCRIBE, '')
        self.socket_sub.setsockopt(zmq.SUBSCRIBE, '')

    def recv_msg(self, root, time):
        poll = zmq.Poller()
        poll.register(self.socket_sub, zmq.POLLIN)
        sockets = dict(poll.poll(1000))
        if self.socket_sub in sockets:
            string = self.socket_sub.recv()
            topic, msg = string.split(' ', 1)
            if topic == "add_robot":
                self.addRobot(msg, root, time)

        root.after(time, self.recv_msg, root, time)

    def addRobot(self, msg, root, time):
        robot_msg = com.Robot()
        robot_msg.ParseFromString(msg)
        path = []
        for s in robot_msg.path.stage:
            stage = (s.x, s.y)
            path.append(stage)
        robot = model.Robot(robot_msg.id, robot_msg.posX, robot_msg.posY,
                            robot_msg.size, self.socket_obs, self.socket_con,
                            robot_msg.speed, path)
        self.robots.append(robot)
        root.after(time, robot.recvEvent, root, time)
