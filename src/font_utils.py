import platform
system = platform.system()

if system == 'Darwin':
    FONT_LOCATION = '/System/Library/Fonts/Helvetica.ttc'
    REVERSE_FONT_LOCATION = '/System/Library/Fonts/ArialHB.ttc'
else:
    FONT_LOCATION = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    REVERSE_FONT_LOCATION = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def text_size(text, free_type_font):
    size, offset = free_type_font.font.getsize(text)
    return (size[0] + offset[0], size[1] + offset[1])

def text_width(text, free_type_font):
    return text_size(text, free_type_font)[0]

def text_height(text, free_type_font):
    return text_size(text, free_type_font)[1]

def wrapped_text_height(text, free_type_font, max_width):
    lines = wrap_text_to_lines(text, free_type_font, max_width)
    nb_lines = len(lines)
    if nb_lines == 0: return 0

    return nb_lines * (text_height(lines[0], free_type_font) + line_spacing(free_type_font))

def line_spacing(free_type_font):
    return free_type_font.size / 3

def wrap_text_to_lines(text, free_type_font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        current_line_with_word = f"{current_line} {word}".strip()
        if text_width(current_line_with_word, free_type_font) <= max_width:
            current_line = current_line_with_word
        else:
            lines.append(current_line)
            current_line = word
    if current_line != "":
        lines.append(current_line)
    return lines

def reverse_script(text):
    return text[::-1]