from pathlib import Path
import os


import click
import librosa
import numpy 
import soundfile as sf

from audioread.exceptions import NoBackendError

from ..config.config import Config
from ..files.directories import get_or_create_base

def _get_tempo_from_loaded_file(y, sr):
    tempo, beat_frame = librosa.beat.beat_track(y=y, sr=sr)
    return tempo

def _time_stretch_loaded_file(target_bpm, y, sr):
    current_bpm = _get_tempo_from_loaded_file(y, sr)
    click.echo(f"current {current_bpm} BPM")
    click.echo(f"BPM type {type(current_bpm)}")
    return librosa.effects.time_stretch(y, rate=target_bpm/current_bpm)

def get_tempo_from_file(file_path):
    y, sr = librosa.load(file_path)
    return _get_tempo_from_loaded_file(y=y, sr=sr)

def time_stretch_file(target_bpm, file_path, output_directory):
    y, sr = librosa.load(file_path)
    bpm_input = numpy.array([target_bpm]) 
    bpm_output = bpm_input.astype(numpy.float) 
    target_bpm = bpm_output[0]

    stretched_y = _time_stretch_loaded_file(target_bpm, y, sr)
    output_file_path = f"{output_directory}/{Path(file_path).stem}.wav"
    click.echo(f"Output path: {output_file_path}")

    sf.write(output_file_path, stretched_y, sr, 'PCM_24')


def time_stretch_directory(target_bpm, target_directory, output_directory):
    for path, currentDirectory, files in os.walk(target_directory):
            Config().set_value("CURRENT_DIRECTORY", path)
            base_output_directory = get_or_create_base(output_directory)
            for file in files:
                filename = os.path.join(path, file)
                click.echo(filename)
                try:
                    time_stretch_file(target_bpm, filename, base_output_directory)
                except NoBackendError:
                     click.echo(f"{filename} is not recognized as an audio file")
