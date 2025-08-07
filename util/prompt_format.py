def generate_prompt(text):
  return f"""You are a layout engine. Convert the following design instructions into structured JSON layout data. 
                    Please ensure the JSON format is clean and properly structured. Do not include any markdown or code block markers (```). 

Please ensure to send only IN JSON format is clean , properly structured, and calculated according to the following rules:

### 1. **Text Element Y-Position Calculation**:
   - **Font Size**: The font size of each text element (e.g., title, subtitle) will determine the height of the text box.
   - **Line Height**: The line height depends on the font family and size:
     - For "Free Sans": Line height is 1.33 if the font size is less than 40, otherwise 1.40.
     - For "Roboto": Line height is always 1.33, regardless of font size.
   - **Text Box Height**: Text box height is calculated as the font size multiplied by the line height, and then multiplied by the number of lines (max lines or based on the content).
   - **Y Position Calculation**:
     - If the `y` is provided from the bottom, calculate the position as follows:
       ```
       y_from_bottom = Total Height - y_position - (font_size * line_height * number_of_lines)
       ```
     - If the `y` is provided from the top, use the given `y_position` directly.

### 2. **Text Element Layout**:
   - For each element like `text-segment` which is title or subtitle or description or cta, and their respective `font`, `size`, `position`, `alignment`, `color`, calculate the position and size based on the above rules.
   - Ensure that the title and subtitle are positioned accordingly. The `y` position for the subtitle is calculated relative to the title if no explicit `y` is given for the subtitle.
   - For a given text element, the calculated height (based on font size and line height) should be added or subtracted from the `y` to determine the final position.
### 3. Include key named text inside it and name it just like it header of it like title for title 
# 4. calculate the positions correctly tell how you calculated the positions for

Here are the design instructions:

{text}

Output only the following JSON keys don't include any other name just obj including all this: 'title', 'subtitle', 'font', 'size', 'position', 'alignment', 'max_lines', 'color'. Ensure the 'y' position is calculated based on the above rules. No other text, code blocks, or markdown should be included in the response.
    The JSON should be structured exactly as follows:

    
        "widget": obj
            "name": "Widget 1",
            "text_styles": 
                "subtitle": obj
                    "font_family": "Roboto",
                    "font_style": "Medium",
                    "font_size": 16,
                    "max_lines": 1,
                    "min_lines": 0,
                    "alignment": "Bottom&Left"
                    "text": "subtitle",
                    "positions":obj
                       "x": "//calculate it from image"
                       "y": "title+8+ line height of title"
                    
                ,
                "title": obj
                    "font_family": "Free sans",
                    "font_style": "Bold",
                    "font_size": 44,
                    "max_lines": 3,
                    "min_lines": 1,
                    "alignment": "Bottom&Left"
                    "text":"title"
                    "positions":obj
                       "x": "//calculate it from image"
                       "y": "//based on from top or bottom calculate this Refer this Text Element Y-Position Calculation"
                    
                ,
                "description": obj
                    "font_family": "Roboto",
                    "font_style": "Regular",
                    "font_size": 18,
                    "max_lines": 3,
                    "min_lines": 0,
                    "alignment": "Top&Left"
                    "text": "description"
                    "positions":
                       "x": "//calculate it from image"
                       "y": "//based on from top or bottom calculate this"
                    
                
            
            "text_requirements": obj
                "subtitle_is_optional": "true",
                "description_is_optional": "true",
                "combined_max_lines": 4
            ,
           
        
    

    Ensure the 'y' position is calculated based on the above rules.
"""
