import os
from pathlib import Path
from pxr import Usd, UsdGeom

work_dir = Path(__file__).parent
file_path = str(work_dir / "_asset/box_payload.usda")
if os.path.exists(file_path):
    os.remove(file_path)
# Create new Stage and set Unit and UP Axis
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters) 
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# Define Xform World Root and Set defualt prim
world_xform = UsdGeom.Xform.Define(stage, "/World")
stage.SetDefaultPrim(world_xform.GetPrim()) # Set the default prim for referencing/payloading

# Define a brown cube
cube = UsdGeom.Cube.Define(stage, "/World/Box_001")
cube.GetDisplayColorAttr().Set([(0.5, 0.3, 0.1)])

stage.Save()
