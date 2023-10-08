
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

slidervalue = 8

#Loads the model
pipe = DiffusionPipeline.from_pretrained("damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16")

# Sets up scheduler
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# Removes cpu reliance
pipe.enable_model_cpu_offload()

#
pipe.progress_bar

##########################

#Actual Runtime Code

##########################

with gr.Blocks() as server:

    # Generates the dang video
    def generateVideo(Prompt,slider):      

        print(slider)

        # Generates the frames  
        video_frames = pipe(Prompt, num_inference_steps=slider).frames
        print("Finished Generating")

        #Removes witespace for file name
        Prompt.replace(" ", "_")

        # Exports the video to{directory}{filename}.mp4
        Video_Path = export_to_video(video_frames,r"{directory}{filename}.mp4".format(filename=Prompt,directory=saveDirectory))        
        print("Finished Saving First Video")

        # Converts to fromat gradio can use cand replaces the previously generated file
        os.system("ffmpeg.exe -y -i {directory}{filename}.mp4 -vcodec libx264 {directory}{filename}.mp4".format(filename=Prompt,directory=saveDirectory))

        # Reinitialized video player with video file
        VideoPlayer = gr.Video(Video_Path)
        return VideoPlayer
    
    # Changes Label Text
    def Display_Info(steps):
        Text_to_Display = ("Seconds: " + str(steps/8))
        return Text_to_Display

    # Prompt input text
    PromptField = gr.TextArea(label="Prompt", placeholder="Type in prompt here")

    with gr.Row():
        # Made a slider for amount of frames. Maximum is an hour because if you really need more...WHY?
        SliderSteps = gr.Slider(0, 28801, slidervalue, label="Frames", step=8, info="1", interactive=True)
        gr.Interface(Display_Info, SliderSteps, gr.Label(), live=True)
    

    # Made a dummy video player, will be replaced by player generated in generateVideo()
    VideoPlayer = gr.Video(Video_Path, interactive=False, height=400)

    # Button to generate and click event handler
    GenerateButton = gr.Button("Generate Video")
    GenerateButton.click(fn=generateVideo, inputs=[PromptField, SliderSteps], outputs=VideoPlayer, api_name="generate_video")

server.launch(debug=True)