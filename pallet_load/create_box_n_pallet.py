from pathlib import Path
from pxr import Usd, UsdGeom, Gf

work_dir = Path(__file__).parent
file_path = str(work_dir / "_asset/full_box_n_pallet.usda")
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
world_xform = UsdGeom.Xform.Define(stage, "/World")
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetDefaultPrim(world_xform)

