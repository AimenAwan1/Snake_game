import pygame
from pygame.locals import *
import time
import random

SIZE = 20
BACKGROUND_COLOUR = (240, 125, 201)

class Button:
    def __init__(self,name, x ,y):
        self.surface = pygame.display.set_mode((1000, 800))
        self.surface.fill('pink')

        font = pygame.font.SysFont('arial',40, bold = True)
        self.surf = font.render(name, True, 'white')
        self.button = pygame.Rect(x,y, 110, 60)
        self.clicked = False

    def draw_button(self):
        action = False
        pos = pygame.mouse.get_pos()

        #if self.button.x <= a <= self.button.x + 110 and self.button.y <= b <= self.button.y + 60:
        if self.button.collidepoint(pos):
            pygame.draw.rect(self.surface, (180,180,180), self.button)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        else:
            pygame.draw.rect(self.surface, (110, 110, 110), self.button)
        self.surface.blit(self.surf, (self.button.x +5, self.button.y+5))

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.display.flip()
        return action

class Test:
    def __init__(self):
        pygame.init()

    def run(self):
        running = True

        start_button = Button("Start", 200, 200)
        quit_button = Button("Quit", 400, 200)
        #self.surface = pygame.display.set_mode((1000, 800))

        while running:

            #self.surface.fill('pink')
            if start_button.draw_button():
                print('Start')
            if quit_button.draw_button():
                running = False


            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    pygame.quit()

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("apple.png").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x= random.randint(0,24)*SIZE
        self.y= random.randint(0,19)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("block1.png").convert()

        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'

    def draw(self):
        #self.parent_screen.fill((BACKGROUND_COLOUR))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE

        self.draw()
class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2  and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def play_background_music(self):
        pygame.mixer.music.load("bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound_name):
        if sound_name == "ding":
            sound = pygame.mixer.Sound("ding.mp3")
        elif sound_name == ("crash"):
            sound = pygame.mixer.Sound("crash.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("background.jpg")
        self.surface.blit(bg, (0,0))
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        for i in range(1,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision Occured"

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True, (200,200,200))
        self.surface.blit(score, (800,10))

    def show_game_over(self):
        time.sleep(1)
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f" GAME OVER Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255,255,255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)

if __name__ == "__main__":
    game = Game()
    game.run()

    #game = Test()
    #game.run()