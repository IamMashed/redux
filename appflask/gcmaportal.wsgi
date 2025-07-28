import os

APP_ROOT = os.path.join(os.path.dirname(__file__))

import sys  # noqa

sys.path.insert(0, APP_ROOT)
from gcmaportal_importer import app as application  # noqa
