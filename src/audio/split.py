#Importing library and thir function
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
from ..config.config import Config
from ..files.names import get_brk_name
import click
from pathlib import Path



def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms


def trim_silence(sound):
    start_trim = detect_leading_silence(sound)
    end_trim = detect_leading_silence(sound.reverse())

    duration = len(sound)    
    return sound[start_trim:duration-end_trim]


def split_file_into_chunks(file_path, output_path, chunk_prefix):
   #reading from audio mp3 file
    sound = AudioSegment.from_file(file_path)
    # spliting audio files
    audio_chunks = split_on_silence(sound, min_silence_len=500, silence_thresh=-40 )
    
    base_name = os.path.basename(Config().get_value("CURRENT_DIRECTORY"))
    output_base = f"{output_path}/{base_name}"
    chunk_prefix = Path(file_path).stem

    if not os.path.exists(output_base):
        os.makedirs(output_base)
    output_folder = f"{output_base}/{chunk_prefix}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    #loop is used to iterate over the output list
    for i, chunk in enumerate(audio_chunks):
        output_file = f"{output_folder}/{chunk_prefix}_{i}.wav"
        print("Exporting file", output_file)
        trim_silence(chunk).export(output_file, format="wav")

def split_directory_into_chunks(target_directory, output_directory):
    for path, currentDirectory, files in os.walk(target_directory):
            for file in files:
                filename = os.path.join(path, file)
                click.echo(filename)
                split_file_into_chunks(filename, output_directory, filename)
