import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

print("=" * 50)
print("GEMINI API DIAGNOSTIC")
print("=" * 50)

# Check if API key exists
if not api_key:
    print("❌ ERROR: No API key found in .env file!")
    print("   Create .env file with: GEMINI_API_KEY=your_key_here")
    exit()

print(f"✅ API Key found: {api_key[:15]}...")
print(f"   Key length: {len(api_key)} characters")
print()

# Try to configure
try:
    print("Configuring Gemini API...")
    genai.configure(api_key=api_key)
    print("✅ Configuration successful!")
except Exception as e:
    print(f"❌ Configuration failed: {e}")
    exit()

# List available models
print("\n📋 Available models that support generateContent:")
print("-" * 50)

try:
    models = genai.list_models()
    found_models = False
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            found_models = True
            print(f"✅ {model.name}")
            print(f"   Display name: {model.display_name}")
            print()
    
    if not found_models:
        print("❌ No models with generateContent support found!")
        print("\n🔍 This means your API key has NO ACCESS to Gemini models.")
        print("   Possible reasons:")
        print("   1. API key is from wrong service")
        print("   2. API key is expired or invalid")
        print("   3. Your account doesn't have access")
        print("   4. Region restrictions")
        
except Exception as e:
    print(f"❌ Error listing models: {e}")