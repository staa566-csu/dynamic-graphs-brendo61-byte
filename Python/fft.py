import os

import pandas as pd
import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpck
import numpy
from math import log2

SAMPLE_FILE_DIR = "../speaker_samples"
OUTPUT_DIR = "../fft_data"


# s_rate, single = wavfile.read("./speaker_samples/center/0_degrees_18:27:15.513170.wav")
#
# FFT = abs(fftpck.fft(single))
# freqs = fftpck.fftfreq(len(FFT), 1.0 / s_rate)
#
# xs = freqs[range(len(FFT) // 2)][1:]
# ys = FFT[range(len(FFT) // 2)][1:]
#
# print(type(xs))


def preform_fft(sample_file: str) -> numpy.ndarray:
    """runs fft on sample_file"""
    s_rate, single = wavfile.read(sample_file)
    sample_fft = abs(fftpck.fft(single))
    return sample_fft[range(len(sample_fft) // 2)][1:]


def get_frequency_range(sample_file: str) -> numpy.ndarray:
    """returns frec range of sample"""

    s_rate, single = wavfile.read(sample_file)

    sample_fft = abs(fftpck.fft(single))
    freqs = fftpck.fftfreq(len(sample_fft), 1.0 / s_rate)

    return freqs[range(len(sample_fft) // 2)][1:]


def build_sample_store() -> dict:
    store = {}

    for sample in os.listdir(SAMPLE_FILE_DIR):
        x_y_tuple = get_sample_name(sample_file=sample)
        if not (entry := store.get(x_y_tuple)):
            store[x_y_tuple] = []
            entry = store[x_y_tuple]

        fft = preform_fft(sample_file=os.path.join(SAMPLE_FILE_DIR, sample))
        # fr = get_frequency_range(sample_file=os.path.join(SAMPLE_FILE_DIR, sample))
        entry.append(fft)

    return store


def get_sample_name(sample_file: str) -> tuple[str, str]:
    """gets the name of the sample"""
    split = sample_file.split("_")
    return split[0], split[1]


def avg_store(store: dict):
    for x_y_tuple, fft_list in store.items():
        store[x_y_tuple] = sum(fft_list) / (len(fft_list) - 1)


def convert_to_db(store: dict):
    for x_y_tuple, fft_list in store.items():
        store[x_y_tuple] = (log2((((sum(fft_list) ** 0.5) / 1000) ** 2) / 90) * 3) + 87


def convert_to_dict_list(store: dict):
    x = []
    y = []
    db = []

    for x_y_tuple, db_ in store.items():
        x_, y_ = x_y_tuple
        x.append(x_)
        y.append(y_)
        db.append(db_)

    return {"x": x, "y": y, "db": db}


def convert_db_for_num_matrix_in_r(dict_for_df: dict, store: dict):
    xs = set(sorted(dict_for_df.get("x")))
    ys = set(sorted(dict_for_df.get("y")))

    data = []
    for x in xs:
        temp = []
        for y in ys:
            temp.append(store[(x, y)])

        data.append(temp)

    df = pd.DataFrame(data)
    return df


def save_df_as_csv(df: pd.DataFrame, save_file: str):
    """saves a dataframe to csv file"""
    df.to_csv(path_or_buf=save_file)


def run_fft():
    """runs fft on all speaker samples"""
    store = build_sample_store()
    avg_store(store=store)
    convert_to_db(store=store)
    dict_for_df = convert_to_dict_list(store=store)
    df2 = convert_db_for_num_matrix_in_r(dict_for_df=dict_for_df, store=store)

    df = pd.DataFrame.from_dict(dict_for_df)

    save_df_as_csv(df=df, save_file="speaker_data.csv")
    save_df_as_csv(df=df2, save_file="db_levels.csv")


if __name__ == '__main__':
    run_fft()
