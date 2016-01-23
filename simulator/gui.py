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
    self.board.robots[id].moveX(x)
    self.board.robots[id].moveY(y)

  def moveRobots(self, x, y):
    for key in self.board.robots:
      if x != 0:
        self.board.robots[key].moveX(self.board.robots[key].x + x)
      if y != 0:
        self.board.robots[key].moveY(self.board.robots[key].y + y)

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

  def addRobot(self, robotId, x, y, speed = 5):
    assert x >= 0 and x < self.size, "x must be inside board!"
    assert y >= 0 and y < self.size, "y must be inside board!"
    self.robots[robotId] = Robot(robotId, x, y, self.robots_size, self, self.canvas)
    self.robots[robotId].speed = speed
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
  speed = 5
  color = "light blue"

  def __init__(self, id, x, y, size, board, canvas):
    self.id = id
    self.x = self.end_x = x
    self.y = self.end_y = y
    self.r = size / 2
    self.board = board
    self.canvas = canvas
    self.current_delta = [0, 0]
    self.movements_queue = []
    self.event_callback = lambda : True

  def __repr__(self):
    return "[" + str(self.x) + ", " + str(self.y) + "]"

  def setEventCallback(self, callback):
    self.event_callback = lambda : callback(self.id)

  def moveOnCanvas(self, delta_x, delta_y):
    self.canvas.move(self.item, delta_x, delta_y)
    self.canvas.move(self.label, delta_x, delta_y)
    self.canvas.update_idletasks()
    pytime.sleep(0.025 / self.speed)

  def animate(self, root, time):
    if hasattr(self, 'animation'):
      self.animation.update()
      if self.animation.isFinished():
        self.movements_queue.pop(0)
        del self.animation
    elif len(self.movements_queue) > 0:
      movement = self.movements_queue[0]
      current_resource = self.board.resources[movement.start_point[0]][movement.start_point[1]]
      future_resource = self.board.resources[movement.desired_point[0]][movement.desired_point[1]]
      self.animation = self.Animation(movement, current_resource, future_resource, self.board.px_size, self)
    root.after(time, self.animate, root, time)

  def moveX(self, x):
    if x > self.board.size or x < 0:
      return
    movement = self.Movement([self.end_x, self.end_y], [x, self.end_y], self.board.px_size)
    self.movements_queue.append(movement)
    self.end_x = x

  def moveY(self, y):
    if (y > self.board.size or y < 0):
      return
    movement = self.Movement([self.end_x, self.end_y], [self.end_x, y], self.board.px_size)
    self.movements_queue.append(movement)
    self.end_y = y

  def draw(self):
    x = self.board.resources[self.x][self.y].center[0]
    y = self.board.resources[self.x][self.y].center[1]
    self.item = self.canvas.create_oval(
      x - self.r, y - self.r, x + self.r, y + self.r, fill=self.color)
    self.label = self.canvas.create_text(x, y)
    self.canvas.itemconfig(self.label, text=str(self.id))
    self.board.resources[self.x][self.y].update(ResourceState.occupied)

  class Movement:
    def __init__(self, start_point, desired_point, px_size):
      self.start_point = start_point
      self.desired_point = desired_point
      self.delta = [
        (desired_point[0] - start_point[0]) * px_size,
        (desired_point[1] - start_point[1]) * px_size
      ]

  class Animation:
    def __init__(self, movement, current_resource, future_resource, px_size, robot):
#      if future_resource.state == ResourceState.occupied:
#        raise
      self.delta = movement.delta
      self.start_point = movement.start_point
      self.desired_point = movement.desired_point
      self.current_resource = current_resource
      self.future_resource = future_resource
      self.current_delta = [0, 0]
      self.px_size = px_size
      self.robot = robot

    def update(self):
      if self.delta[0] != 0:
        self.current_delta[0], delta = self.updatePosition(self.delta[0], self.current_delta[0])
        self.robot.moveOnCanvas(delta, 0)
      if self.delta[1] != 0:
        self.current_delta[1], delta = self.updatePosition(self.delta[1], self.current_delta[1])
        self.robot.moveOnCanvas(0, delta)

    def isFinished(self):
      return \
        abs(self.current_delta[0] - self.delta[0]) == 0 and \
        abs(self.current_delta[1] - self.delta[1]) == 0

    def updatePosition(self, delta, current_delta):
      step_delta = self.getStepDelta(delta, current_delta)
      current_delta += step_delta
      self.updateResource(current_delta)
      return current_delta, step_delta

    def updateResource(self, current_delta):
      half_dist = self.px_size / 2
      if abs(current_delta) < half_dist:
        self.current_resource.update(ResourceState.occupied)
      elif abs(current_delta) - self.robot.r > half_dist:
        self.robot.event_callback()
        self.current_resource.update(ResourceState.free)
      if abs(current_delta) + self.robot.r > half_dist:
        self.robot.x = self.desired_point[0]
        self.robot.y = self.desired_point[1]
        self.future_resource.update(ResourceState.occupied)

    def getStepDelta(self, delta, current_delta):
      step_delta = int(self.px_size / 10)
      step_delta = 1 if step_delta <= 0 else step_delta
      if abs(delta - current_delta) >= step_delta:
        if delta < 0:
          return -step_delta
        else:
          return step_delta
      else:
        return delta - current_delta
