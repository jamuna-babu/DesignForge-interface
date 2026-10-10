import json
import re
from flask import abort

def extract_json_from_code_block(data):
    json_data = data
    # Extract only the JSON
    matches = re.match(r"```(json)*([^`]+)```", data)
    if matches and len(matches.groups()) > 0:
        json_data = matches.group(2)
    return json.loads(json_data)

def get_key_from_singleton_dict(singleton_dict):
    keys = list(singleton_dict.keys())
    return keys[0]

def calculate_position_from_json(data):
        print("helllooo inside this")
        def get_line_height(font_family, font_size):
            font_family = font_family.lower()
            print(font_family,"family")
            if "free sans" in font_family:
                return 1.2 if font_size < 40 else 1.33
            elif "roboto" in font_family:
                return 1.33
            else:
                return 1.33  # Default

        def parse_position(pos_str, axis, image_width, image_height, refs, element_data):
            pos_str = pos_str.strip().lower()
            print(pos_str,axis)

            font_size = element_data["font_size"]
            print(font_size,"font size")
            line_height = get_line_height(element_data["font_family"], font_size)
            print(line_height,"line height after this")
            num_lines = 1
            text_box_height = font_size * line_height * num_lines
            print(text_box_height,"height,",font_size,line_height,num_lines,"lines")

            if axis == "x":
                if "from left" in pos_str:
                    print("from left called")
                    return int(pos_str.split("px")[0])
                elif "from right" in pos_str:
                    return image_width - int(pos_str.split("px")[0])
            
            elif axis == "y":
                if "from the top" in pos_str or "from top" in pos_str:
                    print("from te top called")
                    return int(pos_str.split("px")[0])
                elif "from the bottom" in pos_str or "from bottom" in pos_str:
                    print("from the bottom called")
                    # y_from_bottom formula
                    y_px = int(pos_str.split("px")[0])
                    print("honey im doing",y_px,text_box_height)
                    print(image_height - y_px , text_box_height,"after minus")
                    return image_height - y_px - text_box_height
                elif "above" in pos_str:
                    print("from the above called")
                    value = int(pos_str.split("px")[0])
                    print(value,"value")
                    ref_element = pos_str.split("above the")[1].strip()
                    print(ref_element,"ref element value",refs,"refs",text_box_height,"text_box_height")
                    if ref_element in refs:
                        return refs[ref_element] - value - text_box_height
                    else:
                        raise ValueError(f"Reference '{ref_element}' not found.")
                        
            raise ValueError(f"Invalid position string: {pos_str}")

        widget_name = list(data.keys())[0]
        device_type = list(data[widget_name].keys())[0]
        image_width = data[widget_name][device_type]["image_width"]
        image_height = data[widget_name][device_type]["image_height"]
        text_styles = data[widget_name][device_type]["text_styles"]

        refs = {}
        unresolved = set(text_styles.keys())
        print(unresolved,"unresolved cases")

        while unresolved:
            progress = False
            for key in list(unresolved):

                try:
                    element_data = text_styles[key]
                    raw_x = element_data["positions"]["x"]
                    raw_y = element_data["positions"]["y"]

                    numeric_x = parse_position(raw_x, "x", image_width, image_height, refs, element_data)
                    numeric_y = parse_position(raw_y, "y", image_width, image_height, refs, element_data)

                    text_styles[key]["positions"]["x"] = round(numeric_x * 20) / 20
                    text_styles[key]["positions"]["y"] = round(numeric_y * 20) / 20

                    refs[key] = numeric_y
                    unresolved.remove(key)
                    progress = True
                except ValueError:
                    continue

            if not progress:
                abort(415, "Guidelines is not as per set standards Positions are not!")


        return data

