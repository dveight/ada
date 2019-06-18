"""global static values used in multiple modules"""

from collections import namedtuple

ALIAS_STRING = "alias({knob}, {alias}, {default})"
INPUT_STRING = "input({knob}, {index}, {location}, {start}, {end})"
OUTPUT_STRING = "output({knob}, {index}, {location})"

KnobAlias = namedtuple("Alias", "knob alias default_value")
KnobInput = namedtuple("Input", "knob index default_value start end")
KnobOutput = namedtuple("Output", "knob index default_value")

ADA_KNOBS = [
    "knobs_to_bake_knobs",
    "knobs_to_knobs_to_bake",
    "knobs_to_set_knobs",
    "knobs_to_knobs_to_set",
    "execute_knobs",
    "knobs_to_execute",
    "execute_code",
    "code_to_execute",
    "queue_order",
    "do_not_knobs_to_bake",
    "knobs_to_serialise",
    "ada",
]

IGNORE_KNOBS = [
    "help",
    "onCreate",
    "onDestroy",
    "knobChanged",
    "updateUI",
    "autolabel",
    "panel",
    "tile_color",
    "gl_color",
    "label",
    "note_font",
    "note_font_size",
    "note_font_color",
    "selected",
    "xpos",
    "ypos",
    "icon",
    "indicators",
    "hide_input",
    "cached",
    "disable",
    "dope_sheet",
    "bookmark",
    "postage_stamp",
    "postage_stamp_frame",
    "useLifetime",
    "name",
    "lock_connections",
    "mapsize",
    "window",
    "gizmo_file",
]

IGNORE_KNOBS.extend(ADA_KNOBS)


INPUT_NODES = {"Read": ["file"], "Camera": ["file"], "ReadGeo": ["file"]}

OUTPUT_NODES = {"Write": ["file"], "DeepWrite": ["file"], "WriteGeo": ["file"]}

ADA_KNOB_CHANGED = (
    "__import__('ada.nuke.node', fromlist=['ada_knob_changed']).ada_knob_changed()"
)

KNOB_TO_EXECUTION_TYPE = {
    "IArray_Knob": "knobs_to_bake",
    "PyScript_Knob": "knobs_to_execute",
    "WH_Knob": "knobs_to_bake",
    "PythonCustomKnob": "knobs_to_set",
    "Color_Knob": "knobs_to_bake",
    "AColor_Knob": "knobs_to_bake",
    "Channel_Knob": "knobs_to_set",
    "Scale_Knob": "knobs_to_bake",
    "Password_Knob": "knobs_to_bake",
    "FreeType_Knob": "knobs_to_set",
    "Transform2d_Knob": "knobs_to_bake",
    "EvalString_Knob": "knobs_to_bake",
    "Unsigned_Knob": "knobs_to_bake",
    "Box3_Knob": "knobs_to_bake",
    "OneView_Knob, , []": "knobs_to_set",
    "Array_Knob": "knobs_to_bake",
    "Help_Knob": "knobs_to_execute",
    "CascadingEnumeration_Knob": "knobs_to_set",
    "SceneView_Knob": "knobs_to_set",
    "String_Knob": "knobs_to_set",
    "XY_Knob": "knobs_to_bake",
    "Multiline_Eval_String_Knob": "knobs_to_bake",
    "File_Knob": "knobs_to_set",
    "Script_Knob": "knobs_to_set",
    "XYZ_Knob": "knobs_to_bake",
    "Keyer_Knob": "knobs_to_bake",
    "ColorChip_Knob": "knobs_to_bake",
    "Range_Knob": "knobs_to_bake",
    "PyCustom_Knob": "knobs_to_set",
    "Font_Knob": "knobs_to_set",
    "UV_Knob": "knobs_to_bake",
    "Text_Knob": "knobs_to_set",
    "Enumeration_Knob": "knobs_to_set",
    "Radio_Knob": "knobs_to_set",
    "ChannelMask_Knob": "knobs_to_set",
    "Format_Knob": "knobs_to_set",
    "Boolean_Knob": "knobs_to_bake",
    "EditableEnumeration_Knob": "knobs_to_set",
    "Double_Knob": "knobs_to_bake",
    "MultiView_Knob": "knobs_to_set",
    "BBox_Knob": "knobs_to_bake",
    "Int_Knob": "knobs_to_bake",
    "ViewView_Knob": "knobs_to_execute",
    "Pulldown_Knob": "knobs_to_set",
}
