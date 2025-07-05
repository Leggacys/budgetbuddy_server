import os
from dotenv import load_dotenv


load_dotenv()

# Environment settings
ENVIRONMENT = os.getenv("ENVIRONMENT", "sandbox")  # Default to sandbox
IS_SANDBOX = ENVIRONMENT.lower() == "sandbox"

# API URLs
NORDIGEN_API_URL = "https://bankaccountdata.gocardless.com/api/v2"

# Redirect URI
REDIRECT_URI = os.environ["REDIRECT_URI"]

# Nordigen credentials
NORDIGEN_SECRET_ID = os.getenv("NORDIGEN_SECRET_ID")
NORDIGEN_SECRET_KEY = os.getenv("NORDIGEN_SECRET_KEY")

# Default sandbox institution for testing
SANDBOX_INSTITUTION_ID = "SANDBOXFINANCE_SFIN0000"

print(f"🔧 Running in {ENVIRONMENT.upper()} mode")
print(f"🔧 API URL: {NORDIGEN_API_URL}")
print(f"🔧 Sandbox mode: {IS_SANDBOX}")