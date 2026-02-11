import os
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyDAw03DJSd32FijoPxKyC6shko4rP21A24"
genai.configure(api_key=API_KEY)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
