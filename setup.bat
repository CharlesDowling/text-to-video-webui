call python -m venv ./venv
call /venv/scripts/activate.bat
call pip3 install torch==2.0.1+cu118 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
call pip3 install -r ./requirements.txt
pause