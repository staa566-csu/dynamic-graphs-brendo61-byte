import numpy as np
import os
import soothingsounds

from pathlib import Path

WHITE_NOISE_FILE = Path("white_noise.wav")
SAMPLE_DURATION = 10
RATE = 44100
BIT_DEPTH = 16


def generate_white_noise_file() -> None:
    """builds a white noise WAV file"""
    np_white_noise: np = soothingsounds.computenoise(ntype="white", fs=RATE, nsec=SAMPLE_DURATION, nbitfloat=BIT_DEPTH, nbitfile=1, verbose=True)
    soothingsounds.savenoise(samps=np_white_noise, nhours=0, fs=RATE, nsec=SAMPLE_DURATION, wavapi="scipy", ofn=WHITE_NOISE_FILE)


def check_white_noise_file_present() -> None:
    """checks if the while noise file is present. If not then make one"""

    if not WHITE_NOISE_FILE.exists():
        print("generating white noise file ...")
        generate_white_noise_file()
        print(f"... done. Saved at {str(WHITE_NOISE_FILE)}")


def play_white_noise() -> None:
    """plays white noise"""

    # wave_obj = simpleaudio.WaveObject.from_wave_file(str(WHITE_NOISE_FILE))
    # play_obj = wave_obj.play()
    # play_obj.wait_done()

    # if system is not happy with output source then this is a simple workaround. Will play to your system default output speakers.
    # tested on Mac. Not sure if it will work for Windows.
    os.system(f'open {str(WHITE_NOISE_FILE)}')
