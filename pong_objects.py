""" A library of objects for the game Pong. """

import pygame
import random

random.seed(None)

class Choppy_AI(object):
    def __init__(self, min_intel, max_intel):
        self.frames_since_last_move = 0
        self.ai_min_intel = min_intel
        self.ai_max_intel = max_intel
        self.reaction_time = 0

    def set_intelligence(self):
        self.reaction_time = random.randint(self.ai_max_intel, self.ai_min_intel) 
        self.frames_since_last_move = 0

    def update(self, paddle, ball):
        if self.frames_since_last_move == self.reaction_time:
            paddle_mid = paddle.y_pos + (paddle.height / 2)
            ball_mid = ball.y_pos + (ball.height / 2)
            if ball.y_vel > 0 and paddle_mid < ball_mid:
                return 1
            elif ball.y_vel < 0 and paddle_mid > ball_mid:
                return -1
            else:
                return 0
            self.frames_since_last_move = 0
        else:
            self.frames_since_last_move += 1
            return 0

class Screen(object):
    """ A datatype for representing a display screen's width and height. """
    def __init__(self, scr_width, scr_height):
        self.width = scr_width
        self.height = scr_width

class Pong_Object(object):
    """ A base class for representing an object in a game of pong. """
    def __init__(self, w, h, x, y, move_speed, scr, obj_color=(255, 255, 255),
            alpha_color=(0, 0, 0)):
        """ 
            Pong_Object constructor:
                w - width of the object.
                h - height of the object.
                x - the x position of the object.
                y - the y position of the object.
                move_speed - the speed at which the object moves.
                scr - the screen the object will be drawn on.
                obj_color - the color of the object
                alpha_color - the color that will be transparent.
        """
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
        """ Returns a tuple containing the width and height of the object. """
        return (self.width, self.height)

    def get_position(self):
        """ Returns a tuple containing the position of the object.
        Will update the position of the object based on game state.
        """
        self._update_position()
        return (self.x_pos, self.y_pos)

    def _update_position(self):
        """ Updates the position of the object, based on its current velocity
        and position.  this is where collision handling will occur.
        """
        new_x = self._next_x_position()
        new_y = self._next_y_position()
        # Check if object is off the left of the screen
        if new_x < 0:
            self.x_pos = 0
        # Check if object is off the right of the screen
        elif new_x > self._screen_info.width - self.width:
            self.x_pos = self._screen_info.width - self.width
        else:
            self.x_pos = new_x
        # Check if object is off the top of the screen
        if new_y < 0:
            self.y_pos = 0
        # Check if object is off the bottom of the screen
        elif new_y > self._screen_info.height - self.height:
            self.y_pos = self._screen_info.height - self.height
        else:
            self.y_pos = new_y

    def _next_x_position(self):
        """ Returns the x position of the object after its next update.
        Does not actually modify the object's position.
        """
        return self.x_pos + self.x_vel * self.speed

    def _next_y_position(self):
        """ Returns the y position of the object after its next update.
        Does not actually modify the object's position.
        """
        return self.y_pos + self.y_vel * self.speed

class Paddle(Pong_Object):
    """ A class for representing a paddle in pong.  Inherits from Pong_Object. """
    def __init__(self, pad_width, pad_height, x, y, move_speed, screen):
        Pong_Object.__init__(self, pad_width, pad_height, x, y, move_speed, screen)

    def get_surface(self):
        """ Returns a surface for a paddle.  The surface will have the width
        and height of the paddle object and will be colored white.
        """
        surf = pygame.Surface(self.get_size())
        surf.fill(self.color)
        surf.convert_alpha()
        return surf

class Ball(Pong_Object):
    """ A class for representing a ball in pong.  Inherits from Pong_Object. """
    def __init__(self, ball_diameter, x, y, move_speed, screen):
        Pong_Object.__init__(self, ball_diameter, ball_diameter, x, y, move_speed, screen)

    def get_position(self, p1, p2):
        """ 
        Override the base class's get_position method so that we can pass in the
        paddles.  This is necessary to handle collision with paddles.
        """
        self.update_position(p1, p2)
        return (self.x_pos, self.y_pos)

    def _check_for_paddle_collision(self, paddle1, paddle2):
        """ A private method for handling paddle collision. If the ball makes
        contact with a paddle, its direction on the x axis will be reversed.
        """
        new_x = self._next_x_position()
        new_y = self._next_y_position()
        # check if the ball will collide with the right paddle (player 1)
        if new_x > paddle1.x_pos-self.width and new_x < paddle1.x_pos + paddle1.width \
                and new_y > paddle1.y_pos and new_y < paddle1.y_pos + paddle1.height:
            self.x_vel = -1
        # check if the ball will collide with the left paddle (player 2)
        elif new_x < paddle2.x_pos + paddle2.width and new_x > paddle2.x_pos \
                and new_y > paddle2.y_pos and new_y < paddle2.y_pos + paddle2.height:
            self.x_vel = 1

    def _check_for_wall_collision(self ):
        """ A private method for handling wall collision. We only need to bounce off
        the top and bottom of the screen.
        """
        new_y = self._next_y_position()
        # check for collision with the bottom of the screen
        if new_y > self._screen_info.height - self.height:
            self.y_vel =  -1
        # check for collision with the top of the screen
        elif new_y < 0:
            self.y_vel = 1

    def update_position(self, p1, p2):
        """
        Override the base class's update_position method so we can handle
        ball/paddle collision.
        """
        self._check_for_paddle_collision(p1, p2)
        self._check_for_wall_collision()
        self.x_pos = self._next_x_position()
        self.y_pos  = self._next_y_position()

    def get_surface(self):
        """ Return a surface for the ball.  The surface will have the width and height
        of the ball, will have a circle in the middle, and black will be set as the alpha
        colorkey for transparency.
        """
        surf = pygame.Surface(self.get_size())
        pygame.draw.circle(surf, self.color, (self.width // 2, self.height // 2),
                self.width // 2)
        surf.set_colorkey(self.alpha)
        surf.convert_alpha()
        return surf

    def is_dead_ball(self):
        """ Returns True if the ball has gone outside the bounds of the screen. """
        return self.x_pos > self._screen_info.width or self.x_pos < 0
