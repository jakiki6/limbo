from pynbt import *

dimension = {
    "name": TAG_String("limbo:the"),
    "id": TAG_Int(0),
    "element": TAG_Compound({
        "piglin_safe": TAG_Byte(1),
        "natural": TAG_Byte(1),
        "ambient_light": TAG_Float(1.0),
        "infiniburn": TAG_String(""),
        "respawn_anchor_works": TAG_Byte(1),
        "has_skylight": TAG_Byte(1),
        "bed_works": TAG_Byte(1),
        "effects": TAG_String("minecraft:the_end"),
        "has_raids": TAG_Byte(1),
        "min_y": TAG_Int(0),
        "height": TAG_Int(256),
        "logical_height": TAG_Int(256),
        "coordinate_scale": TAG_Float(1.0),
        "ultrawarm": TAG_Byte(1),
        "has_ceiling": TAG_Byte(0)
    })
}

biome = {
    "name": TAG_String("limbo:the_biome"),
    "id": TAG_Int(0),
    "element": TAG_Compound({
        "precipitation": TAG_String("none"),
        "depth": TAG_Float(0.0),
        "temperature": TAG_Float(1.5),
        "scale": TAG_Float(0.0),
        "downfall": TAG_Float(0.0),
        "category": TAG_String("none"),
        "effects": TAG_Compound({
            "sky_color": TAG_Int(0xfb03ff),
            "water_fog_color": TAG_Int(0xfb03ff),
            "fog_color": TAG_Int(0xfb03ff),
            "water_color": TAG_Int(0xfb03ff),
        }),
    })
}

dimension_codec = {
    "minecraft:dimension_type": TAG_Compound({
        "type": TAG_String("minecraft:dimension_type"),
        "value": TAG_List(TAG_Compound, [
            TAG_Compound(dimension)
        ])
    }),
    "minecraft:worldgen/biome": TAG_Compound({
        "type": TAG_String("minecraft:worldgen/biome"),
        "value": TAG_List(TAG_Compound, [
            TAG_Compound(biome)
        ])
    })
}

#print(NBTFile(value=dimension_codec).pretty())