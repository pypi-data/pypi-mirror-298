import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from pfandbon.barcode_utils import generate_barcode

class PfandbonGenerator:
    def __init__(self, config):
        self.config = config
        self.output_folder = config.get("output_folder", "outputs")
        self.font_path = config.get("font_path", "arial.ttf")
        self.font_size = config.get("font_size", 24)
        self.initialize_folders()

    def initialize_folders(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def create_receipt(self, total_amount):
        barcode_text = generate_barcode(total_amount)
        receipt_image = Image.new("RGB", (400, 600), "white")
        draw = ImageDraw.Draw(receipt_image)
        
        # Add Header
        header_text = "LEERGUTBON"
        self.draw_centered_text(draw, header_text, (200, 30))

        # Add Address
        self.draw_centered_text(draw, "Supermarkt XYZ", (200, 70))
        self.draw_centered_text(draw, "Musterstraße 123", (200, 90))
        self.draw_centered_text(draw, "12345 Musterstadt", (200, 110))

        # Display Barcode Number
        self.draw_centered_text(draw, f"Leergutbon-Nr.: {barcode_text[11:18]}", (200, 150))

        # Add the total amount
        self.draw_centered_text(draw, f"Gesamtbetrag: {total_amount:.2f} EUR", (200, 300))

        # Add Date & Time
        date_time_text = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.draw_centered_text(draw, date_time_text, (200, 350))

        # Save the receipt
        output_path = os.path.join(self.output_folder, f"receipt_{barcode_text}.png")
        receipt_image.save(output_path)
        print(f"Pfandbon gespeichert unter {output_path}")

    def draw_centered_text(self, draw, text, position):
        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
        except IOError:
            font = ImageFont.load_default()
        text_width, text_height = draw.textsize(text, font=font)
        draw.text((position[0] - text_width // 2, position[1]), text, font=font, fill="black")
