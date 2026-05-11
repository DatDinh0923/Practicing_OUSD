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

base_class = stage.CreateClassPrim("/_Base_Prop")
world_xform.GetPrim().GetSpecializes().AddSpecialize(base_class.GetPath())

status_varset = world_xform.GetPrim().GetVariantSets().AddVariantSet("box_status")
status_varset.AddVariant("intact")
status_varset.AddVariant("damaged")

# Default variant
status_varset.SetVariantSelection("intact")
# authoring data inside variant
status_varset.SetVariantSelection("damaged")

with status_varset.GetVariantEditContext():
    over_prim = stage.OverridePrim("/Box/Box_001")
    box_geom = UsdGeom.Cube(over_prim)
    box_geom.GetDisplayColorAttr().Set([(0.7, 0.3, 0.1)])
    box_geom.AddScaleOp().Set(Gf.Vec3f(1.0, 0.7, 1.0))

# Revert to default state before saving
status_varset.SetVariantSelection("intact")

stage.Save()