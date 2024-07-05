import google.generativeai as genai
import anthropic
import requests
import os
from backend.constants import get_plan_prompt, get_code_prompt, get_error_fixing_prompt
import json
genai.configure(api_key='AIzaSyCmf5l6rdp6UPR29W15b-6AaVrvWrA3-wU')
claude = anthropic.Anthropic(api_key='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')

PIXABAY_API_KEY = '2540675-37862254858a0d195f577f35b'  # Replace with your actual Pixabay API key

def fetch_clip_art(query):
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query}&image_type=vector&per_page=3"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        if data['hits']:
            image_url = data['hits'][0]['webformatURL']
            image_name = f"{query.replace(' ', '_')}.jpg"
            
            # Create the clip_art directory if it doesn't exist
            clip_art_dir = os.path.join('backend', 'assets')
            os.makedirs(clip_art_dir, exist_ok=True)
            
            image_path = os.path.join('backend', 'assets', image_name)
            
            with open(image_path, 'wb') as f:
                f.write(requests.get(image_url).content)
            
            return image_path
    except requests.RequestException as e:
        print(f"Error fetching clip art: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response content: {response.text}")
    except KeyError as e:
        print(f"Unexpected response format: {e}")
        print(f"Response content: {data}")
    
    return None

def generate_manim_code(text: str, style: str, use_claude: bool) -> str:
    flash_model = genai.GenerativeModel('gemini-1.5-flash')

    plan_prompt = get_plan_prompt(text)
    plan_response = flash_model.generate_content(plan_prompt)
    animation_plan = plan_response.text.strip()

    # Extract clip art requirements
    clip_art_requirements = ["cat"]
    #for line in animation_plan.split('\n'):
        #if line.startswith("Clip Art Requirements:"):
            #clip_art_requirements = line.split(':')[1].strip().split(',')
            #break

    # Fetch clip art images
    clip_art_paths = []
    for item in clip_art_requirements:
        image_path = fetch_clip_art(item.strip())
        print(f"image_path: {image_path}")
        if image_path:
            clip_art_paths.append(image_path)
    code_prompt = get_code_prompt(text, animation_plan, clip_art_paths)
    print(code_prompt)
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