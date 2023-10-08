# Import Ai libraries
import torch
import gradio as gr
import os
from huggingface_hub import model_info, hf_hub_download

# Hugging face libraries in order to work with the model (Totally not aliens)
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video

# Settings imports
import json

# Dummy video path for initializing the placeholder video player
Video_Path = None
#try:
SettingsJsonLoad = json.load(open(r"settings.json"))

### Settings Enumeration
saveDirectory = SettingsJsonLoad["OutputDirectory"]
defaultModel = SettingsJsonLoad["DefaultModel"]

## Model choice enumerations
ModelChoicesFirst=["damo-vilab/text-to-video-ms-1.7b","damo-vilab/modelscope-damo-text-to-video-synthesis","damo-vilab/text-to-video-ms-1.7b-legacy","hotshotco/Hotshot-XL"]
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

with gr.Blocks() as WebUI:

    # F***ing ridiculously long bulls**t just to make it chooseable
    pipe = DiffusionPipeline.from_pretrained(str(ModelChoice[list(ModelChoice.keys())[list(ModelChoice.values()).index({defaultModel})]]).strip("{}'"), torch_dtype=torch.float16, variant="fp16")
    # Sets up scheduler
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    # Removes cpu reliance
    pipe.enable_model_cpu_offload()
    # Displays progress bar in console
    pipe.progress_bar
    
    # Loads model
    def LoadModel():
        #Loads the model
        ModelToLoad = str(ModelChoice[ModelSelect.value]).strip("{}'")
        pipe = DiffusionPipeline.from_pretrained(ModelToLoad, torch_dtype=torch.float16, variant="fp16")
        # Sets up scheduler
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        # Removes cpu reliance
        pipe.enable_model_cpu_offload()
        # Displays progress bar in console
        pipe.progress_bar

    with gr.Row():
        # Allows for the choice of different models
        print(ModelChoice.values())
        print(list(ModelChoice.keys())[list(ModelChoice.values()).index({defaultModel})])
        ModelSelect = gr.Dropdown(ModelChoice, label="Selected Model", value=list(ModelChoice.keys())[list(ModelChoice.values()).index({defaultModel})], interactive=True)
        ModelLoad = gr.Button("Load Model")
        ModelLoad.click(fn=LoadModel())

    with gr.Tab("Generation") as server:
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

        with gr.Row():
            # Prompt input text
            PromptField = gr.TextArea(label="Prompt", placeholder="Type in prompt here")

            # Made a dummy video player, will be replaced by player generated in generateVideo()
            VideoPlayer = gr.Video(Video_Path, interactive=False, height=400)

        with gr.Row():

            # Made a slider for amount of frames. Maximum is an hour because if you really need more...WHY?
            SliderSteps = gr.Slider(0, 28801, slidervalue, label="Frames", step=8, info="1", interactive=True)
            gr.Interface(Display_Info, SliderSteps, gr.Label(), live=True)

        # Button to generate and click event handler
        GenerateButton = gr.Button("Generate Video")
        GenerateButton.click(fn=generateVideo, inputs=[PromptField, SliderSteps], outputs=VideoPlayer, api_name="generate_video")

    with gr.Tab("Settings") as settings:
        def applysettings(SaveDir):
            SaveSettings = {
                "OutputDirectory" : SaveDir,
                }
            json.dumps()
        
        OutputDirectory = gr.Textbox(label="Output Directory", value=saveDirectory, interactive=True)
        ApplySettings = gr.Button("Apply Settings")
        ApplySettings.click(applysettings, inputs=[OutputDirectory])



WebUI.launch(debug=True)