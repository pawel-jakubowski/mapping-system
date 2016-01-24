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
	msg = robot.SerializeToString()
        self.socket_pub.send("add_robot %s" % msg)



    def QueueController(self):
	string = self.socket_obs.recv()
        topic, msg = string.split(' ', 1)
        event = com.Event()
        event.ParseFromString(msg)
	event_table=[event.robot,event.stage,event.stage-1,event.stage-2] 
        print(event)
	print(event_table)
	return event_table   



    def ControlableEvent(self, robot, stage):
        event = com.Event()
        event.robot = robot
        event.stage = stage
	msg = event.SerializeToString()
	print "send control event"
	print event.robot
	print event.stage
        self.socket_con.send("%d %s" % (event.robot, msg))




    def InitEnvPathSendMessage(self):
	print "sending the initialize environment/path message"
	time.sleep(1)
	self.defineEnv(20,20,10,10)
	time.sleep(1)
	self.defineRobot(0,7,10,self.PathGeneration())
	time.sleep(1)
	self.defineRobot(1,8,10,self.PathGeneration())
	time.sleep(1)
	#self.defineRobot(2,9,10,self.PathGeneration())
	time.sleep(1)
	#self.defineRobot(3,10,10,self.PathGeneration())
	time.sleep(1)
	#self.defineRobot(4,11,10,self.PathGeneration())
	time.sleep(1)



    
#def ReceiveEvent():
	#odbior danych z QueueControllera
	#bierzemy pierwszy event 

	#event zwraca nam pozycje robota
 	#id robota
	#resource w ktorym jest
	#recource o ktory pyta

	#na podstawie tego w ktorym jest i o ktory pyta oraz generowanej sciezki
	#wyznaczamy resource w ktorym byl 
	#pakujemy 
	#wysylamy do controllera

#def FreeResource():
	#odbiera dane z receive event
	#zwolnienie resourcu czyli ustawienie resourcu w ktorym byl robot na unknown
	#Update stata //czyli update informacji o planszy ktore resourcy sa wolne ktory nie itd


#def AllocateResource():
	#odbior danych
	#zajecie resourcu
	#Update stata
	#wyslij dane do symulator funckja PublishData()
	
#def Controller():
	# z funkcji Receive Event dostajemy info w talblicyo id robota 
	
	#otrzymujemy dane
	
	#zwalniamy resource funckja FreeResource
	#sprawdzamy czy na liscie z wiekszym priorytetem mozna przypisac odpowiedni resource to to robimy

	#if resource o ktory pytamy jest wolny
	#odpalamy funckje AllocateResource
	#else
	#resource jest zajety 
	#tworzymy liste robotow z wyzszy priorytem,
	 
def main():
    controller = Controller()
    time.sleep(1)
    controller.InitEnvPathSendMessage()
    time.sleep(2)
    while True:
 	string = controller.socket_obs.recv()
        topic, msg = string.split(' ', 1)
        event = com.Event()
        event.ParseFromString(msg)
	print(event)
	print(event.robot)
	print(event.stage)
	controller.ControlableEvent(1,1)
	#time.sleep(1)

if __name__ == '__main__':
    main()  # This is executed if file is not imported































