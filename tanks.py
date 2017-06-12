import pygame
import inspect, os, sys
import random 


pygame.init()

if getattr(sys, "frozen", False):
    # frozen
    DIRECTORY = os.path.dirname(sys.executable)
    IMAGES = DIRECTORY 
else:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    IMAGES = os.path.join(DIRECTORY, "images") 

print("\n\n" + IMAGES+ "\n\n")
SMALL_FONT = pygame.font.SysFont("comicsansms", 25)
MEDIUM_FONT = pygame.font.SysFont("comicsansms", 50)
LARGE_FONT = pygame.font.SysFont("comicsansms", 80)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (200, 0, 0)
LIGHT_RED = (255, 0, 0)

YELLOW = (200, 200, 0)
LIGHT_YELLOW = (255, 255, 0)

GREEN = (34, 177, 76)
LIGHT_GREEN = (0, 255, 0)

BLUE = (0, 0, 255)

DISPLAY_X = 800
DISPLAY_Y = 600

gameDisplay = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
pygame.display.set_caption("Tanks")

#snake_img = pygame.image.load(os.path.join(IMAGES, "snake.png"))
#apple_img = pygame.image.load(os.path.join(IMAGES, "apple.png"))
direction = "right"
    
clock = pygame.time.Clock()


tankWidth = 40
tankHeight = 20
turretWidth = 5
wheelWidth = 5

FPS = 30
BLOCK_SIZE = 20
APPLE_SIZE = 30
SNAKE_SPEED = BLOCK_SIZE
START_LENGTH = 10
GROWTH_RATE = 5

def text_objects(text, color, font):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, font, y_displace=0):
    textSurface, textRect = text_objects(msg, color, font)
    textRect.center = (DISPLAY_X/2, DISPLAY_Y/2+y_displace)
    gameDisplay.blit(textSurface, textRect)

def text_to_button(msg, color, button, size):
    textSurface, textRect = text_objects(msg, color, size)
    textRect.center = ((button[0]+button[2]/2, button[1]+button[3]/2))
    gameDisplay.blit(textSurface, textRect)

def button(text, x, y, width, height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y+height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1:
            if action == "quit":
                pygame.quit()
                quit()

            if action == "menu":
                game_intro()

            if action == "controls":
                game_controls()

            if action == "play":
                gameLoop()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))
    text_to_button(text, BLACK, (x, y, width, height), SMALL_FONT)

def tank(x,y, turretPosition):
    x = int(x)
    y = int(y)
    
    possibleTurrets = [(x-27, y-2), 
                       (x-26, y-5),
                       (x-25, y-8),
                       (x-23, y-12),
                       (x-20, y-14),
                       (x-18, y-15),
                       (x-15, y-17),
                       (x-11, y-21),
                       ]

    pygame.draw.circle(gameDisplay, WHITE, (x, y), tankHeight//2)
    pygame.draw.rect(gameDisplay, WHITE, (x-tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, WHITE, (x,y), possibleTurrets[turretPosition], turretWidth)

    for dx in range(1, tankWidth, tankWidth//8+2):
        pygame.draw.circle(gameDisplay, WHITE, (x-tankHeight+dx, y+22), wheelWidth)

def score(score):
    text = SMALL_FONT.render("Score: " + str(score), True, YELLOW)
    gameDisplay.blit(text, [0,0])
    
def game_controls():
    controls = True

    while controls:
        gameDisplay.fill(BLACK)
        message_to_screen("Controls", LIGHT_GREEN, LARGE_FONT, -100)
        message_to_screen("Fire: Spacebar", YELLOW, SMALL_FONT, -20)
        message_to_screen("Move turret: Up and Down arrows", YELLOW, SMALL_FONT, 10)
        message_to_screen("Move tank: Left and Right arrows", YELLOW, SMALL_FONT, 40)
        message_to_screen("Pause: P", YELLOW, SMALL_FONT, 70)

        button("play", 150, 500, 100, 50, GREEN, LIGHT_GREEN, action="play") 
        #button("main menu", 350, 500, 100, 50, YELLOW, LIGHT_YELLOW, action="menu") 
        button("quit", 550, 500, 100, 50, RED, LIGHT_RED, action="quit") 



        pygame.display.update()
        clock.tick(10) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False


def game_intro():
    intro = True

    while intro:
        gameDisplay.fill(BLACK)
        message_to_screen("Welcome to Tanks!", LIGHT_GREEN, LARGE_FONT, -100)
        message_to_screen("Control the snake with the arrow keys.", YELLOW, SMALL_FONT, -20)
        message_to_screen("The objective is to shoot and destroy", YELLOW, SMALL_FONT, 10)
        message_to_screen("the enemy tank before they destroy you.", YELLOW, SMALL_FONT, 40)
        message_to_screen("The more enemies you destroy, the harder they get.", YELLOW, SMALL_FONT, 70)
        message_to_screen("Press C to start, Q to quit and P to pause!", WHITE, SMALL_FONT, 180)

        button("play", 150, 500, 100, 50, GREEN, LIGHT_GREEN, action="play") 
        button("controls", 350, 500, 100, 50, YELLOW, LIGHT_YELLOW, action="controls") 
        button("quit", 550, 500, 100, 50, RED, LIGHT_RED, action="quit") 

        pygame.display.update()
        clock.tick(15) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False

def pause():
    paused = True
    message_to_screen("PAUSED", YELLOW, LARGE_FONT, -100)
    message_to_screen("Press C to continue, or Q to quit.", WHITE, SMALL_FONT, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        #gameDisplay.fill(BLACK)
        clock.tick(5)


def gameLoop():

    mainTankX = DISPLAY_X * 0.9
    mainTankY = DISPLAY_Y * 0.7
    tankMove = 0
    turretMove = 0
    turretPosition = 4
    
    gameExit = False
    gameOver = False

    while not gameExit:
        clock.tick(FPS)
        if gameOver == True:
            message_to_screen("GAME OVER!", RED, LARGE_FONT, y_displace=-50)
            message_to_screen("Press C to play again or Q to quit.", WHITE, SMALL_FONT, y_displace=50)
            pygame.display.update()
        
        while gameOver == True:
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == pygame.K_c:
                        gameLoop()
    
        # EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tankMove += -5
                elif event.key == pygame.K_RIGHT:
                    tankMove += 5
                elif event.key == pygame.K_UP:
                    turretMove += 1
                elif event.key == pygame.K_DOWN:
                    turretMove += -1
                elif event.key == pygame.K_p:
                    pause()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    tankMove += 5
                elif event.key == pygame.K_RIGHT:
                    tankMove += -5
                elif event.key == pygame.K_UP:
                    turretMove += -1
                elif event.key == pygame.K_DOWN:
                    turretMove += 1
    
        # GRAPHICS
        gameDisplay.fill(BLACK)
        mainTankX += tankMove
        if 0 <= turretPosition + turretMove < 8:
            turretPosition += turretMove
        tank(mainTankX, mainTankY, turretPosition)

        pygame.display.update()

    # QUIT
    pygame.quit()
    quit()

game_intro()
