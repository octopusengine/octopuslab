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

PADDLE_WIDTH = 16
PADDLE_HEIGHT = 3
PADDLE_Y = 54
BALL_SIZE = 5
BRICK_WIDTH = 12
BRICK_HEIGHT = 4
BRICK_HOR_OFFSET = 8
BRICK_VER_OFFSET = 8

OLED = oled_init(SCREEN_WIDTH, SCREEN_HEIGHT)      # init oled display
OLED.clear()            # clear
L, R, C = buttons_init()

# def displayNum(num):
#     num = str(num)
#     for n in range(len(num)):
#         displayDigit(OLED, int(num[n]), n, 2, 6)

# default coordinates for position


printTitle("oled_pong.py")
print("this is simple Micropython example | ESP32 & octopusLAB")
print()

# superObject class with isTouching function to ameliorate collision check chaos
class Ball:
   def __init__(self):
      self.x = int(SCREEN_WIDTH/2)
      self.y = 50
      self.xold = self.x
      self.yold = self.y
      self.vx = 3
      self.vy = 3

   def draw(self):
      OLED.fill_rect(self.xold, self.yold, BALL_SIZE, BALL_SIZE, 0)
      OLED.fill_rect(self.x, self.y, BALL_SIZE, BALL_SIZE, 1)
      OLED.show()

class Brick:
   def __init__(self, x, y):
      self.x = x
      self.y = y

   def draw(self):
      OLED.fill_rect(self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT, 1)
      OLED.show()

   def undraw(self):
      OLED.fill_rect(self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT, 0)
      OLED.show()
      self.x = 2048     # write a delete function
      self.y = 1024

class Paddle:
   def __init__(self):
      self.x = int((SCREEN_WIDTH-PADDLE_WIDTH)/2)
      self.xold = self.x

   def draw(self):
      OLED.fill_rect(self.xold, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT, 0)
      OLED.fill_rect(self.x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT, 1)
      OLED.show()
   
class oled_pong:

   def __init__(self):
      print("__init__")
      self.start_game(self)

   def start_game(self, start_lives = 3):
      print("start_game")
      paddle = Paddle()
      ball = Ball()
      self.createBricks()
      
      self.score = 0
      paddle.draw()
      ball.draw()
      
      self.run(ball, paddle)

   def createBricks(self):
      brick_y = 20
      brickCount = 8
      brick_x = 6
      self.bricks = []
      for ind in range (brickCount):         
         self.bricks.append(Brick(brick_x, brick_y))
         self.bricks[ind].draw()
         brick_x += BRICK_WIDTH + BRICK_VER_OFFSET

   def getInput(self, step = 4):
      if button(L)[0] > 8: return -step
      if button(R)[0] > 8: return step
      return 0

   def dtctCollision(self, ball, paddle):
      if ball.x > SCREEN_WIDTH - BALL_SIZE: ball.vx = -ball.vx
      if ball.x < 0: ball.vx = -ball.vx
      if ball.y > SCREEN_HEIGHT - BALL_SIZE: ball.vy = -ball.vy
      if ball.y < 0:
         ball.vy = -ball.vy
         self.score += 1
         #displayNum(score)

      if ball.x + BALL_SIZE > paddle.x and ball.x < paddle.x + PADDLE_WIDTH and ball.y + BALL_SIZE >= PADDLE_Y and ball.y + BALL_SIZE <= PADDLE_Y + PADDLE_HEIGHT:
         ball.vy = -ball.vy

      for brick in self.bricks:
         if ball.x + BALL_SIZE > brick.x and ball.x < brick.x + BRICK_WIDTH and brick.y + BALL_SIZE >= brick.y and ball.y + BALL_SIZE <= brick.y + BRICK_HEIGHT:
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
         ball.draw()
         paddle.draw()
         
         #if paddle_x > 0 and paddle_x + PADDLE_WIDTH < SCREEN_WIDTH: 
         #print(step)
         #self.draw(paddle_x-step, paddle_x)
         sleep_ms(3)

if __name__ == "__main__":
	oled_pong().start_game()