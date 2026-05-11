import os
from pathlib import Path
from pxr import Usd, UsdGeom, Gf

work_dir = Path(__file__).parent
file_path = str(work_dir/ "_asset/box.usda")
if os.path.exists(file_path):
    os.remove(file_path)
# Define new stage, make /Box become default prim, set unit and axis
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
world_xform = UsdGeom.Xform.Define(stage, "/Box")
stage.SetDefaultPrim(world_xform.GetPrim())
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

# Adding payload arc to /_asset/box_payload.usda
world_xform.GetPrim().GetPayloads().AddPayload("./box_payload.usda")


# extendHint (optinal, this is still hardcoded, this is so that it can tell the exact bbox of the box, without loading the payload at all)
model_api = UsdGeom.ModelAPI.Apply(world_xform.GetPrim())
model_api.SetExtentsHint(
    [Gf.Vec3f(-50.0, -50.0, -50.0), Gf.Vec3f(50.0, 50.0, 50.0)]
)
stage.Save()
