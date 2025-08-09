def generate_prompt(text):
    return f"""You are a layout parsing AI. Based on the following UI guideline, extract and return a structured JSON object containing layout details for each text element.
### Your output JSON must follow this structure:
  "widget_name": "string",             # e.g., banner, carousel
  "device_type": "string",             # e.g., mobile, iPhone, desktop
  "overall_width": number,
  "overall_height": number,
  "elements": obj
    "element_name": obj
      "x_left": number,                # If position is from left, use as-is
      "x_right": number,               # If position is from right, use as-is
      "y_top": number,                 # If position is from top, use as-is
      "y_bottom": number,              # If position is from bottom, use as-is
      "font_size": number,
      "font_family": "string",         # Only one value, not an array
      "alignment": "string",           # e.g., left, center, right, top, bottom
      "max_lines": number

### Parsing Rules:
- Extract `widget_name`, `device_type` from the guideline.
- the overall_height and overall_width will be mentioned has width and height of the widget
- For each text element (e.g., title, subtitle, description):
  - Assign position values depending on how they are specified in the guideline:
    - If position is specified **from left**, store it in `x_left`.
    - If from **right**, store it in `x_right`.
    - If from **top**, store it in `y_top`.
    - If from **bottom**, store it in `y_bottom`.
  - Do **not** calculate actual x or y coordinates. Just assign the raw distances to the respective `x_` or `y_` fields.
- Only one `font_family` value per element.
- Include `font_size`, `alignment`, and `max_lines` per element.
- Skip any undefined or optional elements that are not mentioned in the guideline.

Return **only the final JSON output** please check if it is proper json. Do not include any explanation or extra text.

guildeline text 
{text}"""
