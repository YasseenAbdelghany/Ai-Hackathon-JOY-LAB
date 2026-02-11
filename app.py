import os
import uuid
import shutil
from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
from prompts import GEMINI_SYSTEM_PROMPT, ADVISOR_SYSTEM_PROMPT

app = Flask(__name__)

# Configure API Key & Client
# User must set OPENAI_API_KEY env var or rely on the fallback (which will likely fail if invalid)
API_KEY = os.getenv("OPENAI_API_KEY") 
client = OpenAI(api_key="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")

@app.route('/advisor/chat', methods=['POST'])
def advisor_chat():
    data = request.json
    history = data.get('history', [])
    
    # Prepend system prompt
    messages = [{"role": "system", "content": ADVISOR_SYSTEM_PROMPT}] + history

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return jsonify({"success": True, "reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Store games in a 'games' folder
GAMES_DIR = "games"
if not os.path.exists(GAMES_DIR):
    os.makedirs(GAMES_DIR)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/play')
def play():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    concept = data.get('concept')
    level = data.get('level', 1) # Default to Level 1
    
    if not concept:
        return jsonify({"success": False, "error": "No concept provided"})

    print(f"Generating Level {level} game for: {concept} using OpenAI")
    
    user_prompt = f"Create a LEVEL {level} simulation game for the '{concept}' Computer Science track."

    try:
        response = client.chat.completions.create(
            model="gpt-4o", # Using a capable model
            messages=[
                {"role": "system", "content": GEMINI_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        game_code = response.choices[0].message.content

        # Robust Cleanup: Extract only the HTML part
        import re
        match = re.search(r'<!DOCTYPE html>.*</html>', game_code, re.DOTALL | re.IGNORECASE)
        if match:
            game_code = match.group(0)
        else:
            # Fallback for simpler tags if DOCTYPE is missing
            match = re.search(r'<html.*</html>', game_code, re.DOTALL | re.IGNORECASE)
            if match:
                 game_code = match.group(0)
            # If no HTML tags found, we might have an issue, but we'll try to write what we have 
            # or maybe just strip code blocks.
            else:
                 if "```html" in game_code:
                    game_code = game_code.split("```html")[1].split("```")[0]
                 elif "```" in game_code:
                    game_code = game_code.split("```")[1].split("```")[0]

        # Save to unique file
        filename = f"{uuid.uuid4().hex}.html"
        filepath = os.path.join(GAMES_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(game_code)

        return jsonify({"success": True, "filename": filename})

    except Exception as e:
        print(f"Error: {e}")
        
        # Fallback logic still useful
        fallback_filename = f"fallback_{uuid.uuid4().hex}.html"
        fallback_path = os.path.join(GAMES_DIR, fallback_filename)
        
        if os.path.exists("gravity_runner.html"):
            shutil.copy("gravity_runner.html", fallback_path)
            return jsonify({
                "success": True, 
                "filename": fallback_filename, 
                "warning": f"AI Error: {str(e)} - Showing Demo Game"
            })

        return jsonify({"success": False, "error": str(e)})

@app.route('/game/<path:filename>')
def serve_game(filename):
    return send_from_directory(GAMES_DIR, filename)

if __name__ == '__main__':
    print("ConceptCade (OpenAI Edition) running on http://127.0.0.1:5000")
    app.run(debug=True)
