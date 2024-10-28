from date_time_widget import DateTimeWidget
from pen import Pen
from PIL import Image

image = Image.new('1', (480, 800), 255)

DateTimeWidget().draw(Pen(image, (100, 50)))

image.show()