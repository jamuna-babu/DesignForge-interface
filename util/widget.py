from flask import abort

class WidgetLayout:
    def __init__(self, attributes):
        self.widget_name = attributes.get('widget_name') 
        self.device_type = attributes.get('device_type') 
        self.overall_width = attributes.get('overall_width')
        self.overall_height = attributes.get('overall_height')
        self.elements = attributes.get('elements')

    def construct_complete_layout(self):
        output_data = {
            self.widget_name: {
                self.device_type: {
                    "text_styles": {},
                    "width": self.overall_width,
                    "height": self.overall_height
                },
                "overall_width": self.overall_width,
                "overall_height": self.overall_height
            },
        }
        
        # Process each element
        for element_name, element in self.elements.items():
            output_data[self.widget_name][self.device_type]["text_styles"][element_name] = \
                    self.process_element(element_name, element)

        return output_data

    def process_element(self, element_name, element):
        x = None
        y = None
        
        # Calculate x
        if "x_left" in element and element["x_left"] is not None:
            x = element["x_left"]
        elif "x_right" in element and element["x_right"] is not None:
            x = self.overall_width - element["x_right"]
        else:
            x = None  # If both are missing or null
        
        # Calculate y
        if "y_top" in element and element["y_top"] is not None:
            y = element["y_top"]
        elif "y_bottom" in element and element["y_bottom"] is not None:
            y = self.overall_height - element["y_bottom"]
        else:
            y = None 

        # validate
        if x is None or y is None:
            abort(415, "Guidelines is not as per set standards!")

        # Prepare text style entry
        return {
            "font_family": element["font_family"].split()[0],  # First word only
            "font_size": element["font_size"],
            "max_lines": element.get("max_lines", None),
            "min_lines": element.get("min_lines", None),
            "alignment": element["alignment"],
            "text": element_name,
            "positions": {
                "x": x,
                "y": y
            }
        }
