import os
import re

def getBgName(backgroundPath):
    bgName = os.path.splitext(backgroundPath)[0]
    patterns = [r"_?simple", r"arccreate_+", r" \(1\)", r"\s+"]
    replace = ["", "", "", "_"]
    for pattern, replacement in zip(patterns, replace):
        bgName = re.sub(pattern, replacement, bgName)
    bg = bgName.lower()
    bg_inverse = (
        bg.replace("light", "conflict")
        if "light" in bg
        else bg.replace("conflict", "light")
        if "conflict" in bg
        else ""
    )
    if bg == "yugamu":
        bg_inverse = "rei"
    elif bg == "rei":
        bg_inverse = "yugamu"
    elif bg == "zettai":
        bg_inverse = "zettai_light"
    elif bg == "zettai_light":
        bg_inverse = "zettai"
    elif bg == "base_colorless":
       bgName = "epilogue"
    return bgName, bg_inverse
