from typing import List
import google.generativeai as genai
import anthropic
import requests
import os
from backend.constants import get_code_prompt, get_relevant_examples_prompt, get_clip_art_prompt
import json
import time
from pathlib import Path

from backend.rag.RAG import RAG

claude = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')
def fetch_clip_art(query: str, colors: str = None) -> dict:
    """Fetch clip art images from Pixabay API based on a search query and optional color filter.

    Args:
        query: A string representing the search term for the desired clip art. Limited to 100 characters
        colors: Optional. A comma-separated string of color properties to filter images.
                Accepted values: "grayscale", "transparent", "red", "orange", "yellow", "green",
                "turquoise", "blue", "lilac", "pink", "white", "gray", "black", "brown"

    Returns:
        A dictionary containing:
        - 'success': A boolean indicating whether the operation was successful.
        - 'path': A string with the local file path of the downloaded image (if successful).
        - 'error': A string with an error message (if unsuccessful).
    """
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={query.replace(' ', '+')}&image_type=all&per_page=3"
    if colors:
        url += f"&colors={colors}"
    try:
        print(f"fetching clip art from {url}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data['hits']:
            image_url = data['hits'][0]['webformatURL']
            image_extension = os.path.splitext(image_url)[1]
            image_name = f"{query.replace(' ', '_')}{image_extension}"
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
    


def generate_manim_code(text: str) -> str:
    examples_list: List[str] = []

    for file in Path('backend/examples').glob('*.py'):
        with open(file, 'r') as f:
            content = f.read()
            class_names = [line.split('class ')[1].split('(')[0].strip() for line in content.split('\n') if line.strip().startswith('class ')]
            examples_list.extend(class_names)

    message = claude.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1500,
        temperature=1,
        system="You are an expert and knowledgeable teacher and Manim programmer. You excel at visualizing concepts in a way that is easy to understand and easy to implement in Manim.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": get_relevant_examples_prompt(examples_list, text)
                    }
                ]
            }
        ]
    )
    animation_plan = message.content[0].text
    print(f"animation plan: \n {animation_plan} \n\n")
    
    message = claude.messages.create(
        model="claude-3-5-sonnet-20240620",
        tools=[
            {
                "name": "fetch_clip_art",
                "description": "Fetch clip art images from Pixabay API based on a search query",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "A string representing the search term for the desired clip art. Limited to 100 characters. Good examples: cat, dog, dna, brain, heart, etc."},
                    },
                    "required": ["query"]
                }
                
            },
        ],
        tool_choice={"type": "auto"},
        max_tokens=1000,
        temperature=1,
        system="You are an expert at identifying clip art needs from animation plans. Answer the user's request using relevant tools (if they are available). Before calling a tool, do some analysis within \<thinking>\</thinking> tags.",
        messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": get_clip_art_prompt(text)
                        }
                    ]
            }
        ]
    )
    
    # Find examples mentioned in the animation plan using string parsing
    mentioned_examples = []
    for example in examples_list:
        if example.lower() in animation_plan.lower():
            mentioned_examples.append(example)
    print(f"mentioned examples: \n {mentioned_examples} \n\n")
    clip_art_queries = []

    
    for content in message.content:
        if isinstance(content, anthropic.types.tool_use_block.ToolUseBlock):
            print(content)
            if content.name == 'fetch_clip_art':
                query = content.input.get('query', '')
                clip_art_queries.append(query)

    code_context = []
    clip_art_paths = []
    for example in mentioned_examples:
        code_context.append(fetch_context(example))
    print(f"code context: \n {code_context} \n\n")
    print(f"clip art queries: \n {clip_art_queries} \n\n")
    for query in clip_art_queries:
        response = fetch_clip_art(query)
        if response['success']:
            clip_art_paths.append(response['path'])
    print(f"clip art paths: \n {clip_art_paths} \n\n")
    code_prompt = get_code_prompt(text, animation_plan, code_context, clip_art_paths)
    message = claude.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
            temperature=1,
            system="You are an expert Manim programmer. Before responding with the code, please make sure to think step by step and consider all the parameters and context. Then, respond with the complete, executable Manim code.",
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
    full_content = message.content[0].text
    print(f"full content: \n {full_content} \n\n")
    manim_code = full_content.split("```python")[1].split("```")[0].strip()
    print(f"manim code: \n {manim_code} \n\n")
    return manim_code
    #

def fetch_context(text: str, top_k: int = 5):
    rag = RAG(persist_dir="backend/RAG/examples_base")
    rag.load_vectorstore("backend/RAG/examples_base")
    context = rag.query(text, top_k)
    return context

