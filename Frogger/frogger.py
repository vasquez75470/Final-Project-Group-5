from graphics import*
import random
import math

WIN_TITLE = "Frogger"
WIN_WIDTH = 448
WIN_HEIGHT = 512
TILE_SIZE = 32
UPDATE_RATE = 30
GREEN_GRASS_XSIZE = 96
GREEN_GRASS_YSIZE = 48

carList = []
trunkList = []
turtleList = []
frogPointList = []

class Rect():
    def __init__(self, point1, point2, color, win):
        self.point1 = point1
        self.point2 = point2
        self.color = color
        self.win = win
        self.rectangle = Rectangle(point1, point2)

    def draw(self):
        self.rectangle.setFill(self.color)
        self.rectangle.setOutline(self.color)
        self.rectangle.draw(self.win)

class Health():
    def __init__(self, health, win):
        self.health = health
        self.win = win
        self.image1 = Image(Point(TILE_SIZE/2, WIN_HEIGHT - TILE_SIZE/2), "FrogUp1.png")
        self.image2 = Image(Point(TILE_SIZE + TILE_SIZE/2, WIN_HEIGHT - TILE_SIZE/2), "FrogUp1.png")

    def draw(self):
        if self.health >= 2: self.image1.draw(self.win)
        if self.health >= 3: self.image2.draw(self.win)
        
    def undraw(self):
        self.image1.undraw()
        self.image2.undraw()

class Time():
    def __init__(self, time, factor, win):
        self.point1 = Point(WIN_WIDTH - 2*TILE_SIZE, WIN_HEIGHT - TILE_SIZE + 8)
        self.point2 = Point(WIN_WIDTH - 2*TILE_SIZE, WIN_HEIGHT - 6)
        self.time = time
        self.counter = 0
        self.factor = factor
        self.win = win
        self.rectangle = Rectangle(Point(self.point1.x - time*factor, self.point1.y), self.point2)

    def draw_text(self):
        message = Text(Point(WIN_WIDTH - TILE_SIZE, WIN_HEIGHT - TILE_SIZE/2 + 2), 'TIME')
        message.setSize(16)
        message.setFace('helvetica')
        message.setTextColor("yellow")
        message.draw(self.win)
    
    def draw(self):
        self.rectangle.setFill("lime")
        self.rectangle.setOutline("lime")
        self.rectangle.draw(self.win)

    def undraw(self):
        self.rectangle.undraw()

    def change_time(self):
        self.time -= 0.5
        self.undraw()
        self.point1 = Point(self.point2.x - self.time*self.factor, self.point1.y)
        self.rectangle = Rectangle(self.point1, self.point2)
        if self.time >= 0: self.draw()
        return self.get_time_over()

    def get_time_over(self):
        if self.time <= 0: return True
        else: return False

    def update(self):
        self.counter += 1
        time_finished = False
        if self.counter % (UPDATE_RATE/2) == 0:
            self.counter = 0
            time_finished = self.change_time()
        return time_finished

class FrogPoint():
    def __init__(self, xPos, yPos, win):
        self.xPos = xPos
        self.yPos = yPos
        self.win = win
        self.is_draw = False
        self.image = Image(Point(xPos + TILE_SIZE/2, yPos + TILE_SIZE/2), "FrogPoint.png")
        self.rect = Rectangle(Point(xPos, yPos), Point(xPos + TILE_SIZE, yPos + TILE_SIZE))

    def collision_detected(self, frog):
        frogCenterX = frog.xPos + TILE_SIZE/2
        frogCenterY = frog.yPos + TILE_SIZE/2
        if self.is_draw == True: return False
        if frogCenterX > self.xPos and frogCenterX < self.xPos + TILE_SIZE and \
           frogCenterY > self.yPos and frogCenterY < self.yPos + TILE_SIZE: return True
        return False

    def draw(self):
        self.image.draw(self.win)
        self.is_draw = True
    def undraw(self): self.image.undraw()
    
class Frog():
    def __init__(self, xPos, yPos, xDir, yDir, health, win):
        self.xPos = xPos
        self.yPos = yPos
        self.xDir = xDir
        self.yDir = yDir
        self.health = health
        self.win = win
        self.image = Image(Point(xPos + TILE_SIZE/2, yPos + TILE_SIZE/2), "FrogUp0.png")

    def handle_input(self):
        key = self.win.checkKey()
        self.xDir = 0
        self.yDir = 0
        if key == "Right": self.xDir = 1
        elif key == "Left": self.xDir = -1
        elif key == "Down": self.yDir = 1
        elif key == "Up": self.yDir = -1
        return self.xDir != 0 or self.yDir != 0
    
    def can_move(self): return not(self.yDir == 1 and self.yPos >= WIN_HEIGHT - 2*TILE_SIZE)

    def move_horizontal(self, xDir, speed):
        self.xPos += xDir * speed / UPDATE_RATE
        self.image.move(xDir * speed / UPDATE_RATE, 0)

    def move(self):
        self.xPos += self.xDir * TILE_SIZE
        self.yPos += self.yDir * TILE_SIZE
        self.image.move(self.xDir * TILE_SIZE, self.yDir * TILE_SIZE)

    def change_sprite(self):
        self.undraw()
        if self.xDir == -1: self.image = Image(Point(self.xPos + TILE_SIZE/2, self.yPos + TILE_SIZE/2), "FrogLeft0.png")
        if self.xDir == 1: self.image = Image(Point(self.xPos + TILE_SIZE/2, self.yPos + TILE_SIZE/2), "FrogRight0.png")
        if self.yDir == -1: self.image = Image(Point(self.xPos + TILE_SIZE/2, self.yPos + TILE_SIZE/2), "FrogUp0.png")
        if self.yDir == 1: self.image = Image(Point(self.xPos + TILE_SIZE/2, self.yPos + TILE_SIZE/2), "FrogDown0.png")
        self.draw()
        
    def draw(self): self.image.draw(self.win)
    def undraw(self): self.image.undraw()

    def redraw(self):
        self.undraw()
        self.draw()

    def update(self):
        if self.handle_input() and self.can_move():
            self.move()
            self.change_sprite()
        
class Turtle():
    def __init__(self, xPos, yPos, speed, is_red, win):
        self.xPos = xPos
        self.yPos = yPos
        self.speed = speed
        self.is_red = is_red
        self.max_frame = 3 if is_red else 8
        self.image_name = "TurtleRed"if is_red else "TurtleGreen"
        self.frame_count = 0
        self.frame_max_rate_speed = 8
        self.frame_rate_speed = 0
        self.win = win
        self.image = Image(Point(xPos + TILE_SIZE/2, yPos + TILE_SIZE/2), self.image_name + str(self.frame_count) + ".png")

    def move_horizontal(self):
        self.xPos -= self.speed / UPDATE_RATE
        self.image.move(-self.speed / UPDATE_RATE, 0)
        
    def wrap_position(self):
        if self.xPos < -2*TILE_SIZE:
            self.xPos += 16 * TILE_SIZE
            self.image.move(16 * TILE_SIZE, 0)

            
    def draw(self): self.image.draw(self.win)
    def undraw(self): self.image.undraw()

    def collision_detected(self, frog):
        offset = 16
        if self.frame_count >= self.max_frame - 1 and self.is_red == False: return False
        if frog.xPos + TILE_SIZE > self.xPos + offset and frog.xPos < self.xPos + TILE_SIZE - offset and \
           frog.yPos + TILE_SIZE > self.yPos + offset and frog.yPos < self.yPos + TILE_SIZE - offset: return True
        return False

    def animation(self):
        self.frame_rate_speed += 1
        if self.frame_rate_speed >= self.frame_max_rate_speed:
            self.frame_rate_speed = 0
            self.frame_count += 1
            self.frame_count = self.frame_count % self.max_frame
            self.undraw()
            self.image = Image(Point(self.xPos + TILE_SIZE/2, self.yPos + TILE_SIZE/2), self.image_name + str(self.frame_count) + ".png")
            self.draw()
            return True
        return False
            
    def update(self):
        frame_changed = self.animation()
        self.move_horizontal()
        self.wrap_position()
        return frame_changed
            
class Car():
    def __init__(self, xPos, yPos, direction, speed, carNumber, carTiles, win):
        self.xPos = xPos
        self.yPos = yPos
        self.direction = direction
        self.speed = speed
        self.carNumber = carNumber
        self.carTiles = carTiles
        self.win = win
        self.image = Image(Point(xPos + carTiles * TILE_SIZE/2, yPos + TILE_SIZE/2), "Car" + str(carNumber) + ".png")

    def undraw(self): self.image.undraw()
    def draw(self): self.image.draw(self.win)

    def move_horizontal(self):
        self.xPos += self.speed * self.direction / UPDATE_RATE
        self.image.move(self.speed * self.direction / UPDATE_RATE, 0)
        
    def wrap_position(self):
        if self.direction == 1 and self.xPos > WIN_WIDTH:
            self.xPos -= 16 * TILE_SIZE
            self.image.move(-16 * TILE_SIZE, 0)
        elif self.direction == -1 and self.xPos < -self.carTiles * TILE_SIZE:
            self.xPos += 16 * TILE_SIZE
            self.image.move(16 * TILE_SIZE, 0)

    def collision_detected(self, frog):
        offset = 6
        if frog.xPos + TILE_SIZE > self.xPos + offset and frog.xPos < self.xPos + self.carTiles*TILE_SIZE - offset and \
           frog.yPos + TILE_SIZE > self.yPos + offset and frog.yPos < self.yPos + TILE_SIZE - offset: return True
        return False

    def update(self):
        self.move_horizontal()
        self.wrap_position()

class Trunk():
    def __init__(self, xPos, yPos, speed, trunkNumber, trunkTiles, win):
        self.xPos = xPos
        self.yPos = yPos
        self.speed = speed
        self.trunkNumber = trunkNumber
        self.trunkTiles = trunkTiles
        self.win = win
        self.image = Image(Point(xPos + trunkTiles*TILE_SIZE/2, yPos + TILE_SIZE/2), "Trunk" + str(trunkNumber) + ".png")

    def undraw(self): self.image.undraw()
    def draw(self): self.image.draw(self.win)

    def move_horizontal(self):
        self.xPos += self.speed / UPDATE_RATE
        self.image.move(self.speed / UPDATE_RATE, 0)
        
    def wrap_position(self):
        if self.xPos > WIN_WIDTH:
            self.xPos -= 20 * TILE_SIZE
            self.image.move(-20 * TILE_SIZE, 0)

    def collision_detected(self, frog):
        offset = 20
        if frog.xPos + TILE_SIZE > self.xPos + offset and frog.xPos < self.xPos + self.trunkTiles*TILE_SIZE - offset and \
           frog.yPos + TILE_SIZE > self.yPos + offset and frog.yPos < self.yPos + TILE_SIZE - offset: return True
        return False
    
    def update(self):
        self.move_horizontal()
        self.wrap_position()

def create_background(win):
    waterRectangle = Rect(Point(0,0), Point(WIN_WIDTH, WIN_HEIGHT/2 + TILE_SIZE/2), "#00044b", win)
    waterRectangle.draw()
    
    streetRectangle = Rect(Point(0,WIN_HEIGHT/2 + TILE_SIZE/2), Point(WIN_WIDTH, WIN_HEIGHT), "#010001", win)
    streetRectangle.draw()

    
    for i in range(math.ceil(WIN_WIDTH/TILE_SIZE)):
        purpleTopGrass = Image(Point(i * TILE_SIZE + TILE_SIZE/2, 8 * TILE_SIZE + TILE_SIZE/2), "PurpleGrass.png")
        purpleTopGrass.draw(win)
        
        purpleBottomGrass = Image(Point(i * TILE_SIZE + TILE_SIZE/2, 14 * TILE_SIZE + TILE_SIZE/2), "PurpleGrass.png")
        purpleBottomGrass.draw(win)

    for i in range(math.ceil(WIN_WIDTH/GREEN_GRASS_XSIZE)):
        greenGrass = Image(Point(i * GREEN_GRASS_XSIZE + GREEN_GRASS_XSIZE/2, 1.5 * TILE_SIZE + GREEN_GRASS_YSIZE/2), "GreenGrass.png")
        greenGrass.draw(win)

def create_turtle(win):
    tList = []
    #TurleLine 1
    tileDistance = 5
    firstPos = random.uniform(0, tileDistance-2 * TILE_SIZE)
    for i in range(6):
        redTurtle = True if i < 4 else False
        xPos = (firstPos + TILE_SIZE*(i%2)) + (tileDistance * TILE_SIZE * math.floor(i/2))
        turtle = Turtle(xPos, 4 * TILE_SIZE, 1.25 * TILE_SIZE, redTurtle, win)
        turtle.draw()
        tList.append(turtle)

    #TurtleLine 2
    tileDistance = 5
    firstPos = random.uniform(0, tileDistance-2 * TILE_SIZE)
    for i in range(9):
        redTurtle = True if i < 3 or i > 5 else False
        xPos = (firstPos + TILE_SIZE*(i%3)) + (tileDistance * TILE_SIZE * math.floor(i/3))
        turtle = Turtle(xPos, 7 * TILE_SIZE, 4 * TILE_SIZE, redTurtle, win)
        turtle.draw()
        tList.append(turtle)
        
    return tList

def create_cars(win):
    cList = []
    # CAR 1
    tilesDistance = 4
    firstPos = random.uniform(0, tilesDistance-1 * TILE_SIZE)
    for i in range(4):
        car = Car(firstPos + (tilesDistance * TILE_SIZE * i), 11 * TILE_SIZE, -1, 2*TILE_SIZE, 1, 1, win)
        car.draw()
        cList.append(car)

    # CAR 2
    tilesDistance = 4
    firstPos = random.uniform(0, tilesDistance-1 * TILE_SIZE)
    for i in range(4):
        car = Car(firstPos + (tilesDistance * TILE_SIZE * i), 13 * TILE_SIZE, -1, 2*TILE_SIZE, 2, 1, win)
        car.draw()
        cList.append(car)

    # CAR 3
    tilesDistance = 3
    firstPos = random.uniform(0, 12 * TILE_SIZE)
    for i in range(2):
        car = Car(firstPos + (tilesDistance * TILE_SIZE * i), 10*TILE_SIZE, 1, 7.5*TILE_SIZE, 3, 1, win)
        car.draw()
        cList.append(car)
        
    # CAR 4
    tilesDistance = 4
    firstPos = random.uniform(0, tilesDistance-1 * TILE_SIZE)
    for i in range(4):
        car = Car(firstPos + (tilesDistance * TILE_SIZE * i), 12*TILE_SIZE, 1, 1.25*TILE_SIZE, 4, 1, win)
        car.draw()
        cList.append(car)

    # CAR 5
    tilesDistance = 5
    firstPos = random.uniform(0, (tilesDistance-1) * TILE_SIZE)
    for i in range(3):
        car = Car(firstPos + (tilesDistance * TILE_SIZE * i), 9*TILE_SIZE, -1, 1.25*TILE_SIZE, 5, 2, win)
        car.draw()
        cList.append(car)
    return cList

def create_trunks(win):
    tList = []
    # TRUNK 1
    tilesDistance = 5
    firstPos = random.uniform(0, (tilesDistance-3) * TILE_SIZE)
    for i in range(4):
        trunk = Trunk(firstPos + (tilesDistance * TILE_SIZE * i), 6*TILE_SIZE, 0.75*TILE_SIZE, 1, 3, win)
        trunk.draw()
        tList.append(trunk)

    # TRUNK 2
    tilesDistance = 5
    firstPos = random.uniform(0, (tilesDistance-3) * TILE_SIZE)
    for i in range(4):
        trunk = Trunk(firstPos + (tilesDistance * TILE_SIZE * i), 3*TILE_SIZE, 1.75*TILE_SIZE, 2, 4, win)
        trunk.draw()
        tList.append(trunk)

    # TRUNK 3
    tilesDistance = 8
    firstPos = random.uniform(0, (tilesDistance-1) * TILE_SIZE)
    for i in range(2):
        trunk = Trunk(firstPos + (tilesDistance * TILE_SIZE * i), 5*TILE_SIZE, 1.75*TILE_SIZE, 3, 6, win)
        trunk.draw()
        tList.append(trunk)
        
    return tList

def create_frogPoint(win):
    fpList = []
    xOffset = TILE_SIZE/2

    for i in range(5):
        frogPoint = FrogPoint(xOffset + (i*3*TILE_SIZE),2*TILE_SIZE, win)
      #  frogPoint.draw()
        fpList.append(frogPoint)

    return fpList

def main():
    win = GraphWin(WIN_TITLE, WIN_WIDTH, WIN_HEIGHT)
    create_background(win)
    game_over = False
    health_count = 3
    frogPointList = create_frogPoint(win)
    
    while(game_over != True):
        carList = create_cars(win)
        trunkList = create_trunks(win)
        turtleList = create_turtle(win)
        frog = Frog(WIN_WIDTH / 2 - TILE_SIZE / 2, WIN_HEIGHT - 2*TILE_SIZE, -1, 0, health_count, win)
        frog.draw()
        health = Health(frog.health, win)
        health.draw()
        time = Time(25, 5, win)
        time.draw()
        time.draw_text()
        collided = False
        
        while(collided != True):
            frame_changed = False
            collided = False
            on_trunk = False
            on_turtle = False
            on_point = False

            collided = time.update()
            frog.update()
            for point in frogPointList:
                if point.collision_detected(frog):
                    point.draw()
                    on_point = True
            
            for car in carList:
                car.update()
                if car.collision_detected(frog): collided = True
                
            for trunk in trunkList:
                trunk.update()
                if trunk.collision_detected(frog):
                    on_trunk = True
                    frog.move_horizontal(1, trunk.speed)
                
            for turtle in turtleList:
                frame_changed = turtle.update()
                if turtle.collision_detected(frog):
                    on_turtle = True
                    frog.move_horizontal(-1, turtle.speed)

            if frame_changed: frog.redraw()
            if (frog.yPos < 8 * TILE_SIZE and (on_trunk == False and on_turtle == False)) or\
               (frog.xPos + TILE_SIZE < 0 or frog.xPos > WIN_WIDTH): collided = True
                
            if collided or on_point:
                for car in carList: car.undraw()
                for trunk in trunkList: trunk.undraw()
                for turtle in turtleList: turtle.undraw()
                frog.undraw()
                health.undraw()
                carList.clear()
                trunkList.clear()
                turtleList.clear()
                if on_point == False:
                    health_count -= 1
                    if health_count <= 0:
                        game_over = True
            update(UPDATE_RATE)
    message = Text(Point(WIN_WIDTH / 2, WIN_HEIGHT * 2/5), 'G A M E   O V E R')
    message.setSize(32)
    message.setFace('helvetica')
    message.setTextColor("red")
    message.draw(win)
    win.getKey()
    win.close()

main()
