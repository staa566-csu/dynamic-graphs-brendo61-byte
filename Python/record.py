import wave
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
BIT_DEPTH = 16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 0.1


def record_sample(save_file: str) -> None:
    """records the sample"""

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    for i in range(30):
        stream.start_stream()
        save_to = f"{save_file}_{i}.wav"

        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()

        wf = wave.open(save_to, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f"... {i} saved")

        stream.stop_stream()

    stream.close()
    p.terminate()
