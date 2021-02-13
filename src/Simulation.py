# *neode.onsave* setgo python3 Simulation.py
import pygame as pg
from pygame.locals import *
import math
import random
from pygame.math import Vector2
import time

room = pg.image.load('room.bmp')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
START = (350,250)
UP = Vector2(0,-1)
DOWN = Vector2(0,1)
RIGHT = Vector2(1,0)
LEFT = Vector2(-1,0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500


class Robot(pg.sprite.Sprite):

    def __init__(self, pos=(420, 420), originalspeed=2):
        super(Robot, self).__init__()
        self.radius = 25
        self.image = pg.Surface((50, 50), pg.SRCALPHA)
        pg.draw.circle(self.image, BLACK, (25, 25), self.radius, 0)
        self.maxspeed = 0.5
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos)
        self.oldposition = Vector2(pos)
        self.direction = Vector2(UP)  # A unit vector pointing upward.
        self.speed = 0
        self.angle_speed = 1
        self.angle = 0
        self.is_colliding = False
        self.angle_change = 0
        self.turning = False

    def reset(self):
        self.speed = self.maxspeed
        self.angle_speed = 1
        self.angle = 0
        self.is_colliding = False
        self.angle_change = 0
        self.turning = False

    def turn(self, x):
            self.turning = True
            self.angle_change = x

    def is_finished_turning(self):
        return not self.turning

    def update(self):
        if (self.angle_change > 0):
            # Rotate the direction vector and then the image.
            self.angle_change -= math.copysign(self.angle_speed, self.angle_change)
            self.direction.rotate_ip(self.angle_speed)
            if(self.angle_change < 0):
                self.angle_change = 0

        if (self.angle_change < 0):
            self.angle_change -= math.copysign(self.angle_speed, self.angle_change)
            self.direction.rotate_ip(-self.angle_speed)
            if(self.angle_change > 0):
                self.angle_change = 0

        if (self.angle_change == 0):
            self.turning = False
            # self.angle += self.angle_speed
        self.image = pg.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
            # print(self.angle_change)
        # Update the position vector and the rect.
        self.oldposition = self.position
        # print('self direction = ' + str(self.direction))
        # print (self.direction)
        self.direction = self.direction.normalize()

        # print(self.direction)

        self.position += self.direction * self.speed
        self.rect.center = self.position
        # if (self.angle_change == 0):
        #     self.direction[0] = round(self.direction[0])
        #     print('direction is = ' + str(self.direction))
        #     self.direction[1] = round(self.direction[1])
        #     print('direction is = ' + str(self.direction))
class Algoritm():

    def __init(self):
        self.name = 'No algorithm chosen'

    def apply(self, robot):
        pass

    def setup(self, robot):
        robot.speed = 2

class Boustrophedon(Algoritm):



    def __init__(self):
        self.count = 0
        self.reversing = 0
        self.short = 0
        self.timetoreverse = 5
        self.turning = False

        self.name = 'Boustrophedon'


    def setup(self, robot):
        robot.speed = robot.maxspeed
        robot.direction = UP


    def apply(self, robot):
        # print (str(self.lastydirection))
        if (robot.is_colliding):
            self.reversing = self.timetoreverse
            self.count += 1
            robot.speed = -(robot.maxspeed)

        if self.turning and robot.is_finished_turning():
            # print("Finished turning.")
            self.turning = False
            robot.speed = robot.maxspeed


        if self.reversing > 0:
            self.reversing = self.reversing + robot.speed
            if self.reversing <= 0:
                # print('stopped reversing')
                self.reversing = 0
                robot.speed = 0
                if (self.count % 2 == 0):
                    robot.turn(-90)
                    self.turning = True
                    self.short = self.timetoreverse *12
                else:
                    robot.turn(90)
                    self.turning = True
                    self.short = self.timetoreverse *12

        if self.short > 0:
            self.short = self.short - robot.speed
            # print('hamnar jag har')
            if self.short <= 0:
                # print('stopped short')
                self.short = 0
                robot.speed = 0
                if (self.count % 2 == 0):
                    robot.turn(-90)
                    self.turning = True
                else:
                    robot.turn(90)
                    self.turning = True

#Spiral algorithm
class Spiral(Algoritm):

    def __init__(self):
        self.name = 'Spiral'

    def setup(self, robot):
        robot.speed = robot.maxspeed
        robot.angle = 100

    def apply(self, robot):

        robot.angle_change = 100
        robot.angle_speed -= 0.1 * pow(robot.angle_speed / 10.0, 2.1)
        if (robot.is_colliding):
            robot.speed = 0

class Spiral_and_Wfoll(Algoritm):

    def __init__(self):
        self.name = 'Spiral+wfoll'
        self.algorithm = Spiral()
        self.reversing = 0
        self.timetoreverse = 50

    def setup(self, robot):
        self.algorithm.setup(robot)

    def apply(self, robot):
        if (type(self.algorithm) == Spiral and robot.is_colliding):
            # self.reversing = self.timetoreverse
            # robot.angle_speed = 0
            # robot.speed = -(robot.maxspeed)
            self.algorithm = Wall_follow()
            self.algorithm.setup(robot)
        # if (type(self.algorithm) == Wall_follow and self.algorithm.count == 500):
        #     self.algorithm = Random_walk()
            self.algorithm.setup(robot)

        if self.reversing > 0:
            self.reversing = self.reversing + robot.speed
            if self.reversing <= 0:
                self.algorithm = Wall_follow()
                self.algorithm.setup(robot)


        self.algorithm.apply(robot)




class Random_walk(Algoritm):

    def __init__(self):
        self.name = 'Random Walk'
        self.reversing = 0
        self.timetoreverse = 20
        self.turning = False


    def setup(self, robot):
        robot.speed = robot.maxspeed



    def apply(self, robot):
        if (robot.is_colliding):
            # print('here?')
            self.reversing = self.timetoreverse
            # print(self.reversing)
            # print(robot.speed)
            robot.speed = -(robot.maxspeed)

        if self.turning and robot.is_finished_turning():
            print("Finished turning.")
            self.turning = False
            robot.speed = robot.maxspeed


        if self.reversing > 0:
            self.reversing = self.reversing + robot.speed
            if self.reversing <= 0:
                print('stopped reversing')
                self.reversing = 0
                robot.speed = 0
                robot.turn(random.randint(90, 270))
                self.turning = True

class Wall_follow(Algoritm):

    def __init__(self):
        self.name = 'Wall Follow'
        self.reversing = 0
        self.timetoreverse = 5
        self.turning = False
        self.count = 0

    def setup(self, robot):
        robot.speed = robot.maxspeed
        robot.angle_speed = 1
        # robot.reset()

    def apply(self, robot):

        if (robot.is_colliding):
            self.reversing = self.timetoreverse
            robot.speed *= -1
            self.count += 1
            # print(self.count)

        if self.turning and robot.is_finished_turning():
            print("Finished turning.")
            self.turning = False
            robot.speed = robot.maxspeed
            robot.angle_change = 1800


        if self.reversing > 0:
            self.reversing = self.reversing + robot.speed
            if self.reversing <= 0:
                print('stopped reversing')
                self.reversing = 0
                robot.speed = 0
                robot.turn(180)
                self.turning = True

class allWithTimer(Algoritm):
    def __init__(self):
        self.name = "allWithTimer"
        self.timebetweenalgorihms = 5
        self.algorithms = [Boustrophedon, Random_walk, Spiral_and_Wfoll]
        self.algorithm_index = 0
        self.currentalgorithm = self.algorithms[self.algorithm_index]()
        self.nextchange = time.time() + self.timebetweenalgorihms

    def setup(self, robot):
        self.currentalgorithm.setup(robot)

    def changealgorithm(self, robot):
        self.algorithm_index = (self.algorithm_index + 1) % len(self.algorithms)
        self.currentalgorithm = self.algorithms[self.algorithm_index]()
        print("Switching to " + str(self.currentalgorithm.name))
        robot.reset()
        self.currentalgorithm.setup(robot)
        self.nextchange = time.time() + self.timebetweenalgorihms

    def apply(self, robot):
        if time.time() > self.nextchange:
            self.changealgorithm(robot)
        elif type(self.currentalgorithm) == Spiral and robot.is_colliding:
            self.changealgorithm(robot)
        self.currentalgorithm.apply(robot)



class Simulator():

    def __init__(self, algorithm, pos):
        self.robot = Robot(pos)
        self.robotsprite = pg.sprite.RenderPlain((self.robot))

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((255, 255, 255))
        pg.display.set_caption('Simulation?')
        self.walls = pg.PixelArray


        self.nextupdate = 0
        self.result = 0
        self.area = 0
        self.name = 'No algorithm chosen'
        self.start = True
        self.algorithm = algorithm
        self.timecount = 0
        self.graph = ''

    def update(self):
        pg.display.flip()

        # self.wall((0,20),(700,20), 10, 'up')
        # self.wall((690,0),(690,500), 10, 'right')
        # self.wall((0,490),(700,490), 10, 'down')
        # self.wall((10,0),(10,500), 10, 'left')

        pg.draw.rect(self.screen, GRAY, (0,0,700,17))
        if (self.start == True):
            self.screen.blit(room, (0,10))
            self.area = (self.calculate_area())
            self.start = False
        pg.draw.circle(self.screen, RED, (int(self.robot.oldposition[0]), int(self.robot.oldposition[1])), 30, 0)
        self.robotsprite.draw(self.screen)
        self.robotsprite.update()
        self.robot.is_colliding = False
        myangle = math.atan2(self.robot.direction[1], self.robot.direction[0])
        myanglerange = 100 * math.pi/180
        numtestpoints = 64
        for i in range(numtestpoints):
            x = self.robot.position[0] + (self.robot.radius + 6) * math.cos(myangle + ((i / (numtestpoints - 1)) -0.5) * myanglerange)
            y = self.robot.position[1] + (self.robot.radius + 6) * math.sin(myangle + ((i / (numtestpoints - 1)) -0.5) * myanglerange)
            x2 = self.robot.position[0] + (self.robot.radius ) * math.cos(myangle + ((i / (numtestpoints - 1)) -0.5) * myanglerange)
            y2 = self.robot.position[1] + (self.robot.radius ) * math.sin(myangle + ((i / (numtestpoints - 1)) -0.5) * myanglerange)
            # print ('x ' + str(x) + ' y ' + str(y))

            if (self.screen.get_at((int(x), int(y))) == (0,0,0,255)):
                self.robot.is_colliding = True
                break

            # self.screen.set_at((int(x2), int(y2)), (0,0,255,255))
            pg.draw.circle(self.screen, BLUE, (int(x2), int(y2)), 2, 0)

        self.textonscreen()






    def textonscreen(self):

        font = pg.font.SysFont('Calibri', 12, True, False)
        text = font.render("coverage:", True, BLACK)
        text2 = font.render(str(int(self.result)) + "%", True, BLACK)
        text3 = font.render(self.name, True, BLACK)
        self.screen.blit(text, [600, 7])
        self.screen.blit(text2, [650, 7])
        self.screen.blit(text3, [50, 7])

    def run_algorithm(self, algo):
        algo.setup(self.robot)
        self.name = algo.name

        run = True
        while(run):
            self.update()
            algo.apply(self.robot)
            # print(self.robot.angle_speed)
            if (pg.time.get_ticks() > self.nextupdate):
                self.nextupdate += 1000
                if (self.count_pixels() >= 99 or self.timecount == 100):
                    run = False
                    self.robot.speed = 0
                    self.name = 'finished in ' + (str(pg.time.get_ticks()/1000) + ' seconds')
                    break

    def count_pixels(self):

        counted = 0

        ar = pg.PixelArray (self.screen)
        for x in range (SCREEN_WIDTH):
            for y in range (SCREEN_HEIGHT):
                if (ar[x,y] == 16711680):
                    counted += 1
        colored = counted
        self.result = (colored/(self.area)*100)
        del ar
        file = open(self.name + '.txt','w')
        self.graph += (str(self.result) + '\n')
        file.write(self.graph)
        file.close()
        self.timecount += 1
        return self.result

    def calculate_area(self):

        counted = 0

        ar = pg.PixelArray (self.screen)
        for x in range (SCREEN_WIDTH):
            for y in range (SCREEN_HEIGHT):
                if (ar[x,y] == 16777215):
                    counted += 1
                # else:
                #     self.walls[x,y] = ar[x,y]
        del ar
        return counted

def main():
    pg.init()
    mysim = Simulator(Boustrophedon(), START)
    clock = pg.time.Clock()
    done = False
    while not done:
        mysim.update()
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    mysim.robot.speed += 1
                elif event.key == pg.K_DOWN:
                    mysim.robot.speed -= 1
                elif event.key == pg.K_LEFT:
                    mysim.robot.angle_speed = -4
                elif event.key == pg.K_RIGHT:
                    mysim.robot.angle_speed = 4
            elif event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    mysim.robot.angle_speed = 0
                elif event.key == pg.K_RIGHT:
                    mysim.robot.angle_speed = 0
                elif event.key == K_1:
                    mysim.run_algorithm(Spiral())
                elif event.key == K_2:
                    mysim.run_algorithm(Random_walk())
                elif event.key == K_3:
                    mysim.run_algorithm(Boustrophedon())
                elif event.key == K_4:
                    mysim.run_algorithm(Wall_follow())
                elif event.key == K_5:
                    mysim.run_algorithm(Spiral_and_Wfoll())
                elif event.key == K_6:
                    mysim.run_algorithm(allWithTimer())


if __name__ == '__main__':
    main()
    pg.quit()
