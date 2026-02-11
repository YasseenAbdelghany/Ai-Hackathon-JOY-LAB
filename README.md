# ConceptCade

ConceptCade is an AI-powered game generator that takes abstract concepts and turns them into playable HTML5/Canvas games.

## Getting Started

### 1. Proof of Concept: Gravity Runner
Open `gravity_runner.html` in your browser to play a demo game generated based on the concept of "Anti-Gravity".

### 3. Use the Web Interface (Recommended)
This provides a graphical interface to generate and play games.

1.  **Install Dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

2.  **Set your OpenAI API Key:**
    ```powershell
    $env:OPENAI_API_KEY = "your_openai_api_key_here"
    ```

3.  **Run the App:**
    ```powershell
    python app.py
    ```

3.  **Play:**
    Open `http://127.0.0.1:5000` in your browser.
    Enter a concept and click GENERATE!

## Project Structure
- `app.py`: Flask web application.
- `templates/index.html`: Web interface.
- `static/style.css`: Neon styling.
- `games/`: Directory where generated games are saved.
- `prompts.py`: AI system prompt.
- `gravity_runner.html`: Pre-generated demo game.
