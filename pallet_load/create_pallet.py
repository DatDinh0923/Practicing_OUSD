from pathlib import Path
from pxr import Usd, UsdGeom, Gf
# The creating defualt world
work_dir = Path(__file__).parent
file_path = str(work_dir / "_asset/pallet.usda")
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
world_pallet_xform = UsdGeom.Xform.Define(stage, "/World")
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetDefaultPrim(world_pallet_xform.GetPrim())

base_class = stage.CreateClassPrim("/_Base_Prop")
world_pallet_xform.GetPrim().GetSpecializes().AddSpecialize(base_class.GetPath())

# Creating prototypes scope
prototype_scope = UsdGeom.Scope.Define(stage, world_pallet_xform.GetPath().AppendPath("Prototypes"))
prototype_scope.CreateVisibilityAttr().Set(UsdGeom.Tokens.invisible)

# Creating plank prototypes
plank_proto_handle = UsdGeom.Xform.Define(stage, prototype_scope.GetPath().AppendPath("PlankHandle"))
plank_prototype = UsdGeom.Cube.Define(stage, plank_proto_handle.GetPath().AppendPath("Plank"))
plank_prototype.CreateDisplayColorAttr([(0.6509803921568628, 0.615686274509804, 0.43529411764705883)])
plank_prototype.CreateSizeAttr().Set(1.0)
# plank_prototype.AddTransformOp()
# plank_prototype.AddScaleOp()

# Creating Block prototypes
legblock_proto_handle = UsdGeom.Xform.Define(stage, prototype_scope.GetPath().AppendPath("LegBlockHandle"))
legblock_prototype = UsdGeom.Cube.Define(stage, legblock_proto_handle.GetPath().AppendPath("LegBlock"))
legblock_prototype.CreateDisplayColorAttr([(0.5686274509803921, 0.4588235294117647, 0.30196078431372547)])
# legblock_prototype.AddScaleOp()
legblock_prototype.CreateSizeAttr().Set(1.0)
# legblock_prototype.AddTransformOp()
# legblock_prototype.AddScaleOp()


# Plank things
def generate_axis_layout(total_length, element_widths, gap_mask):
    total_material_width = sum(element_widths)
    total_gaps = sum(gap_mask)
    gap_size = (total_length - total_material_width) / total_gaps if total_gaps > 0 else 0
    current_edge = -total_length / 2

    layout = []
    for i, width in enumerate(element_widths):
        centre_pos = current_edge + (width / 2)
        layout.append((centre_pos, width))
        current_edge += width

        if i < len(gap_mask) and gap_mask[i]:
            current_edge += gap_size
    
    return layout

top_plank_widths = [11.0, 13.0] + [9.5]*5 + [13.0, 11.0]
top_plank_has_gap = [False] + [True]*6 + [False]
stringer_widths = [9.5]*3
stringer_has_gap = [True]*2
bottom_plank_2pcs_widths = [9.5]*2
bottom_plank_2pcs_has_gap = [True]
bottom_plank_3pcs_widths = [9.5]*3
bottom_plank_3pcs_has_gap = [True]*2

top_planks_pos = generate_axis_layout(
    total_length=120,
    element_widths = top_plank_widths,
    gap_mask = top_plank_has_gap
)

stringer_pos = generate_axis_layout(
    total_length=120,
    element_widths = stringer_widths,
    gap_mask = stringer_has_gap
)

bottom_plank_2pcs_pos = generate_axis_layout(
    total_length=120,
    element_widths = bottom_plank_2pcs_widths,
    gap_mask = bottom_plank_2pcs_has_gap
)

bottom_plank_3pcs_pos = generate_axis_layout(
    total_length=120,
    element_widths = bottom_plank_3pcs_widths,
    gap_mask = bottom_plank_3pcs_has_gap
)
for i, (pos, width) in enumerate(top_planks_pos):
    top_plank_xform = UsdGeom.Xform.Define(stage,  world_pallet_xform.GetPath().AppendPath(f"TopPlank_{i+1:02d}"))
    top_plank_xform.GetPrim().GetReferences().AddInternalReference(plank_proto_handle.GetPath())
    top_plank_xform.GetPrim().SetInstanceable(True)
    top_plank_xform.AddTranslateOp().Set(Gf.Vec3d(0 ,0, pos))
    top_plank_xform.AddScaleOp().Set(Gf.Vec3f(120.0, 1.5, width))

for i, (pos, width) in enumerate(stringer_pos):
    stringer_xform = UsdGeom.Xform.Define(stage,  world_pallet_xform.GetPath().AppendPath(f"Stringer_{i+1:02d}"))
    stringer_xform.GetPrim().GetReferences().AddInternalReference(plank_proto_handle.GetPath())
    stringer_xform.GetPrim().SetInstanceable(True)
    stringer_xform.AddTranslateOp().Set(Gf.Vec3d(pos ,-2.0, 0))
    stringer_xform.AddScaleOp().Set(Gf.Vec3f(width, 2.5, 120.0))

for i, (pos, width) in enumerate(bottom_plank_2pcs_pos):
    zwei_xform = UsdGeom.Xform.Define(stage,  world_pallet_xform.GetPath().AppendPath(f"Zwei_{i+1:02d}"))
    zwei_xform.GetPrim().GetReferences().AddInternalReference(plank_proto_handle.GetPath())
    zwei_xform.GetPrim().SetInstanceable(True)
    zwei_xform.AddTranslateOp().Set(Gf.Vec3d(0 ,-14, pos))
    zwei_xform.AddScaleOp().Set(Gf.Vec3f(120.0, 2.5, width))

for i, (pos, width) in enumerate(bottom_plank_3pcs_pos):
    drei_xform = UsdGeom.Xform.Define(stage,  world_pallet_xform.GetPath().AppendPath(f"Drei_{i+1:02d}"))
    drei_xform.GetPrim().GetReferences().AddInternalReference(plank_proto_handle.GetPath())
    drei_xform.GetPrim().SetInstanceable(True)
    drei_xform.AddTranslateOp().Set(Gf.Vec3d(pos ,-14, 0))
    drei_xform.AddScaleOp().Set(Gf.Vec3f(width, 2.5, 101.0))

# LegBlock things

# Exact X properties: (Center_X, Size_X)
# Left corner block, Middle block, Right corner block
def calculate_block_positions(total_length, outer_size, inner_size):
    """
    Automatically calculates the 3 center positions and sizes for a row of blocks.
    Ensures the outer blocks sit perfectly flush with the pallet edges.
    """
    # Left/Front block center (flush with negative edge)
    min_pos = -total_length / 2.0 + outer_size / 2.0

    
    # Center block is always at 0.0
    mid_pos = 0.0
    
    # Right/Back block center (flush with positive edge)
    max_pos = total_length / 2.0 - outer_size / 2.0

    
    # Return a list of (position, size) tuples matching your matrix format
    return [
        (min_pos, outer_size),
        (mid_pos, inner_size),
        (max_pos, outer_size)
    ]


# X-Axis: 120cm total length, outer blocks are 16cm, center is 9.5cm
z_axis_120 = calculate_block_positions(total_length=120.0, outer_size=16.0, inner_size=9.5)

# Z-Axis runs along the 100cm Depth: All blocks are 9.5cm deep
x_axis_100 = calculate_block_positions(total_length=120.0, outer_size=9.5, inner_size=9.5)


# --- 2. THE CLEAN GRID GENERATOR ---
block_idx = 1

for z_pos, z_scale in z_axis_120:
    for x_pos, x_scale in x_axis_100:
        block_path = world_pallet_xform.GetPath().AppendPath(f"LegBlock_{block_idx:02d}")
        block_xform = UsdGeom.Xform.Define(stage, block_path)
        block_xform.GetPrim().GetReferences().AddInternalReference(legblock_proto_handle.GetPath())
        block_xform.GetPrim().SetInstanceable(True)
        
        # --- POSITION ---
        block_xform.AddTranslateOp().Set(Gf.Vec3d(x_pos, -8, z_pos))
        
        # --- SCALE ---
        block_xform.AddScaleOp().Set(Gf.Vec3f(x_scale, 9.5, z_scale))
        
        block_idx += 1

stage.Save()