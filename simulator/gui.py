import time as pytime
import Tkinter as tk
from enum import Enum


class Window:
  title = "Mapping system - simulator"
  buttons = []
  frames = {}

  def __init__(self, root):
    self.root = root
    root.window = self
    root.title(self.title)
    # root.minsize(width=900, height=780)
    self.addButtons()

  def moveRobot(self, id, x, y):
    if x != 0:
      self.board.robots[id].moveX(x)
    if y != 0:
      self.board.robots[id].moveY(y)

  def moveRobots(self, x, y):
    for key in self.board.robots:
      if x != 0:
        self.board.robots[key].moveX(robot.x + x)
      if y != 0:
        self.board.robots[key].moveY(robot.y + y)

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

  def addBoard(self, size):
    self.frames['canvas'] = tk.Frame(self.root)
    self.frames['canvas'].grid(row=0, column=1)
    self.board = Board(self.frames['canvas'], size)
    self.board.refresh()

  def __repr__(self):
    str = "Window is not initialized!"
    if hasattr(self, "board"):
      str = "Board size: %d\n" % self.board.size
      str += "Robots: %d\n" % self.board.robots_count
      str += "Robots coordinates:\n"
      str += "[" + ", ".join(repr(x) for x in self.board.robots) + "]"
    return str


class Board:
  width = 600
  size = 20
  robots_count = 5
  resources = []
  robots = {}

  def __init__(self, root, size=size, robots=robots_count):
    self.root = root
    self.canvas = tk.Canvas(root, width=self.width, height=self.width, bg="white smoke")
    self.canvas.pack(fill="both", expand=True)

    self.size = size
    self.px_size = self.width / self.size
    self.robots_size = 0.6 * self.px_size

    self.initResources()

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

  def setBase(self, minPoint, maxPoint):
    assert minPoint[0] >= 0 and minPoint[1] >= 0, "minPoint must be inside board!"
    assert maxPoint[0] < self.size and maxPoint[1] < self.size, "maxPoint must be inside board!"
    assert minPoint[0] <= maxPoint[0] and minPoint[1] <= maxPoint[1], "minPoint must be less or equal maxPoint"
    print "Base:"
    for x in range(minPoint[0], maxPoint[0]+1):
      for y in range(minPoint[1], maxPoint[1]+1):
        self.resources[x][y].update(ResourceState.base)

  def addRobot(self, robotId, x, y):
    assert x >= 0 and x < self.size, "x must be inside board!"
    assert y >= 0 and y < self.size, "y must be inside board!"
    self.robots[robotId] = Robot(robotId, x, y, self.robots_size, self, self.canvas)
    time = 1
    self.root.after(time, self.robots[robotId].animate, self.root, time)

  def refresh(self):
    self.canvas.delete("all")
    self.drawResources()
    self.drawRobots()

  def drawResources(self):
    for row in self.resources:
      for resource in row:
        resource.draw()
        # resource.drawCenter()

  def drawRobots(self):
    for key in self.robots:
      self.robots[key].draw()


class ResourceState(Enum):
  free = 1
  occupied = 2
  requested = 3
  base = 4


class Resource:
  state = ResourceState.free

  def __init__(self, x, y, canvas, state=ResourceState.free):
    self.x = x
    self.y = y
    self.canvas = canvas
    center_x = (self.x[1] - self.x[0]) / 2 + self.x[0]
    center_y = (self.y[1] - self.y[0]) / 2 + self.y[0]
    self.center = [center_x, center_y]
    self.state = state

  def draw(self):
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
  speed = 1
  color = "light blue"

  def __init__(self, id, x, y, size, board, canvas):
    self.id = id
    self.x = self.endX = x
    self.y = self.endY = y
    self.r = size / 2
    self.board = board
    self.canvas = canvas
    self.current_delta = [0, 0]
    self.movementsQueue = []
    self.event_callback = lambda : (_ for _ in ()).throw(Exception("Callback for robot " + str(self.id) + " was not set!"))

  def __repr__(self):
    return "[" + str(self.x) + ", " + str(self.y) + "]"

  def setEventCallback(self, callback):
    self.event_callback = lambda : callback(self.id)

  def moveOnCanvas(self, speedX, speedY):
    self.canvas.move(self.item, speedX, speedY)
    self.canvas.move(self.label, speedX, speedY)
    self.canvas.update_idletasks()
    pytime.sleep(0.025)

  def animate(self, root, time):
    if hasattr(self, 'animation'):
      self.animation.update(self.speed)
      if self.animation.isFinished():
        self.movementsQueue.pop(0)
        del self.animation
    elif len(self.movementsQueue) > 0:
      movement = self.movementsQueue[0]
      currentResource = self.board.resources[movement.startPoint[0]][movement.startPoint[1]]
      futureResource = self.board.resources[movement.desiredPoint[0]][movement.desiredPoint[1]]
      self.animation = self.Animation(movement, currentResource, futureResource, self.board.px_size, self)
    root.after(time, self.animate, root, time)

  def moveX(self, x):
    if x > self.board.size or x < 0:
      return
    movement = self.Movement([self.endX, self.endY], [x, self.endY], self.board.px_size)
    self.movementsQueue.append(movement)
    self.endX = x

  def moveY(self, y):
    if (y > self.board.size or y < 0):
      return
    movement = self.Movement([self.endX, self.endY], [self.endX, y], self.board.px_size)
    self.movementsQueue.append(movement)
    self.endY = y

  def draw(self):
    x = self.board.resources[self.x][self.y].center[0]
    y = self.board.resources[self.x][self.y].center[1]
    self.item = self.canvas.create_oval(
      x - self.r, y - self.r, x + self.r, y + self.r, fill=self.color)
    self.label = self.canvas.create_text(x, y)
    self.canvas.itemconfig(self.label, text=str(self.id))
    self.board.resources[self.x][self.y].update(ResourceState.occupied)

  class Movement:
    def __init__(self, startPoint, desiredPoint, px_size):
      self.startPoint = startPoint
      self.desiredPoint = desiredPoint
      self.delta = [
        (desiredPoint[0] - startPoint[0]) * px_size,
        (desiredPoint[1] - startPoint[1]) * px_size
      ]

  class Animation:
    def __init__(self, movement, currentResource, futureResource, px_size, robot):
      if futureResource.state == ResourceState.occupied:
        raise
      self.delta = movement.delta
      self.startPoint = movement.startPoint
      self.desiredPoint = movement.desiredPoint
      self.currentResource = currentResource
      self.futureResource = futureResource
      self.current_delta = [0, 0]
      self.px_size = px_size
      self.robot = robot

    def update(self, speed):
      if self.delta[0] != 0:
        self.current_delta[0], speed = self.updatePosition(speed, self.delta[0], self.current_delta[0])
        self.robot.moveOnCanvas(speed, 0)
      if self.delta[1] != 0:
        self.current_delta[1], speed = self.updatePosition(speed, self.delta[1], self.current_delta[1])
        self.robot.moveOnCanvas(0, speed)

    def isFinished(self):
      return \
        abs(self.current_delta[0] - self.delta[0]) == 0 and \
        abs(self.current_delta[1] - self.delta[1]) == 0

    def updatePosition(self, speed, delta, current_delta):
      speed = self.getNewSpeed(speed, delta, current_delta)
      current_delta += speed
      self.updateResource(current_delta)
      return current_delta, speed

    def updateResource(self, current_delta):
      half_dist = self.px_size / 2
      if abs(current_delta) < half_dist:
        self.currentResource.update(ResourceState.occupied)
      elif abs(current_delta) - self.robot.r > half_dist:
        self.robot.event_callback()
        self.currentResource.update(ResourceState.free)
      if abs(current_delta) + self.robot.r > half_dist:
        self.robot.x = self.desiredPoint[0]
        self.robot.y = self.desiredPoint[1]
        self.futureResource.update(ResourceState.occupied)

    def getNewSpeed(self, speed, delta, current_delta):
      if abs(delta - current_delta) >= speed:
        if delta < 0:
          return -speed
        else:
          return speed
      else:
        return delta - current_delta
