import pygame, random, time
from pygame.locals import *

height = 650
width = 450
points = 0
path = "C:\\Users\\Dell\\Desktop\\Agnieszka\\python\\Flappy bird\\img\\"

class Bird:
    def __init__(self, screen) -> None:

        self.images =  [pygame.image.load(f'{path}bluebird-upflap.png').convert_alpha(),
                        pygame.image.load(f'{path}bluebird-midflap.png').convert_alpha(),
                        pygame.image.load(f'{path}bluebird-downflap.png').convert_alpha()]
        
        self.x = width / 2
        self.y = height / 2
        self.screen = screen
        self.i = 0

    def push_button(self):
        self.y -= 10

    def fall(self):
        self.y += 10

    def display(self):
        self.screen.blit(self.images[self.i%3], (self.x, self.y))
        self.i += 1


def check_position(y):
    return y >= height -70 or y <= 0

def check_pipe_pos(p, bird_y):
    bird_x = width // 2
    bird_height = 24
    pipe_width = p.i_down.get_width()
    pipe_gap = 320                

    if bird_x + bird_height > p.x and bird_x < p.x + pipe_width:
        if bird_y < p.y_u + pipe_gap or bird_y + bird_height > p.y_d:
            return True
    return False

def count_points(bird, pipes):
    global points
    for pipe in pipes:
        if not pipe.passed and pipe.x + pipe.i_down.get_width() < bird.x:
            pipe.passed = True
            points += 1

class Pipe:
    def __init__(self, screen) -> None:
        self.i_down = pygame.image.load(f'{path}pipe-green.png').convert_alpha()
        self.i_up = pygame.transform.rotate(self.i_down, 180)
        self.rand_height = random.randint(280, height - random.randint(150, 200))
        self.x = width
        self.y_d = self.rand_height
        self.y_u = self.rand_height - height + 200
        self.screen = screen
        self.passed = False
     
    def display(self):
        self.screen.blit(self.i_down, (self.x, self.y_d))
        self.screen.blit(self.i_up, (self.x, self.y_u))
        self.x -= 8

def create_new_pipe(screen):
    return Pipe(screen)

def disp_ponits(points, screen):
    myFont = pygame.font.SysFont("Times New Roman", 18)
    pts = myFont.render("Your score : {}".format(points), 1, (255,255,255))
    screen.blit(pts, (20, 20))

def game_over(points, screen):
    myFont = pygame.font.SysFont("Times New Roman", 30)
    pts = myFont.render("Game over! Your score: {}".format(points), 1, (255,255,255), (49,163,41))
    screen.blit(pts, (100, width//2))
    pygame.display.flip() 
    time.sleep(3)

class Ground:
    def __init__(self, screen) -> None:
        self.imp = pygame.image.load(f'{path}ground.png').convert_alpha()
        self.screen = screen
        self.x = 0
        self.y = height - 40
    
    def display(self):
        self.screen.blit(self.imp, (self.x, self.y))
        self.x -= 8
        if self.x <= -width:
            self.x = 0    
        

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True

    ground = Ground(screen)
    bird = Bird(screen)
    pipes = [create_new_pipe(screen)]
    pipe_add_interval = 2000  # Time in milliseconds between pipe generation
    last_pipe_add_time = pygame.time.get_ticks()

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.push_button()
        else:
            bird.fall()

        if check_position(bird.y) or any(check_pipe_pos(pipe, bird.y) for pipe in pipes):
            game_over(points, screen)
            running = False
            continue            

        if current_time - last_pipe_add_time > pipe_add_interval:
            pipes.append(create_new_pipe(screen))
            last_pipe_add_time = current_time

        pipes = [pipe for pipe in pipes if pipe.x > -pipe.i_down.get_width()]

        count_points(bird, pipes)

        screen.fill((0, 0, 0))

        for pipe in pipes:
            pipe.display()

        bird.display()
        ground.display()

        disp_ponits(points, screen)

        pygame.display.flip()
        clock.tick(30)


    pygame.quit()
    print(f"Your score: {points}") 
