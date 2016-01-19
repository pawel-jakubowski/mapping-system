import zmq
import time
import communication_pb2 as com


class TestCommunication:
    port_pub = 1111  # creating robots and updating paths
    port_obs = 2222  # observable events
    port_con = 3333  # controllable events
    context = zmq.Context()
    socket_pub = context.socket(zmq.PUB)
    socket_obs = context.socket(zmq.SUB)
    socket_con = context.socket(zmq.PUB)

    def __init__(self):
        self.socket_pub.bind("tcp://*:%s" % self.port_pub)
        self.socket_obs.connect("tcp://localhost:%s" % self.port_obs)
        self.socket_con.bind("tcp://*:%s" % self.port_con)
        self.socket_obs.setsockopt(zmq.SUBSCRIBE, '')

    def send_msg(self, msg):
        self.socket_pub.send(msg)
        print("sent")

    def sendRobot(self):
        robot = com.Robot()
        robot.id = 0
        robot.posX = 4
        robot.posY = 5
        robot.size = 1
        stage = robot.path.stage.add()
        stage.x = 4
        stage.y = 5
        stage = robot.path.stage.add()
        stage.x = 4
        stage.y = 4
        stage = robot.path.stage.add()
        stage.x = 4
        stage.y = 3
        msg = robot.SerializeToString()
        self.socket_pub.send("add_robot %s" % msg)

    def sendEnv(self):
        env = com.Environment()
        env.x = 30
        env.y = 30
        env.baseX = 10
        env.baseY = 10
        msg = env.SerializeToString()
        self.socket_pub.send("environment %s" % msg)

    def sendEvent(self, robot):
        event = com.Event()
        event.robot = robot
        event.stage = 1
        msg = event.SerializeToString()
        self.socket_con.send("%d %s" % (event.robot, msg))


def main():
    test = TestCommunication()
    time.sleep(1)
    test.sendEnv()
    time.sleep(2)
    test.sendRobot()
    time.sleep(5)
    test.sendEvent(0)
    time.sleep(1)
    test.sendEvent(1)
    test.sendEvent(0)
    while True:
        string = test.socket_obs.recv()
        topic, msg = string.split(' ', 1)
        event = com.Event()
        event.ParseFromString(msg)
        print(event)

if __name__ == '__main__':
    main()  # This is executed if file is not imported
