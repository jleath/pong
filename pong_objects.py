import pygame
import random

random.seed(None)

class Screen(object):
    def __init__(self, scr_width, scr_height):
        self.width = scr_width
        self.height = scr_width

class Pong_Object(object):
    def __init__(self, w, h, x, y, move_speed, scr, obj_color=(255, 255, 255),
            alpha_color=(0, 0, 0)):
        self.width = w
        self.height = h
        self.x_pos = x
        self.y_pos = y
        self.color = obj_color
        self.alpha = alpha_color
        self.speed = move_speed
        self.x_vel = 0.0
        self.y_vel = 0.0
        self._screen_info = scr

    def get_size(self):
        return (self.width, self.height)

    def get_position(self):
        self._update_position()
        return (self.x_pos, self.y_pos)

    def _update_position(self):
        new_x = self._next_x_position()
        new_y = self._next_y_position()
        if new_x < 0:
            self.x_pos = 0
        elif new_x > self._screen_info.width - self.width:
            self.x_pos = self._screen_info.width - self.width
        else:
            self.x_pos = new_x
        if new_y < 0:
            self.y_pos = 0
        elif new_y > self._screen_info.height - self.height:
            self.y_pos = self._screen_info.height - self.height
        else:
            self.y_pos = new_y

    def _next_x_position(self):
        return self.x_pos + self.x_vel * self.speed

    def _next_y_position(self):
        return self.y_pos + self.y_vel * self.speed

class Paddle(Pong_Object):
    def __init__(self, pad_width, pad_height, x, y, move_speed, screen):
        Pong_Object.__init__(self, pad_width, pad_height, x, y, move_speed, screen)

    def get_surface(self):
        surf = pygame.Surface(self.get_size())
        surf.fill(self.color)
        surf.convert_alpha()
        return surf

class Ball(Pong_Object):
    def __init__(self, ball_diameter, x, y, move_speed, screen):
        Pong_Object.__init__(self, ball_diameter, ball_diameter, x, y, move_speed, screen)

    def get_position(self, p1, p2):
        self.update_position(p1, p2)
        return (self.x_pos, self.y_pos)

    def _check_for_paddle_collision(self, paddle1, paddle2):
        new_x = self._next_x_position()
        new_y = self._next_y_position()
        if new_x > paddle1.x_pos-self.width and new_x < paddle1.x_pos + paddle1.width \
                and new_y > paddle1.y_pos and new_y < paddle1.y_pos + paddle1.height:
            self.x_vel = -1
        elif new_x < paddle2.x_pos + paddle2.width and new_x > paddle2.x_pos \
                and new_y > paddle2.y_pos and new_y < paddle2.y_pos + paddle2.height:
            self.x_vel = 1

    def _check_for_wall_collision(self):
        new_y = self._next_y_position()
        if new_y > self._screen_info.height - self.height:
            self.y_vel =  -1
        elif new_y < 0:
            self.y_vel = 1

    def update_position(self, p1, p2):
        self._check_for_paddle_collision(p1, p2)
        self._check_for_wall_collision()
        self.x_pos = self._next_x_position()
        self.y_pos  = self._next_y_position()

    def get_surface(self):
        surf = pygame.Surface(self.get_size())
        pygame.draw.circle(surf, self.color, (self.width // 2, self.height // 2),
                self.width // 2)
        surf.set_colorkey(self.alpha)
        surf.convert_alpha()
        return surf

    def is_dead_ball(self):
        return self.x_pos > self._screen_info.width or self.x_pos < 0
