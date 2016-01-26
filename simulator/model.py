from proto import  communication_pb2 as com


class Robot:
    def __init__(self, id, x, y, socket_pub, socket_sub, speed=2,
                 path=[]):
        self.id = id
        self.x = x
        self.y = y
        self.speed = speed
        self.stage = 0
        self.current_goal = 0
        self.path = path
        self.socket_pub = socket_pub
        self.socket_sub = socket_sub
        self.move_callbacks = []

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
        if  self.stage + 1 < len(self.path) and (self.stage <= self.current_goal or self.stage == 0):
            self.stage = self.stage + 1
            self.x = self.path[self.stage][0]
            self.y = self.path[self.stage][1]
            event = com.Event()
            event.robot = self.id
            event.stage = self.stage
            msg = event.SerializeToString()
            self.socket_pub.send("%d %s" % (self.id, msg))
        else:
            print("Robot %d ended move" % self.id)

    def addMoveCallback(self, callback):
        self.move_callbacks.append(callback)

    def recvEvent(self, msg, root):
        event = com.Event()
        event.ParseFromString(msg)
        print("Robot %d should move" % self.id)
        for c in self.move_callbacks:
            if self.current_goal + 1 < len(self.path):
                self.current_goal += 1
                new_pos = self.path[self.current_goal]
                c(root, self.id, new_pos[0], new_pos[1])
                print("Robot %d should move to (%d, %d)" % (self.id,
                                                            new_pos[0],
                                                            new_pos[1]))
            else:
                print("Robot %d ended move" % (self.id))
