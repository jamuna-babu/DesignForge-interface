def generate_prompt(text):
    print(text)
    return f"""
You are a JSON extraction and transformation engine.  
You will read parsed PDF text and return a SINGLE valid JSON object in the exact schema below.  
Do NOT output explanations, comments, or any text outside the JSON.  

INPUT: 
{text}



Position rules:
1. Top or Bottom values always map to `y`. Store them as "<number>px from top" or "<number>px from bottom" exactly as in the PDF.
2. Left or Right values always map to `x`. Store them as "<number>px from left" or "<number>px from right" exactly as in the PDF.
3. If a position is relative (e.g., "300px above title"), store it exactly as in the PDF in the correct axis (`y` for above/below, `x` for left/right of another element).
4. Do NOT calculate numeric coordinates — keep the exact raw strings from the PDF.
5. Preserve formatting, spacing, and units exactly.

Additional typography rules:  
- Extract font family, style, size, max_lines, min_lines, and alignment exactly as in the PDF.  
- Preserve capitalization, punctuation, and spacing exactly as in the PDF.

replace_value_of_widget_in_pdf fill this value from widget: ______ value
replace_value_of_devicetype_in_pdf

THIS IS SAMPLE OUTPUT :
{{
  "replace_value_of_widget_in_pdf": {{
    "replace_value_of_devicetype_in_pdf": {{
      "text_requirements": {{
        "subtitle_is_optional": true,
        "description_is_optional": true,
        "combined_max_lines": 4
      }},
      "text_styles": {{
        "title": {{
          "font_family": "Free sans",
          "font_style": "Bold",
          "font_size": 44,
          "max_lines": 3,
          "min_lines": 1,
          "alignment": "Bottom&Left",
          "text": "title",
          "positions": {{ "y": "264px from bottom", "x": "16px from left" }}
        }},
        "subtitle": {{
          "font_family": "Roboto",
          "font_style": "(subtitle)Roboto, Medium, Size 16",
          "font_size": 16,
          "max_lines": 1,
          "min_lines": 0,
          "alignment": "Bottom&Left",
          "text": "subtitle",
          "positions": {{ "y": "726px from top", "x": "16px from left" }}
        }},
        "description": {{
          "font_family": "Roboto",
          "font_style": "Roboto, Regular, Size 18",
          "font_size": 18,
          "max_lines": 2,
          "min_lines": 0,
          "alignment": "Top&Left",
          "text": "description",
          "positions": {{ "y": "726px from top", "x": "16px from left" }}
        }}
      }},
      "image_width": <int>,
      "image_height": <int>
    }}
  }}
}}
OUTPUT ONLY JSON NO ADDITONAL, ALL KEYS MUST BE FILLED WITH VALUES.
 YOU CAN DO IT ACCURATELY FOLLOW THE POSITION RULES TO FILL positions. 
 For text keys use their key name like title or subtitle or description
"""

