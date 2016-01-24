import zmq
import time
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



    def defineEnv(self,x,y,base_x,base_y):
        env = com.Environment()
        env.x = x
        env.y = y
        env.baseX = base_x
        env.baseY = base_y
        msg = env.SerializeToString()
        self.socket_pub.send("environment %s" % msg)



    def PathGeneration(self):
	
	return 0



    def defineRobot(self, robot_id, robot_x0, robot_y0, robot_path):#define how many robots should be created
        robot = com.Robot()
        robot.id = robot_id
        robot.posX = robot_x0
        robot.posY = robot_y0
        robot.size = 1
	stage = robot.path.stage.add()
        stage.x = robot_x0
        stage.y = robot_y0
        stage = robot.path.stage.add()
        stage.x = robot_x0
        stage.y = robot_y0+1
        stage = robot.path.stage.add()
        stage.x = robot_x0
        stage.y = robot_y0+2
	stage = robot.path.stage.add()
        stage.x = robot_x0
        stage.y = robot_y0+3
	stage = robot.path.stage.add()
        stage.x = robot_x0
        stage.y = robot_y0+4
	stage = robot.path.stage.add()
        stage.x = robot_x0+1
        stage.y = robot_y0+4
	stage = robot.path.stage.add()
        stage.x = robot_x0+2
        stage.y = robot_y0+4
	stage = robot.path.stage.add()
        stage.x = robot_x0+3
        stage.y = robot_y0+4
	stage = robot.path.stage.add()
        stage.x = robot_x0+4
        stage.y = robot_y0+4
	msg = robot.SerializeToString()
        self.socket_pub.send("add_robot %s" % msg)

    def defineRobot1(self, robot_id, robot_x0, robot_y0, robot_path):#define how many robots should be created
        robot = com.Robot()
        robot.id = robot_id
        robot.posX = robot_x0
        robot.posY = robot_y0
        robot.size = 1
	stage = robot.path.stage.add()
        stage.x = robot_x0
        stage.y = robot_y0
        stage = robot.path.stage.add()
        stage.x = robot_x0+1
        stage.y = robot_y0
        stage = robot.path.stage.add()
        stage.x = robot_x0+2
        stage.y = robot_y0
	stage = robot.path.stage.add()
        stage.x = robot_x0+3
        stage.y = robot_y0
	stage = robot.path.stage.add()
        stage.x = robot_x0+4
        stage.y = robot_y0
	stage = robot.path.stage.add()
        stage.x = robot_x0+4
        stage.y = robot_y0+1
	stage = robot.path.stage.add()
        stage.x = robot_x0+4
        stage.y = robot_y0+2
	stage = robot.path.stage.add()
        stage.x = robot_x0+4
        stage.y = robot_y0+3
	msg = robot.SerializeToString()
        self.socket_pub.send("add_robot %s" % msg)


    def ControlableEvent(self, robot):
        event = com.Event()
        event.robot = robot
        event.stage = 1
	msg = event.SerializeToString()
	#print "send control event"
	print "send control event for robot:" + str(event.robot)
	#print event.stage
        self.socket_con.send("%d %s" % (event.robot, msg))




    def InitEnvPathSendMessage(self):
	print "sending the initialize environment/path message"
	time.sleep(1)
	self.defineEnv(20,20,10,10)
	time.sleep(1)
	self.defineRobot(0,7,10,self.PathGeneration())
	time.sleep(1)
	self.defineRobot1(1,8,10,self.PathGeneration())
	time.sleep(1)
	self.defineRobot(2,9,10,self.PathGeneration())
	time.sleep(1)
	self.defineRobot1(3,10,10,self.PathGeneration())
	time.sleep(1)
	self.defineRobot(4,11,10,self.PathGeneration())
	time.sleep(1)
	self.defineRobot1(5,2,10,self.PathGeneration())
	time.sleep(1)
	self.defineRobot(6,3,10,self.PathGeneration())
	time.sleep(1)
	self.defineRobot1(7,4,10,self.PathGeneration())
	time.sleep(1)
	self.defineRobot(8,5,10,self.PathGeneration())
	time.sleep(1)


	 
def main():
    controller = Controller()
    time.sleep(1)
    controller.InitEnvPathSendMessage()
    time.sleep(5)
    while True:
 	string = controller.socket_obs.recv()
        topic, msg = string.split(' ', 1)
        event = com.Event()
        event.ParseFromString(msg)
	print(event)
	controller.ControlableEvent(event.robot)
	

if __name__ == '__main__':
    main()  # This is executed if file is not imported































