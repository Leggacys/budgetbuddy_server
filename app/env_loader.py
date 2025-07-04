import os
from flask.cli import load_dotenv


load_dotenv()

def load_nordingen_production_url():
    return os.getenv("NORDIGEN_API_URL_PROD")

def load_redirect_uri():
    return os.getenv("REDIRECT_URI")

def load_nordigen_secret_id():
    return os.getenv("NORDIGEN_SECRET_ID")

def load_nordigen_secret_key():
    return os.getenv("NORDIGEN_SECRET_KEY")