import zmq
# import time
import model
import communication_pb2 as com
import time as t


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

    def recv_msg( self, root, time):
        try:
            string = self.socket_sub.recv(flags=zmq.NOBLOCK)
            topic, msg = string.split(' ', 1)
            if topic == "add_robot":
                self.addRobot(msg, root, time)
            elif topic == "environment":
                self.initEnvironment(msg)
        except zmq.error.ZMQError as e:
            if 'Resource temporarily unavailable' in str(e):
                pass
            else:
                raise e

        root.after(time, self.recv_msg, root, time)

    def recv_event(self, root, time):
        try:
            # print("f. recv cont event")
            string = self.socket_con.recv(flags=zmq.NOBLOCK)
            # print(string)
            topic, msg = string.split(' ', 1)
            self.robots[int(topic)].recvEvent(msg, root)
        except zmq.error.ZMQError as e:
            if 'Resource temporarily unavailable' in str(e):
                pass
            else:
                raise e

        root.after(time, self.recv_event, root, time)

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
        robot.addMoveCallback(self.moveRobot)
        self.robots.append(robot)
        root.window.board.addRobot(robot_msg.id, robot_msg.posX, robot_msg.posY, robot_msg.speed)
        sendEventLambda = lambda robot_id: self.sendEvent(robot_id)
        root.window.board.robots[robot_msg.id].setEventCallback(sendEventLambda)
        root.window.board.refresh()
        print("Robot created")
        robot.sendEvent()

    def initEnvironment(self, msg):
        env_msg = com.Environment()
        env_msg.ParseFromString(msg)
        print(env_msg)

    def sendEvent(self, robot_id):
        for r in self.robots:
            if r.id == robot_id:
                print("Sim send obser. event")
                print(r.path, r.stage)
                r.sendEvent()
        print "Get Event from: " + str(robot_id)

    @staticmethod
    def moveRobot(root, robot_id, x, y):
        root.window.moveRobot(robot_id, x, y)
        # print(robot_id)
