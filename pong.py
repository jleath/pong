import pygame, sys
from pygame.locals import *
from pong_objects import *
from pong_locals import *
import random

random.seed(None)
pygame.init()

if not pygame.font.get_init():
    print('Pygame: Font module failed to load.')
if not pygame.mixer.get_init():
    print('Pygame: Mixer module failed to load.')
if not pygame.display.get_init():
    print('Pygame: Display module failed to load.')

font = pygame.font.Font(pygame.font.get_default_font(), 16)

enemy_ai = Enemy_AI(AI_MIN_REACT, AI_MAX_REACT, AI_HIT_ZONE_MIN, AI_HIT_ZONE_MAX)

# font surfaces
MUTING_INST = font.render(MUTE_INST_TEXT, 0, WHITE)
START_INST = font.render(START_INST_TEXT, 0, WHITE)
MOVEMENT_INST = font.render(MOVE_INST_TEXT, 0, WHITE)
QUIT_INST = font.render(QUIT_INST_TEXT, 0, WHITE)

# sound objects
bat_hit_snd = pygame.mixer.Sound(BAT_HIT_SND)
wall_hit_snd = pygame.mixer.Sound(WALL_HIT_SND)
score_snd = pygame.mixer.Sound(SCORE_SND)
point_lost_snd = pygame.mixer.Sound(POINT_LOST_SND)

# Game objects
screen_info = Screen(SCREEN_WIDTH, SCREEN_HEIGHT)
paddle1 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE1_START_X, PADDLE1_START_Y, 
        PADDLE_SPEED, screen_info, obj_color=GREEN)
paddle2 = Paddle(PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE2_START_X, PADDLE2_START_Y,
        PADDLE_SPEED, screen_info, obj_color=GREEN)
ball = Ball(BALL_WIDTH, BALL_START_X, BALL_START_Y, BALL_SPEED, screen_info,
       bat_hit_snd, wall_hit_snd, score_snd, point_lost_snd, obj_color=GREEN)

clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode(SCREEN_SIZE)

# prepare display surface 
pygame.display.set_caption(CAPTION_TEXT)
SCREEN.fill(BLACK)
SCREEN.convert_alpha()

# get surfaces for paddles and ball
paddle1_surface = paddle1.get_surface()
paddle2_surface = paddle2.get_surface()
ball_surface = ball.get_surface()

# game state variables
done = False
in_play = False
elapsed = 0.0
show_stats = False
decoy = None

# Main game loop
while not done:
    seconds = elapsed / 1000.0
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                show_stats = not show_stats
            if event.key == pygame.K_q:
                done = True
            if event.key == pygame.K_UP:
                paddle1.y_vel = -1
            if event.key == pygame.K_DOWN:
                paddle1.y_vel = 1
            if event.key == pygame.K_SPACE and not in_play:
                ball.x_vel = random.choice([1, -1])
                ball.y_vel = random.choice([1, -1])
                enemy_ai.set_reaction_time()
                in_play = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle1.y_vel = 0
    if enemy_ai.focused:
        if abs(paddle2.y_pos - ball.y_pos) < 50 and ball.x_pos < 100:
            paddle2.y_vel = enemy_ai.update(paddle2, ball)
        else:
            paddle2.y_vel = enemy_ai.update(paddle2, decoy)
        if ball.x_vel > 0:
            enemy_ai.focused = False
            decoy = None
    else:
         if ball.x_vel <= -1 and (ball.y_vel > 1 or ball.y_vel < -1):
            decoy = enemy_ai.focus(ball, paddle1, paddle2, seconds)
         paddle2.y_vel = enemy_ai.update(paddle2, ball)
    if ball.x_vel == 0 and ball.y_vel == 0:
        paddle2.y_vel = enemy_ai.update(paddle2, ball)


    if ball.is_dead_ball(paddle1, paddle2):
        enemy_ai.unfocus()
        decoy = None
        ball = Ball(BALL_WIDTH, BALL_START_X, BALL_START_Y, BALL_SPEED,
                screen_info, bat_hit_snd, wall_hit_snd, score_snd, point_lost_snd)
        in_play = False
        

    # Draw to game
    SCREEN.fill(BLACK)
    SCREEN.blit(paddle1_surface, paddle1.get_position(seconds))
    SCREEN.blit(paddle2_surface, paddle2.get_position(seconds))
    SCREEN.blit(ball_surface, ball.get_position(paddle1, paddle2, seconds))

    # draw text
    SCREEN.blit(font.render(str(paddle1.score), 0, WHITE),
            (SCREEN_WIDTH / 4, SCREEN_HEIGHT - 25))
    SCREEN.blit(font.render(str(paddle2.score), 0, WHITE), 
            (SCREEN_WIDTH - (SCREEN_WIDTH / 4), SCREEN_HEIGHT - 25))
    if show_stats:
        SCREEN.blit(font.render('HIT-ZONE: ' + str(enemy_ai.hit_zone) + ' REACT: ' + \
                str(enemy_ai.reaction_time), 0, WHITE), (50, 100))
        if enemy_ai.focused:
            SCREEN.blit(font.render('FOCUSED', 0, WHITE), (50, 50))
            SCREEN.blit(font.render('AI PADDLE: ' + str(int(paddle2.x_pos)) + ', ' + str(int(paddle2.y_pos)),
                0, WHITE), (50, 25))
        if decoy is not None:
            SCREEN.blit(font.render('Expected intercept: ' + str(int(decoy.x_pos)) + ', ' + str(int(decoy.y_pos)),
                0, WHITE), (300, 25))
    
    pygame.display.flip()
    elapsed = clock.tick(FPS)

pygame.quit()
sys.exit()

