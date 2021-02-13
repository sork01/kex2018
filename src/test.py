import pygame

RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

SCREEN_SIZE = (800, 600)
FPS = 60
BG_COLOR = BLUE

class Ball(pygame.sprite.Sprite):
    def __init__(self, color=WHITE, radius=10, position=[], velocity=[]):
        super(Ball, self).__init__()

        self.color = color
        self.radius = radius
        self.position = list(position) or [0, 0]
        self.velocity = list(velocity) or [0, 0]
        self.bounds = (screen.get_size()[0] - self.radius,
                       screen.get_size()[1] - self.radius)

        self.image = pygame.Surface(2*[self.radius*2])
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, self.color, 2*(self.radius,), self.radius)

    def update(self, dt=1./FPS):
        super(Ball, self).update()

        for i in [0, 1]:
            self.position[i] += self.velocity[i] * dt

            if self.position[i] < self.radius:
                self.position[i] = self.radius
                self.velocity[i] *= -1

            elif self.position[i] > self.bounds[i]:
                self.position[i] = self.bounds[i]
                self.velocity[i] *= -1

        self.rect.center = self.position


pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

background = pygame.Surface(screen.get_size())
background.fill(BG_COLOR)
screen.blit(background, (0,0))

balls = pygame.sprite.Group()
balls.add(Ball(color=RED,   radius=100, position=[  0, 300], velocity=[ 100, 0]))
balls.add(Ball(color=GREEN, radius=100, position=[700, 300], velocity=[-100, 0]))

done = False
while not done:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True

    balls.update()
    if pygame.sprite.collide_rect(*balls):
        collision = pygame.sprite.collide_circle(*balls)
        print (collision)
        if collision:
            for ball in balls:
                ball.velocity[0] *= -1

    balls.clear(screen, background)
    balls.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
