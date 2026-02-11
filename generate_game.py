import os
from openai import OpenAI
from prompts import GEMINI_SYSTEM_PROMPT

def generate_game(concept, api_key=None, output_file="game.html"):
    """
    Generates a game based on a concept using the OpenAI API.
    """
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("Error: OPENAI_API_KEY not found. Please set it as an environment variable.")
            return

    client = OpenAI(api_key=api_key)

    print(f"Generating game for concept: '{concept}' using OpenAI...")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": GEMINI_SYSTEM_PROMPT},
                {"role": "user", "content": concept}
            ]
        )
        
        game_code = response.choices[0].message.content

        # Basic cleanup
        if "```html" in game_code:
            game_code = game_code.replace("```html", "").replace("```", "")
        if "```" in game_code:
             game_code = game_code.replace("```", "")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(game_code)
            
        print(f"Game saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("--- ConceptCade Game Generator (OpenAI) ---")
    user_concept = input("Enter a concept to gamify: ")
    generate_game(user_concept)
