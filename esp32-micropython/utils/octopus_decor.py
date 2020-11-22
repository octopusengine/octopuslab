# this module is "decorators" library for Octopus FrameWork
# usage:
# @octopus_debug
# def yourFunc(): ...

def octopus_debug(ledon=False,info=True):
   if ledon:
         from components.led import Led
         led = Led(2)
         
   def _octopus_debug(fnc):
      import time
      print("--- decorator --- @octopus_debug:")
      #if ledon: led.blink()
      
      try:
            fname = fnc.__name__
      except:
            fname = "?"
      
      def ff(*args, **kwargs):
         if ledon: led.value(1)
         start = time.time()
         result = fnc(*args, **kwargs)
         end = time.time() - start
         if ledon: led.value(0)
         
         print("=== function name: ", fname)
         print("=== duration (sec.) --->", str(end))
         return result

      return ff
   return _octopus_debug
