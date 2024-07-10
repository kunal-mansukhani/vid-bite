from typing import List
from pathlib import Path
import importlib
import inspect

def get_plan_prompt(text: str, examples: List[str]) -> str:
    return f"""
    <task>
    Develop a comprehensive plan for a 10-30 second animation using Manim to visualize the following concept: {text}
    </task>

    <context>
    If helpful, here is a list of examples we have. Narrow down the top 3 most relevant and decide if and how to use them in your animation plan. Do not mention more than 3:
    {examples}
    </context>

    <requirements>
    Please provide:
    1. A clear, step-by-step outline of the animation sequence
    2. Detailed instructions on how to transition out of one scene and into another
    3. Extremely precise and detailed descriptions of each visual element and transition
    4. Specific timing suggestions for each step and specific size and locations for each visual/text piece
    5. Potential technical challenges a programmer might face during implementation
    6. Proposed solutions or workarounds for each identified challenge
    7. For each scene, include a section about the visuals, text, transition in, and transition out, and voice over text
    8. If standard clip art images could help the animation be more clear, then explicitly state that in your animation plan and be EXTREMELY conservative with your clip art selection. No more than 2 and they should be generic stock photos and not be able to be visualized using Manim code.

    <instructions>
    Your plan should be EXTREMELY detailed to allow a programmer to implement the animation in Manim without additional guidance. Your animation plan should include beautiful descriptions of visuals that will demonstrate the concept to the watcher. Also, explictly mention UP TO THREE EXACT example classes you used in your animation plan (e.g ExampleBackgroundRectangle, UsingRotate, DodecahedronScene). No more than 3
    </instructions>
    """

def get_relevant_examples_prompt(examples: List[str], query: str) -> str:
    return f"""
    <task>
    Here is a list of Manim examples we have. Narrow down the top 3 most relevant to visualizing {query} and decide if they will be helpful in visualizing the concept in Manim.
    {examples}

    </task>

    <instructions>
    Think step-by-step. Output a list of the exact names of the top 3 most relevant example classes. (e.g. ExampleBackgroundRectangle, UsingRotate, DodecahedronScene).
    </instructions>
    """
def get_clip_art_prompt(query: str):
    return f"""
    The goal is to visualize {query} using Manim animations. Determine if the animation for this query might require clip art images. Example: for visualizing a CNN, a clip art image of a cat could be useful as an example input image. Be EXTREMELY conservative with your clip art selection. No more than 2 and they should be generic stock photos and not be able to be easily visualized using Manim code. If no clip art is necessary, then output nothing
    """

def get_code_prompt(text: str, animation_plan: str, examples_context: List[str], asset_paths: List[str]) -> str:
    return f"""


    <user_query>
    Please visualize the following user query using a manim animation video, following the animation plan and using the relevant example_context: {text}
    </user_query>


    <animation_plan>
    {animation_plan}
    </animation_plan>

    <examples_context>
    Here are some examples that will be helpful in visualizing the user query:
    {examples_context}
    </examples_context>

    <instructions>
    Think step-by-step
    </instructions>

    <requirements>
    1. Include all necessary imports at the beginning of the file.
    2. Implement the entire animation in a single, well-structured scene class.
    3. Ensure the code is fully executable without any external dependencies or additional files.
    4. Avoid using external resources such as GIFs, images, or custom fonts unless specified.
    5. Keep variable and class names to maximum of 2 characters long
    6. Use MathTex for mathematical expressions
    7. Optimize the code for clarity, efficiency, and adherence to Manim best practices.
    8. Use Manim Voiceover Azure for the voice over and ensure the voice over is synced with the animation
    9. Carefully manage the positioning and sizing of all visual elements:
       - Use specific coordinates (e.g., UP, DOWN, LEFT, RIGHT, or exact numerical positions) for all objects.
       - Set appropriate scales for all objects to ensure they fit on the screen.
       - Utilize Manim's alignment methods (e.g., next_to(), align_to(), move_to()) to position objects relative to each other.
       - Group related objects together using VGroup when appropriate.
    10. Prevent overlapping of text and visuals:
       - Use arrange() method for organizing multiple objects.
       - Implement appropriate spacing between objects (e.g., buff parameter in positioning methods).
       - Consider using shift() to fine-tune positions if needed.
    11. Manage text visibility and readability:
       - Break long text into multiple lines using line breaks or separate Text objects.
       - Adjust font size as needed to ensure text fits and is readable.
    12. Add detailed comments explaining the positioning and sizing decisions for each visual element.
    13. Implement smooth transitions between scenes or major visual changes to enhance clarity.
    14. Use appropriate animation durations to allow viewers to comprehend each step.
    15. If using 3DScene, then inherit from both VoiceoverScene and ThreeDScene but make sure the text is in 2D. 
    16. Do not include a if __name__ == "__main__": in your code. Just write the class
    17. Use ImageMobject for clip art images. You must use these assets in your animation:
        {[path.replace('backend/', '') for path in asset_paths]}
    18. Ensure the animations fit in 1280x720 resolution

    If you are given image assets, think through how you can use them for this aniamtion, then implement it accordingly.
    </requirements>

    <examples>
    Here is an example of Manim code with Azure voiceover:
        {EXAMPLES}
    </examples>
    """

def get_error_fixing_prompt(code: str, error: str) -> str:
    return f"""
    The following Manim code produced an error:
    <code>
    Code:
    {code}
    </code>

    <error>
    {error}
    </error>

    <requirements>
    1. Include all necessary imports at the beginning of the file.
    2. Implement the entire animation in a single, well-structured scene class.
    3. Keep variable and class names to maximum of 2 characters long
    4. Use MathTex for mathematical expressions
    5. Optimize the code for clarity, efficiency, and adherence to Manim best practices.
    6. Use Manim Voiceover Azure for the voice over and ensure the voice over is synced with the animation
    7. Carefully manage the positioning and sizing of all visual elements:
       - Use specific coordinates (e.g., UP, DOWN, LEFT, RIGHT, or exact numerical positions) for all objects.
       - Set appropriate scales for all objects to ensure they fit on the screen.
       - Utilize Manim's alignment methods (e.g., next_to(), align_to(), move_to()) to position objects relative to each other.
       - Group related objects together using VGroup when appropriate.
    8. Prevent overlapping of text and visuals:
       - Use arrange() method for organizing multiple objects.
       - Implement appropriate spacing between objects (e.g., buff parameter in positioning methods).
       - Consider using shift() to fine-tune positions if needed.
    9. Manage text visibility and readability:
       - Break long text into multiple lines using line breaks or separate Text objects.
       - Adjust font size as needed to ensure text fits and is readable.
    10. Add detailed comments explaining the positioning and sizing decisions for each visual element.
    11. Implement smooth transitions between scenes or major visual changes to enhance clarity.
    12. Use appropriate animation durations to allow viewers to comprehend each step.
    13. If using 3DScene, then inherit from both VoiceoverScene and ThreeDScene but make sure the text is in 2D.
    14. Do not include a if __name__ == "__main__": in your code. Just write the class
    15. Ensure the animations fit in 1280x720 resolution
    16. Avoid removing any of the assets used in the animation
    </requirements>

    <instructions>
    Please analyze the error and suggest potential fixes. Then, implement the most promising fix and provide the ENTIRE corrected code that will run out of the box. Prioritize examples when attempting to visualize the concept. 
    </instructions>
    """

EXAMPLES = """
Example:
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.azure import AzureService


class AzureExample(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice="en-US-AriaNeural",
                style="newscast-casual",
            )
        )

        circle = Circle()
        square = Square().shift(2 * RIGHT)

        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
            self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)

        with self.voiceover(text="Now, let's transform it into a square.") as tracker:
            self.play(Transform(circle, square), run_time=tracker.duration)

        with self.voiceover(
            text="You can also change the pitch of my voice like this.",
            prosody={"pitch": "+40Hz"},
        ) as tracker:
            pass

        with self.voiceover(text="Thank you for watching."):
            self.play(Uncreate(circle))

        self.wait()

"""
