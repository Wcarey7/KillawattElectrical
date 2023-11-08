import os
from dotenv import load_dotenv
from app import create_app


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


#################################################################################
#### App Entry Point
####
#### Set config with a .env file placed in the root project directory.
#### If no .env or environment variable set, default(DevelopmentConfig) is used.
#### Example: FLASK_ENV=development
#################################################################################
app = create_app(os.getenv('FLASK_ENV') or 'default')
