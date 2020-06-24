# octopusLAB simple xexample
# HW: ESP32 + i2c OLED display
# import examples.oled_brickbreaker

# imports
from time import sleep_ms
from util.octopus import *
from shell.terminal import printTitle
from util.display_segment import displayDigit

octopus()            # include main library

# constants
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

PADDLE_WIDTH = 16
PADDLE_HEIGHT = 3
PADDLE_Y = 54
BALL_SIZE = 5


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

class oled_pong:

   def __init__(self):
      #print("__init__")
      self.start_game(self)

   def start_game(self, start_lives = 3):
      x = int(SCREEN_WIDTH/2)
      y = 50
      paddle_x = x-int(PADDLE_WIDTH/2)
      self.score = 0

      self.vx = 3
      self.vy = 3
      self.drawBall(x,y,x,y)
      self.drawPaddle(paddle_x, paddle_x)
      self.run(x, y, paddle_x)

   def drawBall(self, xold, yold, x, y):
      OLED.fill_rect(xold, yold, BALL_SIZE, BALL_SIZE, 0)
      OLED.fill_rect(x, y, BALL_SIZE, BALL_SIZE, 1)
      OLED.show()

   def drawPaddle(self, xold, x):
      OLED.fill_rect(xold, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT, 0)
      OLED.fill_rect(x, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT, 1)
      OLED.show()

   def getInput(self, step = 4):
      if button(L)[0] > 8: return -step
      if button(R)[0] > 8: return step
      return 0

   def dtctCollision(self, x, y, paddle_x):
      if x > SCREEN_WIDTH - BALL_SIZE: self.vx = -self.vx
      if x < 0: self.vx = -self.vx
      if y > SCREEN_HEIGHT - BALL_SIZE: self.vy = -self.vy
      if y < 0:
         self.vy = -self.vy
         self.score += 1
         #displayNum(score)

      if x + BALL_SIZE > paddle_x and x < paddle_x + PADDLE_WIDTH and y + BALL_SIZE >= PADDLE_Y and y + BALL_SIZE <= PADDLE_Y + PADDLE_HEIGHT:
         self.vy = -self.vy

   def run(self, x, y, paddle_x):
      while True:
         xold = x
         yold = y
         x += self.vx
         y += self.vy
         
         self.dtctCollision(x, y, paddle_x)
         self.drawBall(xold,yold,x,y)
         step = self.getInput()
         #if paddle_x > 0 and paddle_x + PADDLE_WIDTH < SCREEN_WIDTH: 
         paddle_x += step
         paddle_x %= SCREEN_WIDTH
         #print(step)
         self.drawPaddle(paddle_x-step, paddle_x)
         sleep_ms(3)

if __name__ == "__main__":
	oled_pong().run(64, 50, 56)
