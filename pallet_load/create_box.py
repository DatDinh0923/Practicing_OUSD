from pathlib import Path
from pxr import Usd, UsdGeom, Gf

# Basic setting up carton box file
work_dir = Path(__file__).parent
file_path = str(work_dir / "_asset/box.usda")
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
world_xform = UsdGeom.Xform.Define(stage, "/World")
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetDefaultPrim(world_xform.GetPrim())

cube_box = UsdGeom.Cube.Define(stage, "/World/Box")
cube_box.GetDisplayColorAttr().Set([(0.76, 0.6, 0.42)])
cube_box.CreateSizeAttr().Set(1.0)
# cube_box.AddScaleOp().Set(Gf.Vec3f(120, 2.5, 9.5)) # zyx, blue green red, tesing plank
stage.Save()
