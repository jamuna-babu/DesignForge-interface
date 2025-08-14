def generate_prompt(text):
    print(text)
    return f"""
You are a layout parsing AI.  
From the following UI guideline text, extract and return ONLY a valid JSON object.  
No explanations, no comments, no extra text — just proper JSON.  

### Output JSON Format:
{{
  "<widget_name>": {{
    "<device_type>": {{
      "text_requirements": {{
        "subtitle_is_optional": <true|false>,
        "description_is_optional": <true|false>,
        "combined_max_lines": <int>
      }},
      "text_styles": {{
        "<element_name>": {{
          "font_family": "<string>",
          "font_style": "<string>",
          "font_size": <int>,
          "max_lines": <int>,
          "min_lines": <int>,
          "alignment": "<string>",
          "text": "<element_name>",
          "positions": {{
            "x": "<string>",
            "y": "<string>"
          }}
        }}
      }},
      "image_width": <int>,
      "image_height": <int>
    }}
  }}
}}

### Parsing Rules:
1. **widget_name** → Extract from "Widget: <name>" in the guideline.
2. **device_type** → Extract from "Device type: <type>".
3. **image_width** & **image_height** → Extract from "Width" and "Height".
4. **positions rule**: -> you can refer Location key  
(description)It should be located 16px above the title
and 16px from left - EXAMPLE 
    here y: "16px above the title" x:"16px from left"
   - If a position is mentioned **from top** or **from bottom**, store it in `"y"` it should be either "intpx from top" or "intpx from bottom" only one from this is needed  as per context give what you read.  
   - If a position is mentioned **from left** or **from right**, store it in `"x"` it should be either "intpx from left" or "intpx from right" not both.  
   - Keep the exact text (e.g., `"16px from left"`), do NOT calculate coordinates.
5. For each element (title, subtitle, description):
   - Include font_family, font_style, font_size, alignment, min_lines, max_lines, and text.
6. For title text: "title" similarly each element you find.
6. Skip any element not mentioned in the guideline.
7. Ensure JSON is valid — no trailing commas, no comments.


### Guideline Text:
{text}
"""