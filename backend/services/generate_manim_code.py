import google.generativeai as genai
import anthropic
import requests
import os
from backend.constants import get_plan_prompt, get_code_prompt, get_error_fixing_prompt
import json
genai.configure(api_key='AIzaSyCmf5l6rdp6UPR29W15b-6AaVrvWrA3-wU')
claude = anthropic.Anthropic(api_key='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')

PIXABAY_API_KEY = '2540675-37862254858a0d195f577f35b'  # Replace with your actual Pixabay API key

def fetch_clip_art(query: str) -> dict:
    """Fetch clip art images from Pixabay API based on a search query.

    Args:
        query: A string representing the search term for the desired clip art.

    Returns:
        A dictionary containing:
        - 'success': A boolean indicating whether the operation was successful.
        - 'path': A string with the local file path of the downloaded image (if successful).
        - 'error': A string with an error message (if unsuccessful).
    """
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=vector&per_page=3"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data['hits']:
            image_url = data['hits'][0]['webformatURL']
            image_name = f"{query.replace(' ', '_')}.jpg"
            
            clip_art_dir = os.path.join('backend', 'assets')
            os.makedirs(clip_art_dir, exist_ok=True)
            
            image_path = os.path.join(clip_art_dir, image_name)
            
            with open(image_path, 'wb') as f:
                f.write(requests.get(image_url).content)
            
            return {"success": True, "path": image_path}
        else:
            return {"success": False, "error": "No images found"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def generate_manim_code(text: str, style: str, use_claude: bool) -> str:
    flash_model = genai.GenerativeModel('gemini-1.5-flash')
    chat = flash_model.start_chat()
    plan_prompt = get_plan_prompt(text)
    plan_response = chat.send_message(plan_prompt)
    animation_plan = plan_response.candidates[0].content.parts[0].text.strip()
    print(f"animation plan: {animation_plan}")
    function_calls_response = chat.send_message("Fetch all the clip arts referenced in the animation plan.", tools=[fetch_clip_art])
    print(f"function calls: {function_calls_response}")
    clip_art_paths = []
    for part in function_calls_response.candidates[0].content.parts:
        if part.function_call:
            fn = part.function_call
            if fn.name == "fetch_clip_art":
                query = fn.args['query']
                if query != "":
                    result = fetch_clip_art(query)
                    if result["success"]:
                        clip_art_paths.append(result["path"])
    print(f"clip art paths: {clip_art_paths}")
    code_prompt = get_code_prompt(text, animation_plan, clip_art_paths, use_claude)
    if use_claude:
        message = claude.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            temperature=1,
            system="You are an expert Manim programmer. Respond only with complete, executable Manim code.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": code_prompt
                        }
                    ]
                }
            ]
        )
        manim_code = message.content[0].text.strip()
    else:
        pro_model = genai.GenerativeModel('gemini-1.5-pro')
        code_response = pro_model.generate_content(code_prompt)
        manim_code = code_response.text.strip()
        print(manim_code)

    manim_code = manim_code.replace("```python", "").replace("```", "")
    return manim_code