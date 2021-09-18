sudo apt install ffmpeg
sudo apt install mkvtoolnix
sudo apt install timidity
sudo apt install fluid-soundfont-gm
sudo apt install python3-dev
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
