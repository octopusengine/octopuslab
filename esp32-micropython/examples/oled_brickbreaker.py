# octopusLAB simple xexample
# HW: ESP32 + i2c OLED display
# import examples.oled_pong

# imports
from time import sleep_ms
from util.octopus import *
from util.display_segment import displayDigit

octopus()            # include main library

# constants
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

PADDLE_HEIGHT = 3
PADDLE_WIDTH = 16
BALL_SIZE = 5
BRICK_WIDTH = 12
BRICK_HEIGHT = 4

OLED = oled_init(SCREEN_WIDTH, SCREEN_HEIGHT)      # init oled display
OLED.clear()            # clear
L, R, C = buttons_init()

printTitle("oled_pong.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

class twoDObject():
   def __init__(self, x, y, width, height):
      self.x = x
      self.y = y
      self.width = width
      self.height = height

   def valueInRange(self, value, min, max):
      return (value >= min) and (value <= max)

   def isTouching(self, anotherObject):
      xOverlap = self.valueInRange(self.x, anotherObject.x, anotherObject.x + anotherObject.width)  or self.valueInRange(anotherObject.x, self.x, self.x + self.width)
      yOverlap = self.valueInRange(self.y, anotherObject.y, anotherObject.y + anotherObject.height) or self.valueInRange(anotherObject.y, self.y, self.y + self.height)
      return xOverlap and yOverlap

class Ball(twoDObject):
   def __init__(self):
      super().__init__(int(SCREEN_WIDTH/2), SCREEN_HEIGHT-PADDLE_HEIGHT-BALL_SIZE, BALL_SIZE, BALL_SIZE)
      self.xold = self.x
      self.yold = self.y
      self.vx   = 3
      self.vy   = 3

   def draw(self):
      OLED.fill_rect(self.xold, self.yold, BALL_SIZE, BALL_SIZE, 0)
      OLED.fill_rect(self.x,    self.y,    BALL_SIZE, BALL_SIZE, 1)
      OLED.show()

   def bounce(self):
      if(self.x > SCREEN_WIDTH - BALL_SIZE):  self.vx = -self.vx   # right edge
      if(self.x < 0):                         self.vx = -self.vx   # left  edge
      if(self.y > SCREEN_HEIGHT - BALL_SIZE): self.vy = -self.vy   # upper edge
      if(self.y < 0):                         self.vy = -self.vy   # lower edge

class Brick(twoDObject):
   def __init__(self, x, y):
      super().__init__(x, y, BRICK_WIDTH, BRICK_HEIGHT)

   def draw(self):
      OLED.rect(self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT, 1)
      OLED.show()

   def undraw(self):
      OLED.rect(self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT, 0)
      OLED.show()
      self.x = 2048     # write a delete function
      self.y = 1024

class Paddle(twoDObject):   
   def __init__(self):
      super().__init__(int((SCREEN_WIDTH-PADDLE_WIDTH)/2), SCREEN_HEIGHT-PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)
      self.xold = self.x

   def draw(self):
      OLED.fill_rect(self.xold, self.y, PADDLE_WIDTH, PADDLE_HEIGHT, 0)
      OLED.fill_rect(self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT, 1)
      OLED.show()
   
class oled_pong:
   def __init__(self):
      paddle = Paddle()
      ball = Ball()
      self.createBricks()

      paddle.draw()
      ball.draw()

      self.run(ball, paddle)

   def createBricks(self):
      BRICK_HOR_OFFSET = 8
      BRICK_VER_OFFSET = 8
      brick_y = 8
      brickCount = 6
      brickRow = 2
      brick_x = 6
      self.bricks = []
      for i in range (brickRow):
         for ind in range (brickCount):         
            self.bricks.append(Brick(brick_x, brick_y))
            self.bricks[i*brickCount+ind].draw()
            brick_x += BRICK_WIDTH + BRICK_HOR_OFFSET
         brick_x = 6
         brick_y += BRICK_HEIGHT + BRICK_VER_OFFSET

   def getInput(self, step = 4):
      if button(L)[0] > 8: return -step
      if button(R)[0] > 8: return step
      return 0

   def dtctCollision(self, ball, paddle):
      if(ball.isTouching(paddle)): ball.vy = -ball.vy
      for brick in self.bricks:
         if(ball.isTouching(brick)):
            brick.undraw()
            ball.vy = -ball.vy

   def run(self, ball, paddle):
      while True:
         ball.xold = ball.x
         ball.yold = ball.y
         ball.x += ball.vx
         ball.y += ball.vy
         paddle.xold = paddle.x
         paddle.x = (paddle.xold + self.getInput()) % SCREEN_WIDTH
         
         self.dtctCollision(ball, paddle)
         ball.bounce()
         ball.draw()
         paddle.draw()
         
         sleep_ms(3)

if __name__ == "__main__":
	oled_pong().start_game()