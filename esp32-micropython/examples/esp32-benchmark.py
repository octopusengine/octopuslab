import time

def test1():
  for _ in range(0,1000000):
    pass

@micropython.native
def test2():
  for _ in range(0,1000000):
    pass


@micropython.viper
def test3():
  for _ in range(0,1000000):
    pass

print("Test will do 1 000 000 iterations in for")
print("Running without optimalization");
st = time.ticks_ms()
test1()
print("Took {}ms".format(time.ticks_ms() - st))

print("Running with native optimalization");
st = time.ticks_ms()
test2()
print("Took {}ms".format(time.ticks_ms() - st))

print("Running with viper optimalization");
st = time.ticks_ms()
test3()
print("Took {}ms".format(time.ticks_ms() - st))
