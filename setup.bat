call python -m venv ./
call scripts/activate.bat
call pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
call pip3 install -r ./requirements.txt
pause