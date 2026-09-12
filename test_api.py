import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

print(f"API Key found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key starts with: {api_key[:10]}...")
    print(f"API Key length: {len(api_key)}")