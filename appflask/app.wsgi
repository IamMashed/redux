import os
APP_ROOT = os.path.join(os.path.dirname(__file__))
#activate_this = APP_ROOT+'/venv/bin/activate_this.py'
#with open(activate_this) as file_:
#    exec(file_.read(), dict(__file__=activate_this))

import sys  # noqa
sys.path.insert(0, APP_ROOT)
from app_importer import app as application  # noqa
