import pygame, sys
from pygame.locals import *
from pong_objects import *
import random

random.seed(None)
pygame.init()

# constants

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 40
PADDLE_SPEED = 10

BALL_WIDTH = 10
BALL_HEIGHT = 10
BALL_SPEED = 3

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_GAP = 0

# Game objects
paddle1 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, SCREEN_WIDTH-PADDLE_WIDTH-PADDLE_GAP, 
                 SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_SPEED)
paddle2 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, 0 + PADDLE_GAP, 
        SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_SPEED)
ball = Ball(BALL_WIDTH, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_SPEED)

clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode(SCREEN_SIZE)

# prepare display surface 
pygame.display.set_caption('PONG')
SCREEN.fill(BLACK)
SCREEN.convert_alpha()

# get surfaces for paddles and ball
paddle1_surface = paddle1.get_surface()
paddle2_surface = paddle2.get_surface()
ball_surface = ball.get_surface()

# game state variables
paused = False
done = False
in_play = False

# Main game loop
while not done:
    if paused:
        #pygame.display.set_caption('PONG - Paused')
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_q:
                    done = True
            elif event.type == QUIT:
                done = True
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True
                if event.key == pygame.K_UP:
                    paddle1.y_vel = -1
                if event.key == pygame.K_DOWN:
                    paddle1.y_vel = 1
                if event.key == pygame.K_w:
                    paddle2.y_vel = -1
                if event.key == pygame.K_s:
                    paddle2.y_vel = 1
                if event.key == pygame.K_SPACE and not in_play:
                    ball.x_vel = random.choice([1, -1])
                    ball.y_vel = random.choice([1, -1])
                if event.key == pygame.K_p:
                    paused = not paused
                    paddle1.y_vel = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle1.y_vel = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle2.y_vel = 0

        # Draw to game
        SCREEN.fill(BLACK)
        SCREEN.blit(paddle1_surface, paddle1.get_position(SCREEN_WIDTH, 
            SCREEN_HEIGHT))
        SCREEN.blit(paddle2_surface, paddle2.get_position(SCREEN_WIDTH,
            SCREEN_HEIGHT))
        SCREEN.blit(ball_surface, ball.get_position(SCREEN_WIDTH, SCREEN_HEIGHT,
                paddle1, paddle2))
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
sys.exit()

