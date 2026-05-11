import os
from pathlib import Path
from pxr import Usd, UsdGeom, Gf

work_path = Path(__file__).parent
file_path = str(work_path / "_asset/conveyor_segment.usda")
if os.path.exists(file_path):
    os.remove(file_path)


stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
converyor_xform: UsdGeom.Xform = UsdGeom.Xform.Define(stage, "/Conveyor_Segment")
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetDefaultPrim(converyor_xform.GetPrim())

# Geometry Scope? Should I add a scope?
geom_scope = UsdGeom.Scope.Define(stage, converyor_xform.GetPath().AppendPath("Geometry"))
geom_scope_prim = geom_scope.GetPrim()

for i in range(3):
    roller_path = geom_scope_prim.GetPath().AppendPath(f"Roller_00{i+1}")
    roller_prim = stage.DefinePrim(roller_path)
    #Adding Reference to roller
    roller_prim.GetReferences().AddReference("./roller.usda")
    UsdGeom.Xformable(roller_prim).AddTranslateOp().Set(Gf.Vec3d(i*50, 0, 0))

stage.Save()