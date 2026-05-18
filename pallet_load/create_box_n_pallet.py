from pathlib import Path
from pxr import Usd, UsdGeom, Gf

work_dir = Path(__file__).parent
file_path = str(work_dir / "_asset/full_box_n_pallet.usda")
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
world_xform = UsdGeom.Xform.Define(stage, "/World")
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetDefaultPrim(world_xform.GetPrim())

geom_scope = UsdGeom.Scope.Define(stage, world_xform.GetPrim().GetPath().AppendPath("Geometry"))
pallet_path = geom_scope.GetPrim().GetPath().AppendPath("Pallet")
pallet_prim = stage.DefinePrim(pallet_path)
pallet_prim.GetReferences().AddReference("./pallet.usda")

box_path = geom_scope.GetPrim().GetPath().AppendPath("Box")
box_prim = stage.DefinePrim(box_path)
box_prim.GetReferences().AddReference("./box.usda")
# UsdGeom.Xformable(box_prim).AddScaleOp().Set(Gf.Vec3f(50, 50, 50))
# UsdGeom.Xformable(box_prim).AddTranslateOp().Set(Gf.Vec3d(0,0.515,0))
# Define your target box dimensions dynamically
box_w, box_h, box_d = 50.0, 50.0, 50.0

# Calculate the precise surface contact point automatically
pallet_top_y = 0.75
calculated_y = pallet_top_y + (box_h / 2.0)

# Use XformCommonAPI to handle the transform matrix order safely
xform_api = UsdGeom.XformCommonAPI(box_prim)
xform_api.SetScale(Gf.Vec3f(box_w, box_h, box_d))
xform_api.SetTranslate(Gf.Vec3d(0, calculated_y, 0))

stage.Save()

stage.Save()

