from microMLP import MicroMLP
mlp = MicroMLP.Create( neuronsByLayers           = [2, 2, 1],
                       activationFuncName        = MicroMLP.ACTFUNC_GAUSSIAN,
                       layersAutoConnectFunction = MicroMLP.LayersFullConnect )

nnFalse  = MicroMLP.NNValue.FromBool(False)
nnTrue   = MicroMLP.NNValue.FromBool(True)

mlp.AddExample( [nnFalse, nnFalse], [nnFalse] )
mlp.AddExample( [nnFalse, nnTrue ], [nnFalse] )
mlp.AddExample( [nnTrue , nnTrue ], [nnTrue] )
mlp.AddExample( [nnTrue , nnFalse], [nnFalse] )

learnCount = mlp.LearnExamples()

print( "LEARNED :" )
print( "  - False and False = %s" % mlp.Predict([nnFalse, nnFalse])[0].AsBool )
print( "  - False and True  = %s" % mlp.Predict([nnFalse, nnTrue] )[0].AsBool )
print( "  - True  and True  = %s" % mlp.Predict([nnTrue , nnTrue] )[0].AsBool )
print( "  - True  and False = %s" % mlp.Predict([nnTrue , nnFalse])[0].AsBool )