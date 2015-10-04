import pygame, sys
from pygame.locals import *
from pong_objects import *
import random

random.seed(None)
pygame.init()

font = pygame.font.Font(pygame.font.get_default_font(), 16)

AI_MAX_INTEL = 10
AI_MIN_INTEL = 20
enemy_ai = Choppy_AI(AI_MIN_INTEL, AI_MAX_INTEL)

# constants

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 40
PADDLE_SPEED = 8

BALL_WIDTH = 10
BALL_HEIGHT = 10
BALL_SPEED = 6

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

PADDLE_GAP = 10

# Game objects
screen_info = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
paddle1 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, SCREEN_WIDTH-PADDLE_WIDTH-PADDLE_GAP, 
                 SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_SPEED, screen_info,
                 obj_color=GREEN)
paddle2 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, 0 + PADDLE_GAP, 
        SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_SPEED, screen_info, obj_color=GREEN)
ball = Ball(BALL_WIDTH, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_SPEED, screen_info,
        obj_color=GREEN)

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
done = False
in_play = False

# Main game loop
while not done:
    caption = 'This AI is ' + str(enemy_ai.reaction_time) + '% dumb!'
    text = font.render(caption, 0, WHITE)
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
            if event.key == pygame.K_SPACE and not in_play:
                ball.x_vel = random.choice([1, -1])
                ball.y_vel = random.choice([1, -1])
                enemy_ai.set_intelligence()
                in_play = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle1.y_vel = 0
    paddle2.y_vel = enemy_ai.update(paddle2, ball)

    if ball.is_dead_ball():
        ball = Ball(BALL_WIDTH, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, BALL_SPEED,
                screen_info)
        in_play = False

    # Draw to game
    SCREEN.fill(BLACK)
    SCREEN.blit(text, (0, 0))
    SCREEN.blit(paddle1_surface, paddle1.get_position())
    SCREEN.blit(paddle2_surface, paddle2.get_position())
    SCREEN.blit(ball_surface, ball.get_position(paddle1, paddle2))
    pygame.display.flip()

pygame.quit()
sys.exit()

