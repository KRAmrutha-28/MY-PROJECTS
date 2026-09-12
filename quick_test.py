from config import Config
print(f"API Key from config: {Config.GEMINI_API_KEY[:15]}...")
print(f"Key length: {len(Config.GEMINI_API_KEY)}")