<!-- <p align="center">
  <img src="path/to/your/image.png" alt="Logo" width="100" height="100">
</p> -->
![GitHub contributors](https://img.shields.io/github/contributors/kunal-mansukhani/vid-bite) 
<!-- This will work when you make the repo public -->

<h1 align="center">VidBite</h1>

<p align="center">
  🤖 Claude Sonnet 3.5 powered generative videos. Concept. 
</p>

<img width="1087" alt="Screenshot 2024-07-10 at 11 32 59 PM" src="https://github.com/kunal-mansukhani/vid-bite/assets/66945981/4220d704-91bb-4e54-8080-fcdfca3c3d8c">


<!-- ## Table of Contents
- [Concept](#concept)
- [Usage](#usage)
- [Models Used](#models-used)
- [Demo Video](#demo-video) -->

## 🧠 Concept

Inspired by the educational style of 3Blue1Brown's videos, VidBite aims to revolutionize the way mathematical and scientific concepts are visualized by automating the generation of custom Manim code and videos. Our application leverage modern-day LLMs to produce high-quality and dynamic visualizations of concepts tailored to specific user needs. 

Users input their mathematical or scientific concepts into the application, which then utilizes powerful AI models to generate corresponding Manim code. This code can be further customized and is ready to be rendered into high-quality animations.

Here's an example video that VidBite generated for the query "CPU Pipelining":

https://github.com/kunal-mansukhani/vid-bite/assets/66945981/14756d7c-c069-419e-b967-3829f54453ed

## 🏛️ System Architecture
<img width="482" alt="Screenshot 2024-07-11 at 12 03 41 AM" src="https://github.com/kunal-mansukhani/vid-bite/assets/66945981/dc2c6655-65ea-451a-9105-b29c3af4e06c">

## 🛠️ Usage (Development)
To use VidBite:

1. Install [Manim dependencies](https://docs.manim.community/en/stable/installation.html)


2. Run the server:
    ```bash
    pip install -r requirements.txt
    python3 -m backend.server
    ```
3. Run the frontend:
    ```bash
    cd extension
    npm install
    npm start
    ```


## Models Used
| Model                       | Description                                                                 | Status  |
|-----------------------------|-----------------------------------------------------------------------------|---------|
| Claude 3.5 Sonnet    | Powerful language model for generating precise Manim code with enhanced performance and latest features.  | ✅      |

## 🔮 Future Improvements

- Chrome Extension: Develop a Chrome extension that allows users to highlight any novel STEM-related concepts encountered while browsing the web and accordingly generate explanatory videos.
- Customizable Video Settings: Introduce settings to adjust various aspects of the generated videos, such as different voice options, subtitles, and video durations, to enhance personalization.
- Image to Video Conversion: Implement functionality to convert observed images into explanatory videos, providing a visual representation of static images as well.


