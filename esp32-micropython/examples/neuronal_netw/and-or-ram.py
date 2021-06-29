# ramdisk for temp nn file
# MicroMLP - multilayer perceptron

from utils.ramdisk import RAMBlockDev
from time import sleep
from microMLP import MicroMLP
from components.led import Led
import os

led = Led(2)
led.blink()

print("---RAM disk init---")

bdev = RAMBlockDev(512, 50) # 512/1024/2048 ok
os.VfsLfs2.mkfs(bdev)
# os.VfsFat.mkfs(bdev)
os.mount(bdev, '/ramdisk')

print("---MLP init---")
mlp = MicroMLP.Create( neuronsByLayers           = [3, 2, 1],
                       activationFuncName        = MicroMLP.ACTFUNC_GAUSSIAN,
                       layersAutoConnectFunction = MicroMLP.LayersFullConnect )

nnFalse  = MicroMLP.NNValue.FromBool(False)
nnTrue   = MicroMLP.NNValue.FromBool(True)
# and
mlp.AddExample( [nnTrue, nnFalse, nnFalse], [nnFalse] )
mlp.AddExample( [nnTrue, nnFalse, nnTrue ], [nnFalse] )
mlp.AddExample( [nnTrue, nnTrue , nnTrue ], [nnTrue] )
mlp.AddExample( [nnTrue, nnTrue , nnFalse], [nnFalse] )
# or
mlp.AddExample( [nnFalse, nnFalse, nnFalse], [nnFalse] )
mlp.AddExample( [nnFalse, nnFalse, nnTrue ], [nnTrue] )
mlp.AddExample( [nnFalse, nnTrue , nnTrue ], [nnTrue] )
mlp.AddExample( [nnFalse, nnTrue , nnFalse], [nnTrue] )

learnCount = mlp.LearnExamples()

print( "LEARNED --- AND ---" )
print( "  - False and False = %s" % mlp.Predict([nnTrue, nnFalse, nnFalse])[0].AsBool )
print( "  - False and True  = %s" % mlp.Predict([nnTrue, nnFalse, nnTrue] )[0].AsBool )
print( "  - True  and False = %s" % mlp.Predict([nnTrue, nnTrue , nnFalse] )[0].AsBool )
print( "  - True  and True  = %s" % mlp.Predict([nnTrue, nnTrue , nnTrue] )[0].AsBool )
print( "LEARNED --- OR ---" )
print( "  - False and False = %s" % mlp.Predict([nnFalse, nnFalse, nnFalse])[0].AsBool )
print( "  - False and True  = %s" % mlp.Predict([nnFalse, nnFalse, nnTrue] )[0].AsBool )
print( "  - True  and False = %s" % mlp.Predict([nnFalse, nnTrue , nnFalse] )[0].AsBool )
print( "  - True  and True  = %s" % mlp.Predict([nnFalse, nnTrue , nnTrue] )[0].AsBool )

mlp.SaveToFile("ramdisk/nn.json") # ... LoadFromFile()
