# text-to-video-webui
Text-to-video-webui, inspired by @Oogabooga and @AUTOMATIC1111. Currently usable in it's current form without many customizations. 

# Installation
One click install supports only windows setup.

### Requires FFMPEG
  > Can be found at https://ffmpeg.org/download.html
  > I used the gyan.dev version. Extract ffmpeg.exe, ffprobe.exe and ffplay.exe to the root directory of text-to-video-webui

## Windows
  Click on the file setup.bat   

## Linux
  In the source directory of the text-to-video-webui
  Run python -m venv ./

  Then run
  pip install -r ./requirements.txt
 

# Usage

## Windows
  After setup.bat finishes click on start.bat

## Linux
  No clue, TODO

## Cross-platform
After starting the WebUI goto 127.0.0.1:7860 and your interface will be available. (No online support yet, it'll be added later).

The picture below is the layout of the interface you'll see.

![Picture of UI Interface](https://github.com/CharlesDowling/text-to-video-webui/assets/121833213/ff87e372-191d-478a-bc2b-a5378f7a97e4)

At the top of the WebUI is a drop down menu to select which model you would like to load and a button to make the program load your model. If the model is not installed the program will automatically install it when you go to load the model. (Currently there is a bug where after installing the model the drop down will still say it's not installed, it is and you can use it after it loads, refer to the console for more information.)

There are two main tabs at the top of the main program area: 
- Generation: Where you set up the prompt and some settings for the generation of the AI video
- Settings: This is the tab where you can adjust some settings. Currently there are only 2 settings, more to come.

Below those options are the Prompt & Negative Prompt text boxes, as well as the Video player:
- The Prompt text box are values you want to be included in your video.
- The Negative Prompt text box are values you do not want to be included in your video
- The Video Player Loads your video after generation. (Also currently bugged regarding framerate.)

At the bottom of the main program area are the Frame & Framerate Sliders and a Generate Video Button:
- The Frame slider determines how many frames should be in the video
- The framerate slider determines how quick the framerate should be
- The Generate Video Button...On second thought it's straight forwards...

# Roadmap
- [X]  Add settings tab - 10/08/2023
- [X]  Add optional save directory - 10/08/2023
- [X]  Finish requirements.txt - 10/08/2023
- [X]  Fix "Load Model" button - 10/08/2023
- [X]  Add option to load more models - 10/08/2023
- [X]  Windows Start bat - 10/08/2023
- [ ]  Windows ~~Run Bat &~~ start Ps1
- [ ]  Windows setup ps1
- [ ]  Linux Run & Setup .sh
- [ ]  Add CPU only support


# Acknowledgements
FFMPEG - Released under LGPL license 2 & GPL 2.1
