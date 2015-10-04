This is just a simple game of pong.

In order to play, you need to have pygame set up.

The major focus of this project is the game's artificial intelligence.  The AI consists
of three separate factors: the notion of a 'hit-zone', reaction-time, and position calculation.

The point on the paddle at which the ball hits affects its vertical speed.  The farther away
from the middle of the paddle, the faster the ball will move.  For example, a ball that bounces
off the top of the paddle will move upwards much faster than a ball that hits near the middle of
the paddle.

When the AI detects this increased speed, it will enter a 'focused' state.  It will attempt
to calculate the eventual position of the ball when the ball reaches the AI's paddle.  This results
in a reduction in reaction time.  So the AI can approximate the location it needs to move its paddle,
but it will be slower in getting it there.

The hit-zone is the AI's attempt to take advantage of the bounce-position dependant speed.  For now,
the hit zone is assigned and changes randomly.  At some point I will change this so that the AI
attempts to learn what the best hit-zones are.

To play the game:
    The game will load with a stationary ball in the middle.  To start the ball moving, press the
    space bar.  You control the right paddle, and use the up and down keys to do so.  If the ball
    passes your paddle, you lose the round and your opponent scores one point.  There is no score
    limit yet.  To quit, press the q key at any time.
