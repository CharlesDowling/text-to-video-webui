import tempfile
from contextlib import contextmanager
from typing import List
import numpy as np
import cv2

# Import Ai libraries
import torch
import gradio as gr
import os

# Hugging face libraries in order to work with the model (Totally not aliens)
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video

# Dummy video path for initializing the placeholder video player
Video_Path = None

#
saveDirectory = "output/"

#Loads the model
pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")

# Sets up scheduler
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# Removes cpu reliance
pipe.enable_model_cpu_offload()


pipe.progress_bar

##########################

#Actual Runtime Code

##########################

with gr.Blocks() as server:

    # Generates the dang video
    def generateVideo(Prompt):        
        video_frames = pipe(Prompt, num_inference_steps=StepsSlider).frames
        print("Finished Generating")
        Prompt.replace(" ", "_")
        Video_Path = export_to_video(video_frames,r"{directory}{filename}.mp4".format(filename=Prompt,directory=saveDirectory))        
        print("Finished Saving First Video")
        os.system("ffmpeg.exe -y -i {directory}{filename}.mp4 -vcodec libx264 {directory}{filename}.mp4".format(filename=Prompt,directory=saveDirectory))
        VideoPlayer = gr.Video(Video_Path)
        return VideoPlayer

    # Prompt input text
    PromptField = gr.TextArea(label="Prompt", placeholder="Type in prompt here")

    # Made a slider for amount of frames. Maximum is an hour because if you really need more...WHY?
    StepsSlider = gr.Slider(0, 28801, 1, label="Frames", step=8, info="1", interactive=True)

    # Made a dummy video player, will be replaced by player generated in generateVideo()
    VideoPlayer = gr.Video(Video_Path, interactive=False, height=400)

    # Button to generate and click event handler
    GenerateButton = gr.Button("Generate Video")
    GenerateButton.click(fn=generateVideo, inputs=PromptField, outputs=VideoPlayer, api_name="generate_video")

server.launch()

