import subprocess
import os
import ctypes
import sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

os.system('cls')

#Installation of requried libraries
print("Installing required libraries")
required_libraries = ["colorama", "pydub", "requests", "gdown"]
act_req = ""

try:
    
    for req in required_libraries:
        actReq = req
        subprocess.check_call(["pip", "install", req])
except Exception as e:
    print(f"Can't install the library {actReq}: \nError {e}")
    input()
    exit(0)
from colorama import Fore, Style
import os
import zipfile
import platform

# Verify windows is 64 bits for installing ffmpeg
is_64bit = platform.architecture()[0] == "64bit"

if (is_64bit):
    ffmpeg_zip_name = "ffmpeg.zip"
else:
    input("Can't install ffmpeg in a 32 bits system")
    exit(0)

# Installing ffmpeg

ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")

if not os.path.exists(ffmpeg_dir):
    os.mkdir(ffmpeg_dir)

    import gdown
    url = 'https://drive.google.com/file/d/1YvDKWBGg4KBkKkrrQ220Etm_0h3V812j/view'
    output_path = 'ffmpeg.zip'
    gdown.download(url, output_path, quiet=False,fuzzy=True)

    ffmpeg_zip_path = os.path.join(os.getcwd(), ffmpeg_zip_name)

    if os.path.exists(ffmpeg_zip_path):
        try:
            with zipfile.ZipFile(ffmpeg_zip_path, "r") as zip_ref:
                zip_ref.extractall(os.getcwd())
            print("FFmpeg has been extracted successfully.")
            os.remove('ffmpeg.zip')
        except Exception as e:
            print(f"{Fore.RED}Error extracting FFmpeg: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}The FFmpeg ZIP file wasn't found in the project folder.{Style.RESET_ALL}")
ffmpeg_zip_path = os.path.join(os.getcwd(), ffmpeg_zip_name)
if os.path.exists(ffmpeg_zip_path):
    os.remove('ffmpeg.zip')
try:
        os.environ["PATH"] += os.pathsep + os.path.abspath(ffmpeg_dir)
except Exception as e:
        print(f"{Fore.RED}Error adding FFmpeg to the PATH environment variable: {e}{Style.RESET_ALL}")

from pydub import AudioSegment
#Config ffmpeg
ffmpeg_path = './ffmpeg/ffmpeg/'
AudioSegment.ffmpeg = ffmpeg_path + 'ffmpeg.exe'
AudioSegment.ffprobe = ffmpeg_path + 'ffprobe.exe'

#Asks for the input audio PATH and get output folder
audio_file = str(input("Insert the path to the audio file to convert into model >>")).strip()
print(f"{Fore.YELLOW}Warning!, if the path doesn't exist it will be created, if it exists make sure it's empty{Style.RESET_ALL}")
output_path = os.path.join(os.getcwd(), "output")

if not os.path.exists(output_path):
    os.makedirs(output_path)

from pydub.silence import split_on_silence

print("Now the audio will be processing")

audio = AudioSegment.from_file(audio_file)

audio_with_sound = split_on_silence(audio, silence_thresh=-36, keep_silence=True)

for i, part in enumerate(audio_with_sound):
    output_file = f"{output_path}/parte_{i+1}.wav"
    part.export(output_file, format="wav")

print("Processing completed. Sound parts have been saved as separate files.")
