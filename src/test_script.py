from api_access import ApiAccess, FakeApiAccess
from screen import Screen

api_access = FakeApiAccess()
Screen(api_access).display(lambda image: image.show())