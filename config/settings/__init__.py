from .base import *

if not config("DEBUG", cast=bool):
    from .production import *
else:
    from .local import *
