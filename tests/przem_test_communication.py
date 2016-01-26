import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import zmq
import time
from proto import communication_pb2 as com


class TestCommunication:
    port_pub = 1111  # creating robots and updating paths
    port_obs = 2222  # observable events
    port_con = 3333  # controllable events
    context = zmq.Context()
    socket_pub = context.socket(zmq.PUB)
    socket_obs = context.socket(zmq.SUB)
    socket_con = context.socket(zmq.PUB)

    # temp - environment size
    cols = 10
    rows = 10

    def __init__(self):
        self.socket_pub.bind("tcp://*:%s" % self.port_pub)
        self.socket_obs.connect("tcp://localhost:%s" % self.port_obs)
        self.socket_con.bind("tcp://*:%s" % self.port_con)
        self.socket_obs.setsockopt(zmq.SUBSCRIBE, '')

        self.resourceMatrix = [[0 for x in range(self.cols)] for x in range(self.rows)]

    def send_msg(self, msg):
        self.socket_pub.send(msg)
        print("sent")

    def sendRobot(self):
        robot = com.Robot()
        robot.id = 0
        robot.posX = 5
        robot.posY = 5
        robot.size = 1
        # stage = robot.path.stage.add()
        # stage.x = 4
        # stage.y = 5
        # stage = robot.path.stage.add()
        # stage.x = 4
        # stage.y = 4
        # stage = robot.path.stage.add()
        # stage.x = 4
        # stage.y = 3

        for elem in self.path:
            stage = robot.path.stage.add()
            stage.x = elem[0] # wsp. x
            stage.y = elem[1] # wsp. y

        msg = robot.SerializeToString()
        self.socket_pub.send("add_robot %s" % msg)

    def generatePath(self):
        # temp path
         self.path = [[5,5], [5,4], [5,3], [5,2], [5,1]]

        # self.path = [[5,5], [5,4], [5,3], [5,2], [5,1], [5,0], [6,0], [7,0], [8,0], [9,0], [9,1], [9,2], [9,3], [9,4],
        #              [9,5], [9,6], [9,7], [9,8], [9,9], [8,9], [7,9], [6,9], [5,9], [4,9], [3,9], [2,9], [1,9], [0,9],
        #              [0,8], [0,7], [0,6], [0,5], [0,4], [0,3], [0,2], [0,1]]


    def updateResourceMatrix(self, currentStage, futureStage):

            # check if future stage is free
            if self.resourceMatrix[futureStage.x] == 0 and self.resourceMatrix[futureStage.y] == 0:
                # free current resource
                self.resourceMatrix[currentStage.x] = 0
                self.resourceMatrix[currentStage.y] = 0

                # take new resource
                self.resourceMatrix[futureStage.x] = 1
                self.resourceMatrix[futureStage.y] = 1

            # resource is occupied
            else:
                pass


    def sendEnv(self):
        env = com.Environment()
        env.x = 10
        env.y = 10
        env.baseX = 5
        env.baseY = 5
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
    test.generatePath()
    test.sendRobot()
    time.sleep(1)
    # test.sendEvent(0)
    # time.sleep(1)
    # test.sendEvent(1)
    # test.sendEvent(0)
    while True:
        string = test.socket_obs.recv()
        topic, msg = string.split(' ', 1)
        event = com.Event()
        event.ParseFromString(msg)
        print("Wysylam event!")
        print(event)


        test.sendEvent(event.robot)

if __name__ == '__main__':
    main()  # This is executed if file is not imported
