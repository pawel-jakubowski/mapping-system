import zmq
import time
from requests.utils import get_environ_proxies

import communication_pb2 as com


class Controller:
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

        self.notHandledEvents = []
        self.highPrioEvents = []
        self.robotsPaths = []

        self.waitForRecvEvent = True


    def defineEnv(self,x,y,base_x,base_y):
        env = com.Environment()
        env.x = x
        env.y = y
        env.baseX = base_x
        env.baseY = base_y
        msg = env.SerializeToString()
        self.socket_pub.send("environment %s" % msg)

        # definition of state with free and occupied resources
        print("envx " + str(env.x))
        print("envy" + str(env.y))

        self.stateMatrix = [[0 for x in range(env.x)] for x in range(env.y)]


    def generatePath(self, robotID):
        # place for magic path generator
        # temp path
        # path0 = [[5,5], [5,4], [5,3], [5,2], [5,1], [5,0], [6,0]]
        # path1 = [[6,5], [7,5], [8,5], [9,5], [8,5], [7,5], [6,5]]
        path0 = [[5,5], [5,4], [6,4], [6,3], [5,3], [5,2], [6,2], [6,1], [5,1], [5,0], [6,0]]
        path1 = [[6,5], [6,4], [6,3], [6,2], [6,1], [6,0], [7,0]]

        # path0 = [[7,10], [7,11], [7,12], [7,13], [7,14], [8,14], [9,14], [10,14], [10,15], [10,16]]
        # path1 = [[8,10], [8,11], [8,12], [8,13], [8,14], [8,15], [8,16]]


        if robotID == 0:
            tempPath = {'robotID': robotID, 'path':path0}
        else:
            tempPath = {'robotID': robotID, 'path':path1}

        # remember path in robotsPaths dict!
        self.robotsPaths.append(tempPath)
        if robotID == 0:
            return path0
        else:
            return path1


    def getCoordFromPath(self, robotID, stage):
        # robotID-1 because index list starts from 0, we are num. robots from 1
        id = self.robotsPaths[robotID]['robotID']
        path = self.robotsPaths[robotID]['path']

        x = path[stage][0]
        y = path[stage][1]
        return x,y


    def getNumOfStages(self, robotID):
        # we are conting stages from 0
        nStages = len(self.robotsPaths[robotID]['path']) - 1
        return nStages


    def isThisLastStage(self, dEvent):
        if dEvent['currentStage'] == self.getNumOfStages(dEvent['robotID']):
            return True
        else:
            return False


    def checkIfFuturePosIsFree(self, dEvent):
        currentX, currentY = self.getCoordFromPath(dEvent['robotID'], dEvent['currentStage'])
        futureX, futureY = self.getCoordFromPath(dEvent['robotID'], dEvent['futureStage'])

        if self.stateMatrix[futureY][futureX] == 0:
            return True
        else:
            print("R{0} jestem w: {1} {2} - current".format(dEvent['robotID'], currentX, currentY))
            print("R{0} {1} {2} resource is occupied!".format(dEvent['robotID'], futureX, futureY))
            return False


    def takeFutureResorce(self, dEvent):
        futureX, futureY = self.getCoordFromPath(dEvent['robotID'], dEvent['futureStage'])
        currentX, currentY = self.getCoordFromPath(dEvent['robotID'], dEvent['currentStage'])
        self.stateMatrix[futureY][futureX] = 1

        print("R{0} jestem w: {1} {2} - current".format(dEvent['robotID'], currentX, currentY))
        print("R{0} zajmuje: {1} {2} - future".format(dEvent['robotID'], futureX, futureY))


    def freeOldResource(self, dEvent):
        oldX, oldY = self.getCoordFromPath(dEvent['robotID'], dEvent['oldStage'])
        oldStage = dEvent['oldStage']

        # free old resource
        if oldStage >= 0:
            self.stateMatrix[oldY][oldX] = 0
            print("R{0} zwalniam: {1} {2}".format(dEvent['robotID'], oldX, oldY))


    def defineRobot(self, robotId, robotX0, robotY0, robotPath):#define how many robots should be created
        robot = com.Robot()
        robot.id = robotId
        robot.posX = robotX0
        robot.posY = robotY0
        robot.size = 1

        for elem in robotPath:
            stage = robot.path.stage.add()
            stage.x = elem[0] # coordinate x
            stage.y = elem[1] # cooridante y

        msg = robot.SerializeToString()
        self.socket_pub.send("add_robot %s" % msg)


    def receiveEvents(self):
        string = self.socket_obs.recv()
        topic, msg = string.split(' ', 1)
        event = com.Event()
        event.ParseFromString(msg)


        # event with data - dictionary!
        dEvent = self.getDataFromEvent(event)
        print("Receive Obs event ze:")
        print(dEvent)

        self.freeOldResource(dEvent)

        self.notHandledEvents.append(event)


    def handleEvents(self):

        # check if in highPrioEvents list exist not checked event
        if self.allHighPrioEventsChecked() == False:
            dEvent = self.highPrioEvents.pop()

            # flag 'checked' is connected only with highPrioEvents list!
            dEvent['checked'] = True
            self.waitForRecvEvent = False

        else:
            # allHighPrioEventsChecked() == True, so get normal not handled event
            event = self.notHandledEvents.pop()

            # event with data - dictionary!
            dEvent = self.getDataFromEvent(event)

            # set flag 'checked' to False
            self.rmHighPrioCheckedFlag()
            self.waitForRecvEvent = True

        print("+++")
        if self.isThisLastStage(dEvent) == False:
            # if resource is free, we are able to handle this event
            if self.checkIfFuturePosIsFree(dEvent) == True:
                self.takeFutureResorce(dEvent)
                self.sendContEvent(dEvent['robotID'], dEvent['futureStage'])
            else:
                # put this resource in highPrioEvents
                self.highPrioEvents.append(dEvent)
                # print("highPro: "+str(self.highPrioEvents))
            print("---")


    def allHighPrioEventsChecked(self):
        # if all events from HighPrio list were checked, get normal event from notHandledEvents list
        # flag 'checked' is connected only with highPrioEvents list!

        if len(self.highPrioEvents) == 0:
            return True
        else:
            for dEvent in self.highPrioEvents:
                if ('checked' in dEvent):
                    if dEvent['checked'] == False:
                        # print("not checked")
                        return False
                    # else:
                    #     print("checked")

                else:
                    print("Error!")

            return True



    def rmHighPrioCheckedFlag(self):
        # reset 'checked' flag in 'highPrioEvents' list means: all highPrioEvents were checked (checked==True)
        # and we took normalEvent
        #
        # robot from this normal event could free resource
        # so we have to reset flag in highPrioEvents which all are checked ('checked'==True)
        # and check highPrio list once again

        if len(self.highPrioEvents) > 0:
            for dEvent in self.highPrioEvents:
                if ('checked' in dEvent):
                   if dEvent['checked'] == True:
                       # reset flag
                       dEvent['checked'] = False
                   else:
                       print("Error in rmHighPrio!")

                else:
                     print("This situation can not occur!")



    def getDataFromEvent(self, eventTemp):
        # tablica danych z eventu
        # [robot id, stage/resource ktory chce zajac dany robot, stage/resource w ktorym jest dany robot,
        # stage resource w ktorym byl dany robot]
        # na podstawie path danego robota wyznaczamy x y poszczegolnych stagow/resourcow

        event = {'event': eventTemp, 'robotID': eventTemp.robot, 'futureStage': eventTemp.stage,
                 'currentStage': eventTemp.stage-1, 'oldStage': eventTemp.stage-2, 'checked':False}

        return event


    def sendContEvent(self, robot, stage):
        event = com.Event()
        event.robot = robot
        event.stage = 1

        msg = event.SerializeToString()
        self.socket_con.send("%d %s" % (event.robot, msg))
        print "Robot {0} send control event".format(robot)



    def sendEnvMsg(self):
        # ta wiadmosc wysyalana jest tylko jeden raz
        # wysylamy sciezki kazdego robota na poczatku do symulatora
        print "sending the initialize environment/path message"
        time.sleep(1)
        # self.defineEnv(20,20,7,10)
        self.defineEnv(10,10,5,6)
        time.sleep(1)
        self.defineRobot(0,5,5, self.generatePath(0))
        time.sleep(1)
        self.defineRobot(1,6,5, self.generatePath(1))
        time.sleep(1)
        # self.defineRobot(3,6,5, self.generatePath())
        # time.sleep(1)

	 
def main():
    controller = Controller()
    time.sleep(1)
    controller.sendEnvMsg()
    time.sleep(5)

    while True:
            # print("1")
            if controller.waitForRecvEvent == True:
                controller.receiveEvents()
            # print("2")
            controller.handleEvents()
            # print("3")

if __name__ == '__main__':
    main()  # This is executed if file is not imported

