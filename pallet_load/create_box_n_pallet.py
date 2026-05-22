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
# Define target box dimensions dynamically
box_w, box_h, box_d = 20.0, 20.0, 20.0
grid_x, grid_y, grid_z = 4, 4, 4         # A 4x4x4 stack
# Accumulate Spacing Pattern
# Start Coordinate = - (total stack dim / 2.0) + (box dim / 2.0)

# This centers the box grid over the exact middle of the pallet
start_x = -((grid_x * box_w) / 2.0) + (box_w / 2.0)
start_z = -((grid_z * box_d) / 2.0) + (box_d / 2.0)

# Calculate the precise surface contact point automatically
pallet_top_y = 0.75
calculated_y = pallet_top_y + (box_h / 2.0)

# The pallet top deck surface sits exactly at Y = 0.75
pallet_top_y = 0.75
start_y = pallet_top_y + (box_h / 2.0)

# --- 4. THE NESTED INSTANCING LOOPS ---
box_idx = 1

for y in range(grid_y):          # Vertical Layers (Height)
    for x in range(grid_x):      # Left to Right (Width)
        for z in range(grid_z):  # Front to Back (Depth)
            
            # Formulate unique path name
            box_path = geom_scope.GetPath().AppendPath(f"Box_{box_idx:03d}")
            box_prim = stage.DefinePrim(box_path)
            
            # Attach the external box template reference
            box_prim.GetReferences().AddReference("./box.usda")
            
            # ACTIVATE INSTANCING: This tells USD to share data under the hood!
            box_prim.SetInstanceable(True)
            
            # --- CALCULATE STEPPING POSITIONS ---
            curr_x = start_x + (x * box_w)
            curr_y = start_y + (y * box_h)
            curr_z = start_z + (z * box_d)
            
            # Apply absolute transformations via XformCommonAPI
            xform_api = UsdGeom.XformCommonAPI(box_prim)
            xform_api.SetTranslate(Gf.Vec3d(curr_x, curr_y, curr_z))
            xform_api.SetScale(Gf.Vec3f(box_w, box_h, box_d))
            
            box_idx += 1

stage.Save()
