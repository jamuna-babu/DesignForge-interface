import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image, ImageFont, ImageDraw
from paddleocr import PaddleOCR
from sklearn.metrics.pairwise import cosine_similarity
import cv2
import numpy as np
import json

# ===== CONFIG =====
REF_FONTS_DIR = "fonts_ref"
IMG_PATH = "/home/d2c-jamuna-babu/Documents/DesignForgeInterface/DesignForge-interface/check3.png"
OUTPUT_PATH= '/home/d2c-jamuna-babu/Documents/DesignForgeInterface/DesignForge-interface/output.png'
GROUP_Y_THRESHOLD = 10
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ===== MODEL LOADING =====
model = models.resnet18(pretrained=True)
model = nn.Sequential(*list(model.children())[:-1])
model.eval().to(DEVICE)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def get_embedding(img):
    img_t = transform(img).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        emb = model(img_t)
    return emb.squeeze().cpu().numpy().reshape(1, -1)

def calculate_point_size_from_pixels(ttf_path, text, pixel_height):
    trial_size = 10
    trial_font = ImageFont.truetype(ttf_path, trial_size)
    ascent, descent = trial_font.getmetrics()
    trial_pixel_height = ascent + descent
    estimated_size = (pixel_height / trial_pixel_height) * trial_size
    return round(estimated_size, 2)

# ===== LOAD REFERENCE FONT EMBEDDINGS =====
ref_embeddings = {}
for fname in os.listdir(REF_FONTS_DIR):
    if fname.lower().endswith(".png"):
        font_name = os.path.splitext(fname)[0]
        img = Image.open(os.path.join(REF_FONTS_DIR, fname)).convert("RGB")
        ref_embeddings[font_name] = get_embedding(img)
    elif fname.lower().endswith(".ttf"):
        font_name = os.path.splitext(fname)[0]
        font = ImageFont.truetype(os.path.join(REF_FONTS_DIR, fname), 48)
        img = Image.new("RGB", (300, 100), "white")
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "Sample", font=font, fill="black")
        ref_embeddings[font_name] = get_embedding(img)

if not ref_embeddings:
    print("No reference fonts found in", REF_FONTS_DIR)
    exit()

# ===== OCR DETECTION =====
ocr = PaddleOCR(use_angle_cls=True, lang='en')
results = ocr.ocr(IMG_PATH, cls=True)

img = Image.open(IMG_PATH).convert("RGB")
elements = []

for line in results[0]:
    box, (text, conf) = line
    x_coords = [p[0] for p in box]
    y_coords = [p[1] for p in box]
    xmin, xmax = int(min(x_coords)), int(max(x_coords))
    ymin, ymax = int(min(y_coords)), int(max(y_coords))

    crop = img.crop((xmin, ymin, xmax, ymax))
    emb = get_embedding(crop)

    similarities = {font_name: cosine_similarity(emb, ref_emb)[0][0]
                    for font_name, ref_emb in ref_embeddings.items()}
    best_match = max(similarities, key=similarities.get) if similarities else None

    font_size_est = ymax - ymin
    ttf_path = os.path.join(REF_FONTS_DIR, best_match + ".ttf") if best_match else None
    if ttf_path and os.path.exists(ttf_path):
        font_size_est = calculate_point_size_from_pixels(ttf_path, text, ymax - ymin)

    elements.append({
        "text": text,
        "conf": conf,
        "y_mid": (ymin + ymax) / 2,
        "font": best_match,
        "font_size": font_size_est,
        "box": box  # Store original OCR polygon for bounding box calculation
    })

# ===== SORT BOTTOM → TOP =====
elements.sort(key=lambda e: e["y_mid"], reverse=True)

# ===== GROUP BY Y-POS & FONT =====
groups = []
current_group = [elements[0]]

for elem in elements[1:]:
    last_elem = current_group[-1]
    if abs(elem["y_mid"] - last_elem["y_mid"]) <= GROUP_Y_THRESHOLD and elem["font"] == last_elem["font"]:
        current_group.append(elem)
    else:
        groups.append(current_group)
        current_group = [elem]
groups.append(current_group)

# ===== MERGE ONLY CONSECUTIVE GROUPS WITH SAME FONT =====
merged_groups = []
for group in groups:
    if merged_groups and merged_groups[-1][0]['font'] == group[0]['font']:
        merged_groups[-1].extend(group)
    else:
        merged_groups.append(group)

# ===== RULES =====
RULES = {
    "order": [ "Description", "Title", "Subtitle"],
    "fonts": {
        "Description": {"family": ["Roboto"], "style": ["Lighter", "Thin", "Regular"], "size": 18, "color": ["black", "white"]},
        "Title": {"family": ["FreeSans"], "style": ["Bold"], "size": 44, "color": ["black", "white"]},
        "Subtitle": {"family": ["Roboto"], "style": ["Normal"], "size": 16, "color": ["black", "white"]}
    },
    "positions": {
        "CTA": {"y_from_bottom": 40, "alignment": "center"},
        "Description": {"y_from_top": 358},
        "Title": {"y_from_bottom": 185},
        "Subtitle": {"relative_to": "Title", "position": "above"}
    },
    "lines": {
        "CTA": {"max_line": 1, "min_line": 1},
        "Description": {"max_line": 3, "min_line": 0},
        "Title": {"max_line": 3, "min_line": 1},
        "Subtitle": {"max_line": 1, "min_line": 0}
    }
}

# ===== MATCH GROUPS TO RULES =====
def map_groups_to_rules(groups, RULES):
    remaining_rules = RULES["fonts"].copy()
    mapped = []

    for group in groups:
        if "-" in group[0]["font"]:
            group_family, group_style = group[0]["font"].split("-", 1)
        else:
            group_family, group_style = group[0]["font"], ""
        group_family = group_family.strip().lower()
        group_style = group_style.strip().lower()
        line_count = len(group)

        matched_type = None
        for element_type, font_rule in list(remaining_rules.items()):
            rule_families = [f.lower() for f in font_rule["family"]]
            rule_styles = [s.lower() for s in font_rule["style"]]
            min_line = RULES["lines"][element_type]["min_line"]
            max_line = RULES["lines"][element_type]["max_line"]
            print(group_family in rule_families , group_style in rule_styles , min_line <= line_count <= max_line)

            if group_family in rule_families and group_style in rule_styles and min_line <= line_count <= max_line:
                matched_type = element_type
                mapped.append({"group": group, "type": element_type})
                del remaining_rules[element_type]
                break

        if not matched_type:
            mapped.append({"group": group, "type": None})

    missing_elements = list(remaining_rules.keys())
    return mapped, missing_elements

# ===== GET ONE BOUNDING BOX PER GROUP =====
def get_group_bounding_boxes(mapped_groups):
    group_boxes = []
    for m in mapped_groups:
        group = m["group"]
        xmins, ymins, xmaxs, ymaxs = [], [], [], []
        for elem in group:
            x_coords = [p[0] for p in elem["box"]]
            y_coords = [p[1] for p in elem["box"]]
            xmins.append(min(x_coords))
            xmaxs.append(max(x_coords))
            ymins.append(min(y_coords))
            ymaxs.append(max(y_coords))
        group_boxes.append({
            "font": group[0]["font"],
            "type": m["type"],
            "bbox": [min(xmins), min(ymins), max(xmaxs), max(ymaxs)]
        })
    return group_boxes

# ===== RUN MAPPING & BOX CREATION =====
mapped_groups, missing = map_groups_to_rules(merged_groups, RULES)
print(merged_groups,"me")
bounding_boxes = get_group_bounding_boxes(mapped_groups)

# ===== PRINT FINAL RESULT =====
for box in bounding_boxes:
    print(box)

print("\nMissing elements:", missing)

# ===== OPTIONAL: DRAW ON IMAGE =====
draw = ImageDraw.Draw(img)
for box in bounding_boxes:
    x1, y1, x2, y2 = box["bbox"]
    draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
    draw.text((x1, y1-10), f"{box['type']}", fill="red")
img.show()
img.save(OUTPUT_PATH)

cv_img = cv2.imread(IMG_PATH)
mask = np.zeros(cv_img.shape[:2], dtype=np.uint8)

# Draw mask over text areas
for box in bounding_boxes:
    x1, y1, x2, y2 = map(int, box["bbox"])
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

# Inpaint to remove text naturally
inpainted_img = cv2.inpaint(cv_img, mask, 3, cv2.INPAINT_TELEA)

# Save cleaned background
CLEAN_BG_PATH = "clean_background.png"
cv2.imwrite(CLEAN_BG_PATH, inpainted_img)
print(f"Clean background saved at {CLEAN_BG_PATH}")


fabric_data = []
for box in bounding_boxes:
    x1, y1, x2, y2 = box["bbox"]
    text_item = next((e for g in merged_groups for e in g if e["font"] == box["font"]), None)
    print(text_item,"text items")
    family, style = text_item["font"].split("-", 1)
    fabric_data.append({
        "left": x1,
        "top": y1,
        "width": x2 - x1,
        "height": y2 - y1,
        "text": text_item["text"] if text_item else "",
        "fontFamily": family,
        "fontStyle": style,
        "fontSize": text_item["font_size"] if text_item else 16
    })

with open("fabric_text_data.json", "w") as f:
    json.dump(fabric_data, f, indent=2)