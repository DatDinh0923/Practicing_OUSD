import os
from pathlib import Path
from pxr import Usd, UsdGeom, Gf

work_path = Path(__file__).parent
file_path = str(work_path / "_asset/rack.usda")
if os.path.exists(file_path):
    os.remove(file_path)
# Make a stage, define default prim
stage: Usd.Stage = Usd.Stage.CreateNew(file_path)
world_xform = UsdGeom.Xform.Define(stage, "/Rack")
UsdGeom.SetStageMetersPerUnit(stage, UsdGeom.LinearUnits.centimeters)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
stage.SetDefaultPrim(world_xform.GetPrim())

base_class = stage.CreateClassPrim("/_Base_Prop")
world_xform.GetPrim().GetSpecializes().AddSpecialize(base_class.GetPath())

# Make a Rackprim
## Beam
prototype_scope = UsdGeom.Scope.Define(stage, world_xform.GetPath().AppendPath("Prototypes"))
prototype_scope.CreateVisibilityAttr().Set(UsdGeom.Tokens.invisible)

beam_proto_handle = UsdGeom.Xform.Define(stage, "/Rack/Prototypes/BeamHandle")
beam_prototype = UsdGeom.Cube.Define(stage, beam_proto_handle.GetPath().AppendPath("Beam"))
beam_prototype.CreateDisplayColorAttr()#.Set([(0.4,0.45,0.45)])
beam_prototype.AddScaleOp()#.Set(Gf.Vec3f(0.1, 2.0 ,0.1))

## Shelf
shelf_proto_handle = UsdGeom.Xform.Define(stage, "/Rack/Prototypes/ShelfHandle")
shelf_prototype = UsdGeom.Cube.Define(stage, shelf_proto_handle.GetPath().AppendPath("Shelf"))
shelf_prototype.CreateDisplayColorAttr().Set([(0.6, 0.4, 0.2)])
shelf_prototype.AddScaleOp().Set(Gf.Vec3f(1.3, 0.1, 1.95))

beam_positions = [(-1,0,2), (1,0,2), (-1,0,-2), (1,0,-2)]
for i, pos in enumerate(beam_positions):
    leg_path = f"/Rack/Leg_{i+1:02d}"
    leg_prim = UsdGeom.Xform.Define(stage, leg_path).GetPrim()
    leg_prim.GetReferences().AddInternalReference("/Rack/Prototypes/BeamHandle")
    leg_prim.SetInstanceable(True)
    UsdGeom.XformCommonAPI(leg_prim).SetTranslate(Gf.Vec3d(pos))

shelf_positions = [(0, -0.2, 0), (0, 1.8, 0)]
for i, pos in enumerate(shelf_positions):
    shelf_path = f"/Rack/Shelf_{i+1:02d}"
    shelf_xform = UsdGeom.Xform.Define(stage, shelf_path)
    shelf_prim = shelf_xform.GetPrim()
    shelf_prim.GetReferences().AddInternalReference("/Rack/Prototypes/ShelfHandle")
    shelf_prim.SetInstanceable(True)
    # UsdGeom.XformCommonAPI(shelf_prim).SetTranslate(Gf.Vec3d(pos))
    shelf_xform.AddTranslateOp()
    
#Vset size
vset_size = world_xform.GetPrim().GetVariantSets().AddVariantSet("size")
vset_size.AddVariant("small")
vset_size.AddVariant("tall")
vset_size.SetVariantSelection("small")
with vset_size.GetVariantEditContext():
    beam_over_prim = stage.OverridePrim("/Rack/Prototypes/BeamHandle/Beam")
    beam_geom = UsdGeom.Cube(beam_over_prim)
    beam_geom.GetScaleOp().Set(Gf.Vec3f(0.1, 2.0, 0.1))

    shelf_01 = UsdGeom.Xformable(stage.GetPrimAtPath("/Rack/Shelf_01"))
    shelf_01.GetTranslateOp().Set(Gf.Vec3d(0, -0.2, 0))
    
    shelf_02 = UsdGeom.Xformable(stage.GetPrimAtPath("/Rack/Shelf_02"))
    shelf_02.GetTranslateOp().Set(Gf.Vec3d(0, 1.8, 0))

vset_size.SetVariantSelection("tall")
with vset_size.GetVariantEditContext():
    beam_over_prim = stage.OverridePrim("/Rack/Prototypes/BeamHandle/Beam")
    beam_geom = UsdGeom.Cube(beam_over_prim)
    beam_geom.GetScaleOp().Set(Gf.Vec3f(0.1, 5.0, 0.1))

    shelf_02 = UsdGeom.Xformable(stage.GetPrimAtPath("/Rack/Shelf_01"))
    shelf_02.GetTranslateOp().Set(Gf.Vec3d(0, -0.2, 0))
    
    shelf_02 = UsdGeom.Xformable(stage.GetPrimAtPath("/Rack/Shelf_02"))
    shelf_02.GetTranslateOp().Set(Gf.Vec3d(0, 4.8, 0))

vset_size.SetVariantSelection("small")

# Vset material
vset_mat = world_xform.GetPrim().GetVariantSets().AddVariantSet("material")
vset_mat.AddVariant("steel")
vset_mat.AddVariant("wood")
vset_mat.SetVariantSelection("steel")
with vset_mat.GetVariantEditContext():
    beam_over_prim = stage.OverridePrim("/Rack/Prototypes/BeamHandle/Beam")
    beam_geom = UsdGeom.Cube(beam_over_prim)
    beam_geom.GetDisplayColorAttr().Set([(0.4,0.45,0.45)])

vset_mat.SetVariantSelection("wood")
with vset_mat.GetVariantEditContext():
    beam_over_prim = stage.OverridePrim("/Rack/Prototypes/BeamHandle/Beam")
    beam_geom = UsdGeom.Cube(beam_over_prim)
    beam_geom.GetDisplayColorAttr().Set([(0.7,0.25,0.05)])

vset_mat.SetVariantSelection("steel")

stage.Save()