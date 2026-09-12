import os

import google.generativeai as genai

# PASTE YOUR NEW API KEY HERE DIRECTLY (for testing only)
API_KEY = os.getenv("GEMINI_API_KEY")

print("🔍 Testing your API key...")
print(f"Key: {API_KEY[:15]}...")

try:
    genai.configure(api_key=API_KEY)
    
    # List all available models
    print("\n📋 Available models:")
    models = genai.list_models()
    
    found = False
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            found = True
            print(f"✅ {model.name}")
    
    if not found:
        print("❌ No models found with generateContent support!")
        
except Exception as e:
    print(f"❌ Error: {e}")