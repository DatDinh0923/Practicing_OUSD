import os
from pathlib import Path
from pxr import Usd, UsdGeom, Gf

work_dir = Path(__file__).parent
file_path = str(work_dir / "_asset/roller.usda")
if os.path.exists(file_path):
    os.remove(file_path)

stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
world_xform = UsdGeom.Xform.Define(stage, "/World")  
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetDefaultPrim(world_xform.GetPrim())

roller = UsdGeom.Cylinder.Define(stage, "/World/Roller")
roller.GetDisplayColorAttr().Set([(0.25, 0.4, 0.8)])
roller.AddScaleOp().Set(Gf.Vec3f(1.0, 1.0, 5.0))

stage.Save()

