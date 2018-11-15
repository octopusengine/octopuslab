echo Welcome to basic octopusLAB script!
echo (edit for your COM port)
pause
ampy -p /COM6 put boot.py
ampy -p /COM6 put ./octopus_robot_board.py

ampy -p /COM6 mkdir lib
ampy -p /COM6 put ./lib/ssd1306.py lib/ssd1306.py
ampy -p /COM6 put ./lib/temperature.py lib/temperature.py

ampy -p /COM6 mkdir config

ampy -p /COM6 mkdir util
ampy -p /COM6 put ./util/setup.py util/setup.py
ampy -p /COM6 put ./util/octopus.py util/octopus.py
ampy -p /COM6 ls util

echo start: 
echo >>> octopus() 
