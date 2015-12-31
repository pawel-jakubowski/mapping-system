import time as pytime
import Tkinter as tk
from enum import Enum


class Window:
    title = "Mapping system - simulator"
    buttons = []
    frames = {}

    def __init__(self, root):
        self.root = root
        root.title(self.title)
        # root.minsize(width=900, height=780)
        self.addBoard()
        self.addButtons()

    def moveRobots(self, x, y):
        for robot in self.board.robots:
            if x != 0:
                robot.moveX(robot.x + x)
            if y != 0:
                robot.moveY(robot.y + y)

    def addButtons(self):
        self.frames['buttons'] = tk.Frame(self.root)
        self.frames['buttons'].grid(row=0, column=0, sticky=tk.N)
        self.buttons.append(tk.Button(self.frames['buttons'], text="Run"))
        self.buttons.append(
            tk.Button(self.frames['buttons'], text="Up", command=lambda: self.moveRobots(0, -1)))
        self.buttons.append(
            tk.Button(self.frames['buttons'], text="Down", command=lambda: self.moveRobots(0, 1)))
        self.buttons.append(
            tk.Button(self.frames['buttons'], text="Left", command=lambda: self.moveRobots(-1, 0)))
        self.buttons.append(
            tk.Button(self.frames['buttons'], text="Right", command=lambda: self.moveRobots(1, 0)))
        for button in self.buttons:
            button.pack(fill="both")

    def addBoard(self):
        self.frames['canvas'] = tk.Frame(self.root)
        self.frames['canvas'].grid(row=0, column=1)
        self.board = Board(self.frames['canvas'], 20)
        self.board.refresh()


class Board:
    width = 600
    size = 20
    robots_count = 5
    resources = []
    robots = []

    def __init__(self, root, size=size, robots=robots_count):
        self.root = root
        self.canvas = tk.Canvas(root, width=self.width, height=self.width, bg="white smoke")
        self.canvas.pack(fill="both", expand=True)

        self.size = size
        self.px_size = self.width / self.size
        self.robots_size = 0.6 * self.px_size

        self.initResources()
        self.initRobots()

    def initResources(self):
        px_size = self.width / self.size
        for i in range(0, self.size):
            self.resources.append([])
            start_x = i * self.px_size
            end_x = (i + 1) * self.px_size
            for j in range(0, self.size):
                start_y = j * self.px_size
                end_y = (j + 1) * self.px_size
                resource = Resource([start_x, end_x], [start_y, end_y], self.canvas)
                self.resources[i].append(resource)

    def initRobots(self):
        for i in range(0, 6, 2):
            x = i + (self.size / 2) - 3
            y = self.size / 2
            self.resources[x][y].update(ResourceState.base)
            robot = Robot(len(self.robots), x, y, self.robots_size, self, self.canvas)
            self.robots.append(robot)

    def refresh(self):
        self.canvas.delete("all")
        self.drawResources()
        self.drawRobots()

    def drawResources(self):
        for row in self.resources:
            for resource in row:
                resource.draw()
                # resource.drawCenter()
        for i in range(0, 6, 2):
            x = i + (self.size / 2) - 3
            y = self.size / 2
            self.resources[x][y].update(ResourceState.base)

    def drawRobots(self):
        for robot in self.robots:
            robot.draw()


class ResourceState(Enum):
    free = 1
    occupied = 2
    requested = 3
    base = 4


class Resource:
    state = ResourceState.free

    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        center_x = (self.x[1] - self.x[0]) / 2 + self.x[0]
        center_y = (self.y[1] - self.y[0]) / 2 + self.y[0]
        self.center = [center_x, center_y]

    def draw(self, state=ResourceState.free):
        self.state = state
        color = self.getBackgroundColor()
        self.item = self.canvas.create_rectangle(self.x[0], self.y[0], self.x[1], self.y[1],
                                                 outline="black", fill=color)

    def getBackgroundColor(self):
        color = self.canvas["background"]
        if self.state == ResourceState.occupied:
            color = "brown1"
        elif self.state == ResourceState.requested:
            color = "light cyan"
        elif self.state == ResourceState.base:
            color = "snow3"
        return color

    def drawCenter(self):
        r = 1
        center_x = self.center[0]
        center_y = self.center[1]
        self.canvas.create_oval(center_x - r, center_y - r, center_x + r, center_y + r)

    def update(self, state):
        if self.state != ResourceState.base:
            self.state = state
        try:
            color = self.getBackgroundColor()
            self.canvas.itemconfig(self.item, fill=color)
        except AttributeError:
            self.item = None


class Robot:
    shouldAnimate = False
    speed = 2
    color = "light blue"

    def __init__(self, id, x, y, size, board, canvas):
        self.id = id
        self.x = x
        self.y = y
        self.r = size / 2
        self.board = board
        self.canvas = canvas

    def __repr__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def getNewSpeed(self, delta, current_delta):
        if abs(delta - current_delta) >= self.speed:
            if delta < 0:
                return -self.speed
            else:
                return self.speed
        else:
            return delta - current_delta

    def updateResourceDuringAnimation(self, current_delta, resource):
        half_dist = self.board.px_size / 2
        if abs(current_delta) < half_dist:
            resource.update(ResourceState.occupied)
        elif abs(current_delta) - self.r > half_dist:
            resource.update(ResourceState.free)
        if abs(current_delta) + self.r > half_dist:
            self.board.resources[self.x][self.y].update(ResourceState.occupied)

    def animate(self, root, time):
        if self.shouldAnimate:
            speedX = self.getNewSpeed(self.delta[0], self.current_delta[0])
            speedY = self.getNewSpeed(self.delta[1], self.current_delta[1])

            self.current_delta[0] += speedX
            self.current_delta[1] += speedY

            if self.delta[0] < 0:
                resource = self.board.resources[self.x + 1][self.y]
                self.updateResourceDuringAnimation(self.current_delta[0], resource)
            elif self.delta[0] > 0:
                resource = self.board.resources[self.x - 1][self.y]
                self.updateResourceDuringAnimation(self.current_delta[0], resource)

            if self.delta[1] < 0:
                resource = self.board.resources[self.x][self.y + 1]
                self.updateResourceDuringAnimation(self.current_delta[1], resource)
            elif self.delta[1] > 0:
                resource = self.board.resources[self.x][self.y - 1]
                self.updateResourceDuringAnimation(self.current_delta[1], resource)

            # print "[%d] current %s" % (self.id, str(self.current_delta))
            # print "[%d] goal %s" % (self.id, str(self.delta))
            # print "[%d] move %d, %d" % (self.id, speedX, speedY)

            self.canvas.move(self.item, speedX, speedY)
            self.canvas.move(self.label, speedX, speedY)
            self.canvas.update_idletasks()
            pytime.sleep(0.015)
            if abs(self.current_delta[0] - self.delta[0]) == 0 and abs(self.current_delta[1] - self.delta[1]) == 0:
                self.shouldAnimate = False
                self.board.resources[self.x][self.y].update(ResourceState.occupied)
        root.after(time, self.animate, root, time)

    def moveX(self, x):
        if x > self.board.size or x < 0:
            return
        if self.board.resources[x][self.y].state == ResourceState.occupied:
            # print "Robot %d goes to occupied resource [%d, %d]!" % (self.id, x, self.y)
            raise
        # print "[ROBOT %d] move to (%d, %d)" % (self.id, x, self.y)
        self.delta = [(x - self.x) * self.board.px_size, 0]
        # print "[%d] goal %s" % (self.id, str(self.delta))
        self.current_delta = [0, 0]
        self.shouldAnimate = True
        self.x = x

    def moveY(self, y):
        if (y > self.board.size or y < 0):
            return
        if self.board.resources[self.x][y].state == ResourceState.occupied:
            # print "Robot %d goes to occupied resource [%d, %d]!" % (self.id, self.x, y)
            raise
        # print "[ROBOT %d] move to (%d, %d)" % (self.id, self.x, y)
        self.delta = [0, (y - self.y) * self.board.px_size]
        self.current_delta = [0, 0]
        self.shouldAnimate = True
        self.y = y

    def draw(self):
        x = self.board.resources[self.x][self.y].center[0]
        y = self.board.resources[self.x][self.y].center[1]
        self.item = self.canvas.create_oval(
            x - self.r, y - self.r, x + self.r, y + self.r, fill=self.color)
        self.label = self.canvas.create_text(x, y)
        self.canvas.itemconfig(self.label, text=str(self.id))
        self.board.resources[self.x][self.y].update(ResourceState.occupied)

    # def goTo(self, point)
