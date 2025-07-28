import os
from pathlib import Path
from dotenv import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__))
DATA_IMPORT = Path(APP_ROOT) / 'app' / 'data_import'
STORAGE_DIR = Path(APP_ROOT) / 'storage'
EVIDENCE_DIR = Path(APP_ROOT) / 'storage' / 'evidence'
EVIDENCE_TEMPLATE_NAME = 'ReduxCoverPage_05_02_21.pdf'

MAPBOX_URL = 'https://api.mapbox.com/styles/v1'
MAPBOX_TOKEN = 'pk.eyJ1IjoicmVkdXgxIiwiYSI6ImNrNXpnMzkzYzJyMmIzbG5uM2xlZGJjdWwifQ._0ovg99Mq_VwbVTmrUrJPw'
MAPBOX_STYLE_ID = 'ck7tqt0yy03sb1ipekp8z2a6d'
MAPBOX_USERNAME = 'redux1'

dotenv_path = os.path.join(APP_ROOT, '.env')

# Load Environment variables from .env
load_dotenv(dotenv_path)

DEBUG = os.getenv('DEBUG')

SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
REPAIR_APPLICATION_SECRET_KEY = os.getenv('REPAIR_APPLICATION_SECRET_KEY') or 'repair application secret key'

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')

APPLICATIONS_DIR = os.getenv('APPLICATIONS_DIR') or 'applications'
IMAGES_OBSERVER_DIR = STORAGE_DIR / APPLICATIONS_DIR

WTF_CSRF_CHECK_DEFAULT = False
WTF_CSRF_ENABLED = False

SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = os.getenv('FLASK_PASSWORD_SALT')

SECURITY_REGISTERABLE = False
SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
SECURITY_USER_IDENTITY_ATTRIBUTES = 'username'
SECURITY_UNAUTHORIZED_VIEW = '/login'
REMEMBER_COOKIE_DURATION = 31536000

FLASK_CORS = os.getenv('FLASK_CORS', False)

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

LANGUAGES = ['en']

BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'UTC'

ROLE_ADMIN = 'admin'
ROLE_MEMBER = 'member'
ROLE_GUEST = 'guest'

USER_ROLES = (
    ROLE_ADMIN,
    ROLE_MEMBER,
    ROLE_GUEST
)

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': min(10, os.cpu_count() * 2),
    'max_overflow': min(15, os.cpu_count() * 4),
}

MAX_WORKER_COUNT = 10

REDIS_URL = os.getenv('REDIS_URL') or 'redis://'
MASS_CMA_LIMIT = os.getenv('MASS_CMA_LIMIT')
MASS_CMA_CHUNK_SIZE = os.getenv('MASS_CMA_CHUNK_SIZE') or 20

WTF_CSRF_TIME_LIMIT = None

UPLOADED_PHOTOS_DEST = STORAGE_DIR / 'counties'
JSON_SORT_KEYS = False

MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
               ['true', 'on', '1']
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_SENDER = 'From: Redux Property Tax Services <noreply@redux.tax>'
MAIL_ALLOWED = os.getenv('MAIL_ALLOWED', False)

# Redux domain dedicated
if os.getenv('REDUX'):
    REMEMBER_COOKIE_DOMAIN = ".redux.tax"
    REMEMBER_COOKIE_REFRESH_EACH_REQUEST = True
    DEFAULT_REMEMBER_ME = True
    SESSION_COOKIE_DOMAIN = ".redux.tax"

# SQLALCHEMY_ECHO = True
