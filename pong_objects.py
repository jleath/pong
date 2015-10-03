import pygame
import random

random.seed(None)

class Paddle():
    def __init__(self, pad_width, pad_height, x, y, move_speed,
            obj_color=(255, 255, 255)):
        self.width = pad_width
        self.height = pad_height
        self.x_pos = x
        self.y_pos = y
        self.color = obj_color
        self.speed = move_speed
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.up = False
        self.down = False

    def get_size(self):
        return (self.width, self.height)

    def get_position(self, scr_width, scr_height):
        self.update_position(scr_width, scr_height)
        return (self.x_pos, self.y_pos)

    def update_position(self, scr_width, scr_height):
        new_x = self.x_pos + self.x_vel * self.speed
        new_y = self.y_pos + self.y_vel * self.speed
        if new_x < 0:
            self.x_pos = 0
        elif new_x > scr_width - self.width:
            self.x_pos = scr_width - self.width
        else:
            self.x_pos = new_x
        if new_y < 0:
            self.y_pos = 0
        elif new_y > scr_height - self.height:
            self.y_pos = scr_height - self.height
        else:
            self.y_pos = new_y

    def get_surface(self):
        surf = pygame.Surface(self.get_size())
        surf.fill(self.color)
        surf.convert_alpha()
        return surf

class Ball():
    def __init__(self, ball_diameter, x, y, move_speed, alpha_color=(0, 0, 0),
            obj_color=(255, 255, 255)):
        self.width = ball_diameter
        self.height = ball_diameter
        self.x_pos = x
        self.y_pos = y
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.speed = move_speed
        self.color = obj_color
        self.radius = self.width / 2
        self.alpha = alpha_color

    def get_size(self):
        return (self.width, self.height)

    def get_position(self, scr_width, scr_height):
        self.update_position(scr_width, scr_height)
        return (self.x_pos, self.y_pos)

    def update_position(self, scr_width, scr_height):
        new_x = self.x_pos + self.x_vel * self.speed
        new_y = self.y_pos + self.y_vel * self.speed
        if new_x > scr_width - self.width:
            self.x_vel = -1 * (abs(random.random() - .5))
        elif new_x < 0:
            self.x_vel = 1 * (abs(random.random() - .5))
        if new_y > scr_height - self.height:
            self.y_vel =  -1 * (abs(random.random() - .5))
        elif new_y < 0:
            self.y_vel = 1 * (abs(random.random() - .5))
        self.x_pos += self.x_vel * self.speed
        self.y_pos += self.y_vel * self.speed

    def get_surface(self):
        surf = pygame.Surface(self.get_size())
        pygame.draw.circle(surf, self.color, (self.width // 2, self.height // 2),
                int(self.radius))
        surf.set_colorkey(self.alpha)
        surf.convert_alpha()
        return surf
