import platform
system = platform.system()

print(system)

if system == 'Darwin':
    FONT_LOCATION = '/System/Library/Fonts/Helvetica.ttc'
else:
    FONT_LOCATION = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
