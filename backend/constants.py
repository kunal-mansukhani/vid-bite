from typing import List


def get_plan_prompt(text: str) -> str:
    return f"""
    Task: Develop a comprehensive plan for a 10-30 second animation using Manim to visualize the following concept: {text}

    Please provide:
    1. A clear, step-by-step outline of the animation sequence
    2. Make sure to provide detailed instructions on how to transition out of one scene and into another
    3. Extremely precise and detailed descriptions of each visual element and transition
    4. Specific timing suggestions for each step and specific size and locations for each visual/text piece
    5. Potential technical challenges a programmer might face during implementation
    6. Proposed solutions or workarounds for each identified challenge
    7. For each scene, include a section about the visuals, text, transition in, and transition out, and voice over text
    8. If the animaton would be improved with standard clip art stock iamges, then include it in the animation plan but use them conservatively.

    Your plan should be EXTREMELY detailed to allow a programmer to implement the animation in Manim without additional guidance. Your animation plan should include beautiful descriptions of visuals that will demonstrate the concept to the watcher. 

    Structure your response as follows:
    1. Animation Plan
    2. Technical Considerations
    3. Clip Art Requirements

    Begin your response with the Animation Plan.

    At the end of your response, include a section titled "Clip Art Requirements" that clearly lists all the clip art images needed for the animation. 
    Example:
    Clip Art Requirements: Cat,Stopsign
    Example 2:
    Clip[ Art Requirements: Dog,Car,Stickfigure
    Follow this exact format for the Clip Art Requirements with comma seperated list
    """
def get_code_prompt(text: str, animation_plan: str, asset_paths: List[str]) -> str:
    return f"""
    Write manim code that visualizes the following: {text}
    Animation Plan:
    {animation_plan}
    Requirements:
    1. Include all necessary imports at the beginning of the file.
    2. Implement the entire animation in a single, well-structured scene class.
    3. Ensure the code is fully executable without any external dependencies or additional files.
    4. Avoid using external resources such as GIFs, images, or custom fonts.
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
    15. Use ImageMobject to insert assets 
    16. Use the following asset paths where appropriate in your code: {[path.replace('backend/', '') for path in asset_paths]}
    Your response should consist solely of the Python code for Manim, without any additional explanations or comments or introductory sentence.

    Here are some examples of good manim animation code:
        {EXAMPLES}
        """
    
def get_error_fixing_prompt(code: str, error: str) -> str:
    return f"""
    The following Manim code produced an error:

    Code:
    {code}

    Error:
    {error}

    Please analyze the error and suggest potential fixes. If the error is about missing files then remove the dependency of those files from the code. Then, implement the most promising fix and provide the entire corrected code.
    - Include all necessary imports
    - Provide the full class definition
    - Ensure the code is complete and ready to run without any additional dependencies or libraries
    - The code should run out-of-the-box WITHOUT additional files like external gifs or images
    """
EXAMPLES = """
Example 1:
from manim import *
import pygments.styles as code_styles
from manim_voiceover import VoiceoverScene

from manim_voiceover.services.azure import AzureService

code_style = code_styles.get_style_by_name('one-dark')


class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        # Initialize speech synthesis using Azure's TTS API
        self.set_speech_service(
            AzureService(
                voice='en-US-AriaNeural',
                style='newscast-casual',  # global_speed=1.15
            )
        )
        banner = ManimBanner().scale(0.5)

        with self.voiceover(text='Hey Manim Community!'):
            self.play(
                banner.create(),
            )

        tracker = self.add_voiceover_text(
            'Today, I want to show you how you can generate voiceovers directly in your Python code.'
        )

        self.play(banner.expand())
        self.wait(tracker.get_remaining_duration(buff=-1))
        self.play(FadeOut(banner))

        demo_code = Code(
            code='''tracker = self.add_voiceover_text(
    '''AI generated voices have become realistic
        enough for use in most content. Using neural
        text-to-speech frees you from the painstaking
        process of recording and manually syncing
        audio to your video.'''
)
self.play(Write(demo_code), run_time=tracker.duration)''',
            insert_line_no=False,
            style=code_style,
            background='window',
            font='Consolas',
            language='python',
        ).rescale_to_fit(12, 0)

        tracker = self.add_voiceover_text(
            '''AI generated voices have become realistic
                enough for use in most content. Using neural
                text-to-speech frees you from the painstaking
                process of recording and manually syncing
                audio to your video.'''
        )
        self.play(Write(demo_code), run_time=tracker.duration)

        with self.voiceover(
            text='''As you can see, Manim started playing this voiceover,
                right as the code object started to be drawn.
                Let's see some more examples.'''
        ):
            pass

        self.play(FadeOut(demo_code))

        circle = Circle()
        square = Square().shift(2 * RIGHT)

        with self.voiceover(text='This circle is drawn as I speak.') as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        with self.voiceover(text='Let's shift it to the left 2 units.') as tracker:
            self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)

        with self.voiceover(text='Now, let's transform it into a square.') as tracker:
            self.play(Transform(circle, square), run_time=tracker.duration)

        with self.voiceover(text='I would go on, but you get the idea.'):
            self.play(FadeOut(circle))

        demo_code2 = Code(
            code='''class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice='en-US-AriaNeural',
                style='newscast-casual',
                global_speed=1.15
            )
        )
        circle = Circle()

        with self.voiceover(text='This circle is drawn as I speak.'):
            self.play(Create(circle))

        with self.voiceover(text='Let's shift it to the left 2 units.') as tracker:
            self.play(circle.animate.shift(2 * LEFT), run_time=tracker.duration)''',
            insert_line_no=False,
            style=code_style,
            background='window',
            font='Consolas',
            language='python',
        ).rescale_to_fit(12, 0)

        with self.voiceover(text='Let's see how the API works!'):
            self.play(FadeIn(demo_code2.background_mobject))

        with self.voiceover(
            text='First, we create a scene using the Voiceover Scene class from the plugin.'
        ):
            self.play(FadeIn(demo_code2.code[:2]))

        with self.voiceover(
            text='Then, we initialize the voiceover by setting the appropriate speech synthesizer.'
        ):
            self.play(FadeIn(demo_code2.code[2]))

        with self.voiceover(text='In this example, we use Azure Text-to-speech.'):
            self.play(FadeIn(demo_code2.code[3]))

        with self.voiceover(
            text='We use the English speaking neural voice called Aria.'
        ):
            self.play(FadeIn(demo_code2.code[4]))

        with self.voiceover(text='We use the style called 'newscast casual'.'):
            self.play(FadeIn(demo_code2.code[5]))

        with self.voiceover(
            text='''Finally, we give an option to speed up the voiceover
            playback fifteen percent, because the default is a bit too slow.'''
        ):
            self.play(FadeIn(demo_code2.code[6:9]))

        with self.voiceover(
            text='''With the configuration out of the way, it is time to animate.'''
        ):
            pass

        with self.voiceover(text='''Let's initialize the circle object.'''):
            self.play(FadeIn(demo_code2.code[9:11]))

        with self.voiceover(
            text='''Then, we need to tell the scene to start narrating,
            by calling the function 'self-dot-voiceover'.'''
        ):
            self.play(FadeIn(demo_code2.code[11]))

        with self.voiceover(
            text='''By wrapping our animation inside a 'with-statement',
            we ensure that once it finishes playing, it will also wait for
            the voiceover playback to finish.'''
        ):
            self.play(FadeIn(demo_code2.code[12]))

        with self.voiceover(
            text='''This is extremely convenient, and let's you chain
            voiceovers back to back without having to think how long they are.'''
        ):
            pass

        with self.voiceover(
            text='''We just need to repeat the same pattern with self-dot-voiceover and with-statements. Here is something cool.'''
        ):
            self.play(FadeIn(demo_code2.code[14]))

        with self.voiceover(
            text='''We can retrieve the duration of the generated voiceover programmatically, and then use it to define for how long an animation should play.'''
        ):
            self.play(FadeIn(demo_code2.code[15]))

        demo_code3 = Code(
            code='''class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        self.set_speech_service(
            AzureService(
                voice='en-US-AriaNeural',
                style='newscast-casual',
                global_speed=1.15
            )
        )
        # self.set_speech_service(
        #     StitcherService('my_voice_recording.mp3')
        # )
        ''',
            insert_line_no=False,
            style=code_style,
            background='window',
            font='Consolas',
            language='python',
        ).scale(0.85)

        demo_code4 = (
            Code(
                code='''class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        # self.set_speech_service(
        #     AzureService(
        #         voice='en-US-AriaNeural',
        #         style='newscast-casual',
        #         global_speed=1.15
        #     )
        # )
        # self.set_speech_service(
        #     StitcherService('my_voice_recording.mp3')
        # )
        ''',
                insert_line_no=False,
                style=code_style,
                background='window',
                font='Consolas',
                language='python',
            )
            .scale(0.85)
            .align_to(demo_code3, LEFT)
        )

        demo_code5 = (
            Code(
                code='''class VoiceoverDemo(VoiceoverScene):
    def construct(self):
        # self.set_speech_service(
        #     AzureService(
        #         voice='en-US-AriaNeural',
        #         style='newscast-casual',
        #         global_speed=1.15
        #     )
        # )
        self.set_speech_service(
            StitcherService('my_voice_recording.mp3')
        )
        ''',
                insert_line_no=False,
                style=code_style,
                background='window',
                font='Consolas',
                language='python',
            )
            .scale(0.85)
            .align_to(demo_code3, LEFT)
        )

        with self.voiceover(
            text='And that's not even the best part! You can switch the AI generated voice with an actual recording of your voice very easily.'
        ):
            self.play(FadeOut(demo_code2))
            self.wait()
            text1 = Tex('AI voice')
            arrow = Tex(r'$\rightarrow$')
            text2 = Tex('Voice recording')
            VGroup(text1, arrow, text2).arrange(RIGHT)
            self.play(Write(text1))
            self.play(Write(arrow))
            self.wait()
            self.play(Write(text2))
            self.wait()
            self.play(FadeOut(text1, text2, arrow))

        with self.voiceover(
            text='To do that, you record an MP3 of the final text of your video.'
        ):
            self.play(FadeIn(demo_code3))

        with self.voiceover(
            text='''Manim-voiceover then splits your audio automatically and replaces the AI generated voice with your real recording.'''
        ):
            self.play(FadeOut(demo_code3.code), FadeIn(demo_code4.code))
            self.play(FadeOut(demo_code4.code), FadeIn(demo_code5.code))

        self.wait(2)

        with self.voiceover(
            text='''Manim-voiceover makes it much easier to do voiceovers for Manim projects.'''
        ):
            self.play(FadeOut(demo_code5.code, demo_code3.background_mobject))

        with self.voiceover(
            text='Visit the GitHub repo to start using it in your project.'
        ):
            self.play(
                FadeIn(
                    Tex(r'\texttt{https://github.com/ManimCommunity/manim-voiceover}')
                )
            )

    self.wait(5)

    Example 2:
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
