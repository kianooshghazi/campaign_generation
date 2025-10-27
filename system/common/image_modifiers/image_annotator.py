from PIL import ImageDraw, ImageFont

class ImageAnnotator:
    def __init__(self, font_path="/Library/Fonts/Arial.ttf"):
        self.font_path = font_path

    def annotate(self, image, text, max_font_size=40, margin=20):
        draw = ImageDraw.Draw(image)
        width, height = image.size

        # Try font sizes from max down to small until text fits
        for font_size in range(max_font_size, 10, -2):
            font = ImageFont.truetype(self.font_path, font_size)
            lines = self._wrap_text(draw, text, font, width - 2 * margin)
            text_height = sum([draw.textbbox((0, 0), line, font=font)[3] for line in lines])
            if text_height + 2 * margin <= height:
                break

        y = height - text_height - margin
        for line in lines:
            line_width = draw.textlength(line, font=font)
            x = (width - line_width) / 2
            draw.text((x, y), line, fill="white", font=font, stroke_width=2, stroke_fill="black")
            y += draw.textbbox((0, 0), line, font=font)[3]

        return image

    def _wrap_text(self, draw, text, font, max_width):
        words = text.split()
        lines, current_line = [], ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if draw.textlength(test_line, font=font) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
