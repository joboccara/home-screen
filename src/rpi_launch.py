from pathlib import Path
import os
import sys
libdir = Path("/home/jonathan/projects/home-screen-dependencies/e-Paper/RaspberryPi_JetsonNano/python/lib")
sys.path.append(str(libdir))

from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2
from screen import Screen
from api_access import ApiAccess

epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()
epd.init_fast()
epd.init_part()
Screen(ApiAccess()).display(lambda image: epd.display_Partial(epd.getbuffer(image), 0, 0, epd.width, epd.height))
