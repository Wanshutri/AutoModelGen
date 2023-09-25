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
required_libraries = ["colorama", "pydub", "requests"]
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

import requests

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download&confirm=1"

    session = requests.Session()

    response = session.get(URL, params={"id": id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


if len(sys.argv) >= 3:
        file_id = sys.argv[1]
        destination = sys.argv[2]
else:
    try:
        file_id = "1YvDKWBGg4KBkKkrrQ220Etm_0h3V812j"
        destination = os.getcwd()
        print(f"dowload {file_id} to {destination}")
        download_file_from_google_drive(file_id, destination)
    except PermissionError:
        if is_admin():
            print(f"{Fore.RED}{e}, , try moving the file to another path{Style.RESET_ALL}")
            input()
            exit(0)
        else:
            print("No admin privileges, restarting with privileges")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            exit(0)
    except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")
            input()
            exit(0)

'''
# downlad URL for the public file from google drive
#ffmpeg_compressed_url = "https://drive.google.com/file/d/1YvDKWBGg4KBkKkrrQ220Etm_0h3V812j/view?usp=drive_link"
ffmpeg_compressed_url = "https://drive.google.com/u/0/uc?id=1YvDKWBGg4KBkKkrrQ220Etm_0h3V812j&export=download"
# Path to save downloaded file
output_path = os.getcwd()

# Make request to download
response = requests.get(ffmpeg_compressed_url)

# Verificar si la descarga se completó correctamente
if response.status_code == 200:
    
    try:
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"ffmpeg downloaded in {output_path}")
    except PermissionError as e:
        if is_admin():
            print(f"{Fore.RED}{e}, , try moving the file to another path{Style.RESET_ALL}")
            input()
            exit(0)
        else:
            print("No admin privileges, restarting with privileges")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            exit(0)
    except:
        print(f"{Fore.RED}Can't download ffmpeg: " + e,{Style.RESET_ALL})
        input()
        exit(0)
else:
    print("Can't download ffmpeg.")
    input()
    exit(0)
'''
# Installing ffmpeg

ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")

if not os.path.exists(ffmpeg_dir):
    os.mkdir(ffmpeg_dir)

    ffmpeg_zip_path = os.path.join(os.getcwd(), ffmpeg_zip_name)

    if os.path.exists(ffmpeg_zip_path):
        try:
            with zipfile.ZipFile(ffmpeg_zip_path, "r") as zip_ref:
                zip_ref.extractall(ffmpeg_dir)
            print("FFmpeg has been extracted successfully.")
        except Exception as e:
            print(f"{Fore.RED}Error extracting FFmpeg: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}The FFmpeg ZIP file wasn't found in the project folder.{Style.RESET_ALL}")

try:
        os.environ["PATH"] += os.pathsep + os.path.abspath(ffmpeg_dir)
except Exception as e:
        print(f"{Fore.RED}Error adding FFmpeg to the PATH environment variable: {e}{Style.RESET_ALL}")

from pydub import AudioSegment
#Config ffmpeg
ffmpeg_path = './ffmpeg/bin'
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
