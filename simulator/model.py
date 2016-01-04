import zmq
import communication_pb2 as com
class Robot:
    def __init__(self, id, x, y, size, socket_pub, socket_sub, speed=2, path=[]):
        self.id = id
        self.x = x
        self.y = y
        self.speed = speed
        self.stage = 0
        self.path = path
        self.socket_pub = socket_pub
        self.socket_sub = socket_sub

    def update_path(self, path, stage=None):
        self.path = path
        if stage is not None:
            self.stage = stage
        # if stage is not set the first stage with the robot's position is set
        else:
            for i, pos in enumerate(path):
                if self.x == pos.x:
                    if self.y == pos.y:
                        self.stage = i
                        break

    def sendEvent(self):
        self.stage = self.stage + 1
        self.x = self.path[self.stage][0]
        self.y = self.path[self.stage][1]
        event = com.Event()
        event.robot = self.id
        event.stage = self.stage
        msg = event.SerializeToString()
        self.socket_pub.send("%d %s" % (self.id, msg))
        print(msg, "sent")

    def recvEvent(self, root, time):
        poll = zmq.Poller()
        poll.register(self.socket_sub, zmq.POLLIN)
        sockets = dict(poll.poll(1000))
        if self.socket_sub in sockets:
            string = self.socket_sub.recv()
            topic, msg = string.split(' ', 1)
            if topic == str(self.id):
                event = com.Event()
                event.ParseFromString(msg)
                print("Robot %d should move" % self.id)
                # do sth to move robot
        root.after(time, self.recvEvent, root, time)
