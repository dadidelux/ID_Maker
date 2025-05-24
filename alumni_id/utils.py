from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
from django.conf import settings

def generate_id_card(alumni):
    """
    Generate an ID card for an alumni using PIL
    Returns a BytesIO object containing the generated ID card image
    """
    # Get the background image
    background = Image.open(alumni.id_background.image.path).convert("RGBA")
    
    # Configuration
    FONT_PATH = os.path.join(settings.STATIC_ROOT, 'fonts', 'arial.ttf')
    FONT_SIZE = 22
    
    # Photo position and size (from your idmaker.py)
    PHOTO_POSITION = (200, 220)  # 200px from left, 220px from top
    PHOTO_SIZE = (400, 540)      # Width: 400px, Height: 540px
    
    # Text positions (from your idmaker.py)
    TEXT_POSITIONS = {
        "name": (700, 180),
        "id": (700, 220),
        "course": (700, 260),
        "year": (700, 300),
        "validity": (700, 340)
    }

    # Load and resize alumni photo
    photo = Image.open(alumni.photo.path)
    photo = photo.resize(PHOTO_SIZE, Image.Resampling.LANCZOS)
    
    # Create a new image with the background
    id_card = background.copy()
    
    # Paste the photo
    id_card.paste(photo, PHOTO_POSITION)
    
    # Initialize drawing context
    draw = ImageDraw.Draw(id_card)
    
    # Load font
    try:
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()

    # Draw text
    full_name = f"{alumni.first_name} {alumni.last_name}"
    draw.text(TEXT_POSITIONS["name"], f"Name: {full_name}", fill="black", font=font)
    draw.text(TEXT_POSITIONS["id"], f"ID: {alumni.school_id}", fill="black", font=font)
    draw.text(TEXT_POSITIONS["year"], f"Year Graduated: {alumni.year_graduated}", fill="black", font=font)
    if alumni.company:
        draw.text(TEXT_POSITIONS["course"], f"Company: {alumni.company}", fill="black", font=font)
    draw.text(TEXT_POSITIONS["validity"], 
             f"Valid until: {alumni.validity_end.strftime('%B %d, %Y')}", 
             fill="black", font=font)

    # Save to BytesIO
    output = BytesIO()
    id_card.save(output, format='PNG')
    output.seek(0)
    
    return output 