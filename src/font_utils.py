import platform
system = platform.system()

if system == 'Darwin':
    FONT_LOCATION = '/System/Library/Fonts/Helvetica.ttc'
else:
    FONT_LOCATION = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def textsize(text, free_type_font):
    size, offset = free_type_font.font.getsize(text)
    return (size[0] + offset[0], size[1] + offset[1])

def textwidth(text, free_type_font):
    return textsize(text, free_type_font)[0]

def textheight(text, free_type_font):
    return textsize(text, free_type_font)[1]
