import pygame, sys
from pygame.locals import *
from pygame.math import Vector2
import random

class SNAKE:

    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.newBlock = False
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.head = self.head_right
        self.tail = self.tail_left

        self.fruit_sound = pygame.mixer.Sound('Sounds/crunch.wav')

    #Draw snake function
    def drawSnake(self):
        self.updateHeadGraphics()
        self.updateTailGraphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:   
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 \
                        or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    if previous_block.x == -1 and next_block.y == 1 \
                        or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    if previous_block.x == 1 and next_block.y == -1 \
                        or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    if previous_block.x == 1 and next_block.y == 1 \
                        or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    #Update Head Sprite
    def updateHeadGraphics(self):
        head_rel = self.body[1] - self.body[0]
        if head_rel == Vector2(1, 0): self.head = self.head_left
        elif head_rel == Vector2(-1, 0): self.head = self.head_right
        elif head_rel == Vector2(0, 1): self.head = self.head_up
        elif head_rel == Vector2(0, -1): self.head = self.head_down

    #Update Tail Sprite
    def updateTailGraphics(self):
        tail_rel = self.body[-2] - self.body[-1]
        if tail_rel == Vector2(1, 0): self.tail = self.tail_left
        elif tail_rel == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_rel == Vector2(0, 1): self.tail = self.tail_up
        elif tail_rel == Vector2(0, -1): self.tail = self.tail_down

    #Snake moves function
    def moveSnake(self):
        if self.newBlock == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.newBlock = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    #Adding block to the snake
    def addBlock(self):
        self.newBlock = True

    #Play the chrunch sound when eating fruit
    def playCrunchSound(self):
        self.fruit_sound.play()
        self.fruit_sound.set_volume(0.2)

class FRUIT:
    def __init__(self):
        self.randomize()

    #Draw fruit sprite
    def drawFruit(self):
        fruitRect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(peach, fruitRect)

    #Randomize position of the fruit
    def randomize(self):
        self.x = random.randint(0, num_cells-1)
        self.y = random.randint(0, num_cells-1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.gameOver = False

    #Reset Game
    def reset(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    #Update snake position, fruit collision and failure
    def update(self):
        self.snake.moveSnake()
        self.checkFruit()
        self.checkFailure()

    #Draw all the elements
    def drawElements(self):
        self.draw_grass()
        self.fruit.drawFruit()
        self.snake.drawSnake()
        self.drawScore()

    #Check if the snake eats the fruit
    def checkFruit(self):
        if self.fruit.pos == self.snake.body[0]:
            # reposition the fruit
            self.fruit.randomize()
            # add another block to the snake
            self.snake.addBlock()
            
            self.snake.playCrunchSound()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    #Check if the snake has a collision
    def checkFailure(self):
        #check if snake is outside of the screen
        if not 0 <= self.snake.body[0].x < num_cells or not 0 <= self.snake.body[0].y < num_cells:
            self.gameOver = True
        #check if the snake hits himself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver = True

    #adds grass color
    def draw_grass(self):
        grass_color = (50, 196, 59)
        for row in range(num_cells):
            if row % 2 == 0:
                for col in range(num_cells):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(num_cells):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
    
    #Render the score value and an image of the fruit
    def drawScore(self):
        score_text = str(self.getScore())
        score_surface = game_font.render(score_text, True, (56, 64, 12))
        score_x = int(cell_size * num_cells - 60)
        score_y = int(cell_size * num_cells - 40)
        score_rect = score_surface.get_rect(center = (score_x, score_y))
        peach_rect = peach.get_rect(midright= (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(peach_rect.left - 5, peach_rect.top - 5, peach_rect.width + score_rect.width + 10,peach_rect.height + 10)
        
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(peach, peach_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 2)

    def drawText(self, text, font, color, y):
        img = font.render(text, True, color)
        score_x = int((cell_size * num_cells) / 2)
        img_rect = img.get_rect(center = (score_x, y))
        screen.blit(img, img_rect)

    def getScore(self):
        return len(self.snake.body) - 3
pygame.init()

#Dimensions of the window
cell_size = 40
num_cells = 20
screen = pygame.display.set_mode((cell_size * num_cells, cell_size * num_cells))

#Set the title of the window
pygame.display.set_caption('Snake')

# # Create a clock object to control the frame rate
clock = pygame.time.Clock()

#main game
main = MAIN()
#Create an event
SCREEN_UPDATE = pygame.USEREVENT

#Set to trigger the event every 150ms
pygame.time.set_timer(SCREEN_UPDATE, 150)

#Load fruit
peach = pygame.image.load('Graphics/peach.png').convert_alpha()

#Game Font
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
game_font_big = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 35)
while True:
    
    #Event Loop
    for event in pygame.event.get():
        #If the window close button is clicked, quit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        #Playing Screen
        if main.gameOver == False:

            #Update every 150ms
            if event.type == SCREEN_UPDATE:
                main.update()

            #Update snake direction
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        if main.snake.direction.y != 1:
                            main.snake.direction = Vector2(0, -1)
                    case pygame.K_DOWN:
                        if main.snake.direction.y != -1:
                            main.snake.direction = Vector2(0, 1)
                    case pygame.K_LEFT:
                        if main.snake.direction.x != 1:
                            main.snake.direction = Vector2(-1, 0)
                    case pygame.K_RIGHT:
                        if main.snake.direction.x != -1:
                            main.snake.direction = Vector2(1, 0)

            #Fill screen with color
            screen.fill((175, 215, 70))

            #Draw all the elements on the screen
            main.drawElements()

        #Game Over Screen
        else: 
            #Draw the Game Over screen with the Score
            screen.fill((0, 0, 0))
            main.drawText('GAME OVER', game_font_big, (255, 255, 255), 320)
            main.drawText('SCORE: ' + str(main.getScore()), game_font_big, (255, 255, 255), 370)
            main.drawText('PRESS SPACE TO PLAY AGAIN', game_font_big, (255, 255, 255), 420)

            #If press the space the game is reset
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_SPACE]:
                main.reset()
                main.gameOver = False

    pygame.display.update()
    clock.tick(120)