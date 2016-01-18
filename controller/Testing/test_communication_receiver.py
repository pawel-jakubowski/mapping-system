import zmq
import time
import communication_pb2 as com


class TestCommunication:
    port_pub = 1111  # creating robots and updating paths
    port_obs = 2222  # observable events
    port_con = 3333  # controllable events
    context = zmq.Context()
    socket_pub = context.socket(zmq.SUB)
    #socket_obs = context.socket(zmq.PUB)
    socket_con = context.socket(zmq.SUB)

    def __init__(self):
        self.socket_pub.connect("tcp://localhost:%s" % self.port_pub)
        #self.socket_obs.bind("tcp://*:%s" % self.port_obs)
        self.socket_con.connect("tcp://localhost:%s" % self.port_con)
        self.socket_pub.setsockopt(zmq.SUBSCRIBE, '')
	self.socket_con.setsockopt(zmq.SUBSCRIBE, '')

    

    

def main():
    test = TestCommunication()
    time.sleep(2)
    while True:
        string_pub = test.socket_pub.recv()
	string_con = test.socket_con.recv()
        topic, msg = string_pub.split(' ', 1)
        robot = com.Robot()
        robot.ParseFromString(msg)
        print(robot)
	print(msg)
       # print(string_pub)
	#print(string_con)

if __name__ == '__main__':
    main()  # This is executed if file is not imported
