import os
import sys
import datetime
import time
import pyaudio

from multiprocessing import Process

from white_noise import check_white_noise_file_present, play_white_noise
from record import record_sample

OUT_FILE_DIR = "../speaker_samples"

OFF_AXIS_X = [-45, -30, -15, 0, 15, 30, 45]
OFF_AXIS_Y = [-45, -30, -15, 0, 15, 30, 45]


def ask_yes_no_question(message: str) -> bool:
    try:
        print(f"{message} (yes/no)")
        user_input = input("\n -> ")

        if user_input == "yes" or user_input[0] == "y":
            return True
        elif user_input == "no" or user_input[0] == "n":
            return False
        else:
            print("I did not understand that. Please try again.")
            return ask_yes_no_question(message=message)

    except RecursionError:
        print("Bad input too many times. Program exiting.")
        sys.exit()


def tell_user_off_axis(x_degree: int, y_degree: int) -> None:
    """asks the user where off-axis degree is being tested"""
    if not ask_yes_no_question(message=f"Place Speaker: X={x_degree}, y={y_degree} off axis. Ready?"):
        tell_user_off_axis(x_degree=x_degree, y_degree=y_degree)


def set_output_file_name(x_degree: int, y_degree: int) -> str:
    """returns the path to the sample will be saved to"""
    return os.path.join(OUT_FILE_DIR, f"{x_degree}_{y_degree}_{datetime.datetime.now().time()}")


def generate_samples(x_degree: int, y_degree: int) -> None:
    """generates a sample of speaker output"""
    tell_user_off_axis(x_degree=x_degree, y_degree=y_degree)
    output_file_name = set_output_file_name(x_degree=x_degree, y_degree=y_degree)

    play = Process(target=play_white_noise, args=())
    play.start()

    record_sample(save_file=output_file_name)

    play.join()

    time.sleep(2)
    print(" ... done")


def run():
    """runs sampling program"""
    print("Sample Gathering Program is starting. Press Ctrl+C to exit at any time.")

    try:
        check_white_noise_file_present()

        for y in OFF_AXIS_Y:
            for x in OFF_AXIS_X:
                generate_samples(x_degree=x, y_degree=y)

        print("All samples collected")
    except KeyboardInterrupt:
        print("User shutdown.")

    print("Program now exiting. Goodbye.")


if __name__ == '__main__':
    run()
