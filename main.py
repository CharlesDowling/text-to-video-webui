######

# Written by Charles Dowling

######

#Export_To_Video Imports
from typing import List
import numpy as np

# Import Ai libraries
import torch
import gradio as gr
import os

# Hugging face libraries in order to work with the model (Totally not aliens)
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
#from diffusers.utils import export_to_video

# Settings imports
import json

import cv2

# Dummy video path for initializing the placeholder video player
Video_Path = None
#try:
SettingsJsonLoad = json.load(open(r"settings.json"))

### Settings Enumeration
saveDirectory = SettingsJsonLoad["OutputDirectory"]
defaultModel = SettingsJsonLoad["DefaultModel"]

## Model choice enumerations
ModelChoicesFirst=["damo-vilab/text-to-video-ms-1.7b","stabilityai/stable-diffusion-2","openai/shap-e","hotshotco/Hotshot-XL"]
ModelChoice = {}

for Model in ModelChoicesFirst:
    try:    
        # Null load to check if the model exists    
        DiffusionPipeline.from_pretrained(Model, torch_dtype=torch.float16, variant="fp16", local_files_only=True)
        print("{ModelName} Found!".format(ModelName=Model))
        ModelChoice["{ModelName} : Installed".format(ModelName=Model)] = {Model}
    except:
        print("{ModelName} : Not Found!".format(ModelName=Model))
        ModelChoice["{ModelName} : Not Installed".format(ModelName=Model)] = {Model}        
        print("Model Not Found: No {Model} in source directory".format(Model=Model))

# Sets a default value of 8 or 1 second of video generation
slidervalue = 8

##########################

#Actual Runtime Code

##########################

#Load default model
pipe = DiffusionPipeline.from_pretrained(defaultModel, torch_dtype=torch.float16, variant="fp16")

# Sets up scheduler
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
# Removes cpu reliance
pipe.enable_model_cpu_offload()
# Displays progress bar in console
pipe.progress_bar

# This function was taken from Diffusers.utils and rewriteen. "It just works" - Todd Howard
def export_to_video(video_frames: List[np.ndarray], output_video_path: str = None) -> str:
    
    fourcc = cv2.VideoWriter_fourcc(*"x264")
    h, w, c = video_frames[0].shape
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps=SliderFrameRate.value, frameSize=(w, h))
    for i in range(len(video_frames)):
        img = cv2.cvtColor(video_frames[i], cv2.COLOR_RGB2BGR)
        video_writer.write(img)
    return output_video_path

with gr.Blocks() as WebUI:

    # Loads model
    def LoadModel(ModelDrop):
        #Loads the model
        ModelToLoad = str(ModelChoice[ModelDrop]).strip("{}'")
        print("Model to Load: " + ModelToLoad)
        #Load model from choice
        pipe = DiffusionPipeline.from_pretrained(ModelToLoad, torch_dtype=torch.float16, variant="fp16")

        #Hopefully this works
        if str(ModelChoice[ModelSelect.value]).find(" : Not Installed") != -1:
            Model = ModelChoice[ModelSelect.value]
            del ModelChoice[list(ModelChoice.keys())[list(ModelChoice.values()).index({ModelSelect.value})]]
            ModelChoice["{ModelName} : Installed".format(ModelName=Model)] = {Model}
            print(Model)
        ModelDrop = gr.Dropdown(ModelChoice, label="Selected Model", value=ModelToLoad, interactive=True)

        pipe.scheduler.compatibles
        print(pipe)
        return ModelDrop    

    with gr.Row():
        # Allows for the choice of different models
        print(ModelChoice.values())
        print(list(ModelChoice.keys())[list(ModelChoice.values()).index({defaultModel})])
        ModelSelect = gr.Dropdown(ModelChoice, label="Selected Model", value=list(ModelChoice.keys())[list(ModelChoice.values()).index({defaultModel})], interactive=True)
        ModelLoad = gr.Button("Load Model")
        ModelLoad.click(fn=LoadModel, inputs=ModelSelect, outputs=ModelSelect)

    with gr.Tab("Generation") as server:
        # Generates the dang video
        def generateVideo(Prompt, NegPrompt, steps, framerate):      
            if NegPrompt == "":
                NegPrompt=None
#            try:
            # Generates the frames  
            video_frames = pipe(prompt=Prompt, negative_prompt=NegPrompt, num_inference_steps=steps).frames
            print("Finished Generating")

            #Removes witespace for file name
            Prompt = Prompt.replace(" ", "_")

            # Exports the video to{directory}{filename}.mp4
            Video_Path = export_to_video(video_frames,r"{directory}{filename}.mp4".format(filename=Prompt,directory=saveDirectory))        
            print("Finished Saving First Video")

            # Converts to fromat gradio can use cand replaces the previously generated file
            os.system("ffmpeg.exe -y -i {directory}{filename}.mp4 -r {framerate} {directory}{filename}1.mp4".format(filename=Prompt,directory=saveDirectory,framerate=framerate))
            #-vcodec libx264

            # Reinitialized video player with video file
            VideoPlayer = gr.Video(Video_Path)
            return VideoPlayer
#            except:
#               print("No model loaded")
        
        # Changes Label Text


        with gr.Row():
            with gr.Column():
                # Prompt input text
                PromptField = gr.TextArea(label="Prompt", placeholder="Type in prompt here")
                NegPromptField = gr.TextArea(label="Negative Prompt", placeholder="Type in negative prompt")

            # Made a dummy video player, will be replaced by player generated in generateVideo()
            VideoPlayer = gr.Video(Video_Path, interactive=False, height=400)

        with gr.Row():
            # Made a slider for amount of frames. Maximum is an hour because if you really need more...WHY?
            SliderSteps = gr.Slider(1, 28801, slidervalue, label="Frames", step=8, info="Video length in seconds: 1.0", interactive=True)

            def Display_Info(SliderSteps):
                Text_to_Display = ("Video length in seconds: " + str(SliderSteps/SliderFrameRate.value))
                SliderSteps = gr.Slider(1, 28801, SliderSteps, label="Frames", step=SliderFrameRate.value, info=Text_to_Display, interactive=True)
                return SliderSteps
            
            def FrameChange(SliderSteps, SliderFrameRate):
                Text_to_Display = ("Video length in seconds: " + str(SliderSteps/SliderFrameRate))
                SliderSteps = gr.Slider(1, 28801, SliderSteps, label="Frames", step=SliderFrameRate, info=Text_to_Display, interactive=True)
                return SliderSteps
            
            #SliderSteps.info = Text_to_Display
            SliderSteps.change(Display_Info, inputs=SliderSteps, outputs=SliderSteps)
            SliderFrameRate = gr.Slider(1, 60, slidervalue, label="Framerate", step=1, interactive=True)
            SliderFrameRate.change(FrameChange,inputs=[SliderSteps,SliderFrameRate], outputs=SliderSteps)



        # Button to generate and click event handler
        GenerateButton = gr.Button("Generate Video")
        GenerateButton.click(fn=generateVideo, inputs=[PromptField, NegPromptField, SliderSteps, SliderFrameRate], outputs=VideoPlayer, api_name="generate_video")

    with gr.Tab("Settings") as settings:
        def applysettings(SaveDir, DefModelDrop):
            DefModel = str(ModelChoice[DefModelDrop]).strip("{}'")
            SaveSettings = {
                "OutputDirectory" : SaveDir,
                "DefaultModel" : DefModel
                }
            with open(r"settings.json", "w") as SettingsFile:
                json.dump(SaveSettings, SettingsFile)
            
        
        OutputDirectory = gr.Textbox(label="Output Directory", value=saveDirectory, interactive=True)
        DefaultModelSelect = gr.Dropdown(ModelChoice, label="Default Model", value=list(ModelChoice.keys())[list(ModelChoice.values()).index({defaultModel})], interactive=True)
        ApplySettings = gr.Button("Apply Settings")
        ApplySettings.click(applysettings, inputs=[OutputDirectory, DefaultModelSelect])

WebUI.launch(debug=True)