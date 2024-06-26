import shutil
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import subprocess
import tempfile
import os
from fastapi.responses import StreamingResponse, JSONResponse
import logging
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your React app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
# Configure the Gemini API
app.mount("/media", StaticFiles(directory="media"), name="media")

genai.configure(api_key='AIzaSyCmf5l6rdp6UPR29W15b-6AaVrvWrA3-wU')

class TextInput(BaseModel):
    text: str
    style: Optional[str] = "default"

@app.post("/generate_video")
async def generate_video(input: TextInput):
    try:
        # Generate Manim code using Gemini
        manim_code = generate_manim_code(input.text, input.style)
        video_path = render_manim_video(manim_code)

        # Construct the URL for the video
        video_url = f"http://localhost:8000/{video_path.relative_to(Path.cwd())}"

        # Return the URL of the generated video
        return JSONResponse(content={"videoUrl": video_url})
    except Exception as e:
        print(f"Error in generate_video: {str(e)}")  # Add this line for logging
        raise HTTPException(status_code=500, detail=str(e))

def generate_manim_code(text: str, style: str) -> str:
    # Use Gemini 1.5 Flash to generate the animation plan
    pro_model = genai.GenerativeModel('gemini-1.5-pro')
    plan_prompt = f"""
    Task: Develop a comprehensive plan for a 10-30 second animation using Manim to teach and visualize the following concept: {text}

    Please provide:
    1. A clear, step-by-step outline of the animation sequence
    2. Make sure to provide detailed instructions on how to transition out of one scene and into another
    2. Detailed descriptions of each visual element and transition
    3. Specific timing suggestions for each step
    4. Potential technical challenges a programmer might face during implementation
    5. Proposed solutions or workarounds for each identified challenge

    Your plan should be sufficiently detailed to allow a programmer to implement the animation in Manim without additional guidance.

    Structure your response as follows:
    1. Animation Plan
    2. Technical Considerations

    Begin your response with the Animation Plan.
    """

    plan_response = pro_model.generate_content(plan_prompt)
    animation_plan = plan_response.text.strip()

    print("Animation Plan:")
    print(animation_plan)
    examples = """
Example 1: BraceAnnotation
from manim import *

class BraceAnnotation(Scene):
    def construct(self):
        dot = Dot([-2, -1, 0])
        dot2 = Dot([2, 1, 0])
        line = Line(dot.get_center(), dot2.get_center()).set_color(ORANGE)
        b1 = Brace(line)
        b1text = b1.get_text("Horizontal distance")
        b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        b2text = b2.get_tex("x-x_1")
        self.add(line, dot, dot2, b1, b2, b1text, b2text)
Example 2:
VectorArrow
from manim import *

class VectorArrow(Scene):
    def construct(self):
        dot = Dot(ORIGIN)
        arrow = Arrow(ORIGIN, [2, 2, 0], buff=0)
        numberplane = NumberPlane()
        origin_text = Text('(0, 0)').next_to(dot, DOWN)
        tip_text = Text('(2, 2)').next_to(arrow.get_end(), RIGHT)
        self.add(numberplane, dot, arrow, origin_text, tip_text)
Example 3:
GradientImageFromArray
from manim import *

class GradientImageFromArray(Scene):
    def construct(self):
        n = 256
        imageArray = np.uint8(
            [[i * 256 / n for i in range(0, n)] for _ in range(0, n)]
        )
        image = ImageMobject(imageArray).scale(2)
        image.background_rectangle = SurroundingRectangle(image, GREEN)
        self.add(image, image.background_rectangle)
Example 4: 
BooleanOperations
from manim import *

class BooleanOperations(Scene):
    def construct(self):
        ellipse1 = Ellipse(
            width=4.0, height=5.0, fill_opacity=0.5, color=BLUE, stroke_width=10
        ).move_to(LEFT)
        ellipse2 = ellipse1.copy().set_color(color=RED).move_to(RIGHT)
        bool_ops_text = MarkupText("<u>Boolean Operation</u>").next_to(ellipse1, UP * 3)
        ellipse_group = Group(bool_ops_text, ellipse1, ellipse2).move_to(LEFT * 3)
        self.play(FadeIn(ellipse_group))

        i = Intersection(ellipse1, ellipse2, color=GREEN, fill_opacity=0.5)
        self.play(i.animate.scale(0.25).move_to(RIGHT * 5 + UP * 2.5))
        intersection_text = Text("Intersection", font_size=23).next_to(i, UP)
        self.play(FadeIn(intersection_text))

        u = Union(ellipse1, ellipse2, color=ORANGE, fill_opacity=0.5)
        union_text = Text("Union", font_size=23)
        self.play(u.animate.scale(0.3).next_to(i, DOWN, buff=union_text.height * 3))
        union_text.next_to(u, UP)
        self.play(FadeIn(union_text))

        e = Exclusion(ellipse1, ellipse2, color=YELLOW, fill_opacity=0.5)
        exclusion_text = Text("Exclusion", font_size=23)
        self.play(e.animate.scale(0.3).next_to(u, DOWN, buff=exclusion_text.height * 3.5))
        exclusion_text.next_to(e, UP)
        self.play(FadeIn(exclusion_text))

        d = Difference(ellipse1, ellipse2, color=PINK, fill_opacity=0.5)
        difference_text = Text("Difference", font_size=23)
        self.play(d.animate.scale(0.3).next_to(u, LEFT, buff=difference_text.height * 3.5))
        difference_text.next_to(d, UP)
        self.play(FadeIn(difference_text))

Example 5:
PointMovingOnShapes
from manim import *

class PointMovingOnShapes(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()
Example 6:
MovingAround
from manim import *

class MovingAround(Scene):
    def construct(self):
        square = Square(color=BLUE, fill_opacity=1)

        self.play(square.animate.shift(LEFT))
        self.play(square.animate.set_fill(ORANGE))
        self.play(square.animate.scale(0.3))
        self.play(square.animate.rotate(0.4))
Example 7:
MovingAngle
from manim import *

class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT

        theta_tracker = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            Angle(
                line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )

        self.add(line1, line_moving, a, tex)
        self.wait()

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )

        a.add_updater(
            lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))

"""
    # Use Gemini Pro to generate the Manim code based on the plan
    pro_model = genai.GenerativeModel('gemini-1.5-pro')
    code_prompt = f"""
    Based on the provided animation plan, generate a complete, self-contained Manim code implementation:

    
    {animation_plan}

    Requirements:
    1. Include all necessary imports at the beginning of the file.
    2. Implement the entire animation in a single, well-structured scene class.
    3. Ensure the code is fully executable without any external dependencies or additional files.
    4. Avoid using external resources such as GIFs, images, or custom fonts.
    5. Optimize the code for clarity, efficiency, and adherence to Manim best practices and ensure all the text fits on the screen.

    Your response should consist solely of the Python code for Manim, without any additional explanations or comments.

    Here are some examples of good manim animation code:
    {examples}
    """

    code_response = pro_model.generate_content(code_prompt)
    manim_code = code_response.text.strip()
    manim_code = manim_code.replace("```python", "").replace("```", "")

    print("\nManim Code:")
    print(manim_code)

    return manim_code

def render_manim_video(manim_code: str, max_attempts=4):
    flash_model = genai.GenerativeModel('gemini-1.5-pro')
    attempt = 0
    
    while attempt < max_attempts:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(manim_code)
            temp_file_path = temp_file.name

        try:
            # Clear the media directory before rendering
            media_dir = Path("media")
            if media_dir.exists():
                shutil.rmtree(media_dir)

            # Run Manim to generate the video
            result = subprocess.run(["manim", "-qm", temp_file_path], 
                                    check=True, 
                                    capture_output=True, 
                                    text=True)
            
            # Determine the scene name (assuming it's the class name 'AnGen')                        
            video_dir = Path("media") / "videos" / Path(temp_file_path).stem / "720p30"
            video_files = list(video_dir.glob("*.mp4"))
            print(f"Video files: {video_files}")
            if video_files:
                video_path = video_files[0]
                return video_path
            else:
                raise FileNotFoundError(f"Generated video file not found in {video_dir}")
            

        except subprocess.CalledProcessError as e:
            print(f"Error in Manim execution (attempt {attempt + 1}): {e}")
            print(f"Manim error output: {e.stderr}")
            
            if attempt < max_attempts - 1:
                # Ask Gemini to analyze the error and suggest fixes
                analysis_prompt = f"""
                The following Manim code produced an error:

                Code:
                {manim_code}

                Error:
                {e.stderr}

                Please analyze the error and suggest potential fixes. If the error is about missing files then remove the dependency of those files from the code. Then, implement the most promising fix and provide the entire corrected code.
                - Include all necessary imports
                - Provide the full class definition
                - Ensure the code is complete and ready to run without any additional dependencies or libraries
                - The code should run out-of-the-box WITHOUT additional files like external gifs or images

                """
                fix_response = flash_model.generate_content(analysis_prompt)
                
                # Extract the corrected code from the response
                corrected_code = fix_response.text.split("```python")[-1].split("```")[0].strip()
                
                manim_code = corrected_code
                print(f"Updated Manim code (attempt {attempt + 2}):\n{manim_code}")
            else:
                raise HTTPException(status_code=500, detail="Failed to generate video after multiple attempts")

        except Exception as e:
            print(f"Unexpected error (attempt {attempt + 1}): {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            os.unlink(temp_file_path)

        attempt += 1

    raise HTTPException(status_code=500, detail="Failed to generate video after maximum attempts")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
