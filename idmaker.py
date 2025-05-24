import csv
from PIL import Image, ImageDraw, ImageFont
import os

# Config
TEMPLATE_PATH = "id_template.png"
FONT_PATH = "fonts/arial.ttf"
OUTPUT_DIR = "output_ids"
PHOTO_DIR = "photos"
FONT_SIZE = 22
# -> left (x,y) down V -> (a,y)
PHOTO_POSITION = (200, 200+20)
#WxH
PHOTO_SIZE = (400, 520+20)

TEXT_POSITIONS = {
    "name": (700, 180),
    "id": (700, 220),
    "course": (700, 260),
    "year": (700, 300)
}

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load font
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# Load student data from CSV
with open("student_data.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        student_id = row["student_id"]
        name = row["name"]
        course = row["course"]
        year = row["year"]
        photo_filename = row["photo_filename"]

        # Open background template
        id_image = Image.open(TEMPLATE_PATH).convert("RGBA")
        draw = ImageDraw.Draw(id_image)

        # Paste photo
        photo_path = os.path.join(PHOTO_DIR, photo_filename)
        if os.path.exists(photo_path):
            photo = Image.open(photo_path).resize(PHOTO_SIZE).convert("RGBA")
            id_image.paste(photo, PHOTO_POSITION)
        else:
            print(f"Warning: Photo not found for {student_id}, skipping photo.")

        # Draw text
        draw.text(TEXT_POSITIONS["name"], f"Name: {name}", fill="black", font=font)
        draw.text(TEXT_POSITIONS["id"], f"ID: {student_id}", fill="black", font=font)
        draw.text(TEXT_POSITIONS["course"], f"Course: {course}", fill="black", font=font)
        draw.text(TEXT_POSITIONS["year"], f"Year: {year}", fill="black", font=font)

        # Save ID image
        output_path = os.path.join(OUTPUT_DIR, f"{student_id}_id.png")
        id_image.save(output_path)
        print(f"Generated ID for {name}: {output_path}")
