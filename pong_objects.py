""" A library of objects for the game Pong. """

import pygame
import random
from pong_locals import *

random.seed(None)

class Choppy_AI(object):
    """ This is a preliminary version of the enemy AI.  I'm not entirely happy
    with it.  It works by randomly setting a reaction time which is
    just simply a number of frames that must be drawn before the ai can act.
    This reaction time is a random number between MIN_INTEL and MAX_INTEL.
    So if the reaction time is 15, the ai will update its paddle's position
    every 15 frames.
    The problem with this is that the movement of the AI's paddle is very choppy.
    I'm going to try to fix this in the methods for drawing the paddle rather than
    messing with the AI too much because I like this particular method.  It is
    simple and works pretty well.
    """
    def __init__(self, min_intel, max_intel, h_zone_min, h_zone_max):
        self.frames_since_last_move = 0
        self.ai_min_intel = min_intel
        self.ai_max_intel = max_intel
        self.reaction_time = self.set_intelligence()
        self.hit_zone_min = h_zone_min
        self.hit_zone_max = h_zone_max
        self.hit_zone = self.hit_zone_min
        self.focused = False

    def set_intelligence(self):
        """ Sets a reaction time between AI_MAX_INTEL and AN_MIN_INTEL and
        resets the frames counter.
        """
        self.reaction_time = random.randint(self.ai_max_intel, self.ai_min_intel) 
        self.frames_since_last_move = 0

    def _time_to_update_intelligence(self):
        """ We will update the AI's hit-zone randomly."""
        return random.randint(self.hit_zone_min, self.hit_zone_max) == self.hit_zone

    def _update_intelligence(self):
        """ Set a new random hit-zone area. """
        self.hit_zone = random.randint(self.hit_zone_min, self.hit_zone_max)

    def unfocus(self):
        self.set_intelligence()
        self.focused = False

    def focus(self, ball, paddle1, paddle2, elapsed):
        self.reaction_time *= 3
        self.focused = True
        ball_copy = ball.copy()
        screen_height = ball_copy._screen_info.height
        while (ball_copy.x_pos > PADDLE_GAP):
            while ball_copy.y_pos > 0 and ball_copy.y_pos < screen_height:
                ball_copy.x_pos += ball_copy.x_vel * (ball_copy.speed * elapsed)
                ball_copy.y_pos += ball_copy.y_vel * (ball_copy.speed * elapsed)
                if ball_copy.x_pos < 0:
                    break
            if ball_copy.y_pos <= 0 and ball_copy.x_pos > 0:
                ball_copy.y_pos = 1
            if ball_copy.y_pos >= screen_height and ball_copy.x_pos > 0:
                ball_copy.y_pos = screen_height - 1
            ball_copy.y_vel *= -1
        return ball_copy
        
        

    def update(self, paddle, ball):
        """ This is where the AI will act.  If enough time has passed for the
        AI to react, it will move its paddle's position to track the ball.
        Otherwise, it will just increment the frame counter and wait.
        The AI also has a 'hit-zone' which is the area of the paddle that
        it will try to hit the ball with. This will vary randomly throughout 
        the game.
        """
        if self.frames_since_last_move == self.reaction_time:
            if self._time_to_update_intelligence():
                self._update_intelligence()
            paddle_mid = paddle.y_pos + (paddle.height / 2)
            ball_mid = ball.y_pos + (ball.height / 2)
            # if the ball is below the paddles hit zone
            if ball.y_vel >= 0 and paddle_mid + self.hit_zone < ball_mid:
                return 1
            # if the ball is above the paddles hit zone
            if ball.y_vel <= 0 and paddle_mid - self.hit_zone > ball_mid:
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

    def get_position(self, elapsed):
        """ Returns a tuple containing the position of the object.
        Will update the position of the object based on game state.
        """
        self._update_position(elapsed)
        return (self.x_pos, self.y_pos)

    def _update_position(self, elapsed):
        """ Updates the position of the object, based on its current velocity
        and position.  this is where collision handling will occur.
        """
        new_x = self._next_x_position(elapsed)
        new_y = self._next_y_position(elapsed)
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

    def _next_x_position(self, elapsed):
        """ Returns the x position of the object after its next update.
        Does not actually modify the object's position.
        """
        return self.x_pos + self.x_vel * (self.speed * elapsed)

    def _next_y_position(self, elapsed):
        """ Returns the y position of the object after its next update.
        Does not actually modify the object's position.
        """
        return self.y_pos + self.y_vel * (self.speed * elapsed)

class Paddle(Pong_Object):
    """ A class for representing a paddle in pong.  Inherits from Pong_Object. """
    def __init__(self, pad_width, pad_height, x, y, move_speed, screen,
            obj_color=(255,255,255)):
        Pong_Object.__init__(self, pad_width, pad_height, x, y, move_speed,
                screen, obj_color=obj_color)
        self.score = 0

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
    def __init__(self, ball_diameter, x, y, move_speed, screen, bat_hit_sound, wall_hit_sound,
            score_sound, point_lost_sound, obj_color=(255, 255, 255)):
        Pong_Object.__init__(self, ball_diameter, ball_diameter, x, y,
                move_speed, screen, obj_color=obj_color)
        self.bat_hit_snd = bat_hit_sound
        self.wall_hit_snd = wall_hit_sound
        self.score_snd = score_sound
        self.point_lost_snd = point_lost_sound

    def copy(self):
        new_ball = Ball(self.width, self.x_pos, self.y_pos, self.speed, 
                self._screen_info, None, None, None, None)
        new_ball.x_vel = self.x_vel
        new_ball.y_vel = self.y_vel
        return new_ball

    def get_position(self, p1, p2, elapsed):
        """ 
        Override the base class's get_position method so that we can pass in the
        paddles.  This is necessary to handle collision with paddles.
        """
        self.update_position(p1, p2, elapsed)
        return (self.x_pos, self.y_pos)

    def _check_for_paddle_collision(self, paddle1, paddle2, elapsed):
        """ A private method for handling paddle collision. If the ball makes
        contact with a paddle, its direction on the x axis will be reversed.
        """
        new_x = self._next_x_position(elapsed)
        new_y = self._next_y_position(elapsed)
        # check if the ball will collide with the right paddle (player 1)
        if new_x > paddle1.x_pos-self.width and new_x < paddle1.x_pos + paddle1.width \
                and new_y > paddle1.y_pos and new_y < paddle1.y_pos + paddle1.height:
            delta_y = self.y_pos - (paddle1.y_pos + paddle1.height / 2)
            self.x_vel = -1
            self.y_vel = delta_y * 0.075 #+ (paddle1.y_vel / 2)
            if self.bat_hit_snd:
                self.bat_hit_snd.play()
        # check if the ball will collide with the left paddle (player 2)
        elif new_x < paddle2.x_pos + paddle2.width and new_x > paddle2.x_pos \
                and new_y > paddle2.y_pos and new_y < paddle2.y_pos + paddle2.height:
            delta_y = self.y_pos - (paddle2.y_pos + paddle2.height / 2)
            self.x_vel = 1
            self.y_vel = delta_y * 0.075 #+ (paddle2.y_vel / 2)
            if self.bat_hit_snd:
                self.bat_hit_snd.play()

    def _check_for_wall_collision(self, elapsed):
        """ A private method for handling wall collision. We only need to bounce off
        the top and bottom of the screen.
        """
        new_y = self._next_y_position(elapsed)
        # check for collision with the bottom of the screen
        if new_y > self._screen_info.height - self.height:
            self.y_vel *= -1
            if self.wall_hit_snd:
                self.wall_hit_snd.play()
        # check for collision with the top of the screen
        elif new_y < 0:
            self.y_vel *= -1
            if self.wall_hit_snd:
                self.wall_hit_snd.play()

    def update_position(self, p1, p2, elapsed):
        """
        Override the base class's update_position method so we can handle
        ball/paddle collision.
        """
        self._check_for_paddle_collision(p1, p2, elapsed)
        self._check_for_wall_collision(elapsed)
        self.x_pos = self._next_x_position(elapsed)
        self.y_pos  = self._next_y_position(elapsed)

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

    def is_dead_ball(self, paddle1, paddle2):
        """ Returns True if the ball has gone outside the bounds of the screen. """
        if self.x_pos > self._screen_info.width:
            self.point_lost_snd.play()
            paddle1.score += 1
            return True
        elif self.x_pos < 0:
            self.score_snd.play()
            paddle2.score += 1
            return True
        else:
            return False
