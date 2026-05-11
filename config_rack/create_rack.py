import os
from pathlib import Path
from pxr import Usd, UsdGeom, Gf

work_path = Path(__file__).parent
file_path = str(work_path / "_asset/rack.usda")
if os.path.exists(file_path):
    os.remove(file_path)
# Make a stage, define default prim
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
world_xform = UsdGeom.Xform.Define(stage, "/World")
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetDefaultPrim(world_xform.GetPrim())

# Make a Rackprim
prototype_scope = UsdGeom.Scope.Define(stage, world_xform.GetPath().AppendPath("Prototypes"))
beam_prototype = UsdGeom.Cube.Define(stage, prototype_scope.GetPath().AppendPath("Beam"))
beam_prototype.GetDisplayColorAttr().Set([(0.4,0.45,0.45)])
UsdGeom.Xformable(beam_prototype).AddScaleOp().Set(Gf.Vec3f(0.1, 2.0 ,0.1))

positions = [
    (-5,0,5),
    (5,0,5),
    (-5,0,5),
    (5,0,-5)
]

for i, pos in enumerate(positions):
    leg_path = world_xform.GetPrim().GetPath().AppendPath(f"Leg_00{i+1}")
    leg_prim = stage.DefinePrim(leg_path)
    leg_prim.GetReferences().AddInternalReference(beam_prototype.GetPath())
    UsdGeom.Xformable(leg_prim).AddTranslateOp().Set(Gf.Vec3d(pos))


stage.Save()