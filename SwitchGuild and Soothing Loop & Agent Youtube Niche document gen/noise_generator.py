import numpy as np
from pydub import AudioSegment
from pydub.playback import play
from scipy.signal import lfilter

def generate_white_noise(duration_ms, volume_db):
    samples = np.random.uniform(-1, 1, int(duration_ms / 1000 * 44100)).astype(np.float32)
    # Convert to int16 for pydub compatibility
    samples_int16 = (samples * 32767).astype(np.int16)
    audio = AudioSegment(samples_int16.tobytes(), frame_rate=44100, sample_width=2, channels=1)
    return audio + volume_db

def generate_pink_noise(duration_ms, volume_db):
    # From https://github.com/python-acoustics/python-acoustics/blob/master/acoustics/signal.py
    samples = np.random.uniform(-1, 1, int(duration_ms / 1000 * 44100)).astype(np.float32)
    # This is a simple approximation. More accurate methods exist.
    b = np.array([0.049922035, -0.095993537, 0.050612699, -0.004408786])
    a = np.array([1.0, -2.494956002, 2.017265875, -0.522189496])
    y = lfilter(b, a, samples)
    y = y / np.max(np.abs(y)) * 0.9 # Normalize
    # Convert to int16 for pydub compatibility
    y_int16 = (y * 32767).astype(np.int16)
    audio = AudioSegment(y_int16.tobytes(), frame_rate=44100, sample_width=2, channels=1)
    return audio + volume_db

def generate_brown_noise(duration_ms, volume_db):
    # From https://github.com/python-acoustics/python-acoustics/blob/master/acoustics/signal.py
    samples = np.random.uniform(-1, 1, int(duration_ms / 1000 * 44100)).astype(np.float32)
    # This is a simple approximation. More accurate methods exist.
    b = np.array([0.05635, -0.04996, 0.02119, -0.00374])
    a = np.array([1.0, -1.57000, 0.64120, -0.07190])
    y = lfilter(b, a, samples)
    y = y / np.max(np.abs(y)) * 0.9 # Normalize
    # Convert to int16 for pydub compatibility
    y_int16 = (y * 32767).astype(np.int16)
    audio = AudioSegment(y_int16.tobytes(), frame_rate=44100, sample_width=2, channels=1)
    return audio + volume_db

if __name__ == "__main__":
    duration = 5000 # milliseconds
    volume = -10 # dB

    print("Generating white noise...")
    white_noise = generate_white_noise(duration, volume)
    white_noise.export("white_noise.wav", format="wav")
    print("White noise saved to white_noise.wav")

    print("Generating pink noise...")
    pink_noise = generate_pink_noise(duration, volume)
    pink_noise.export("pink_noise.wav", format="wav")
    print("Pink noise saved to pink_noise.wav")

    print("Generating brown noise...")
    brown_noise = generate_brown_noise(duration, volume)
    brown_noise.export("brown_noise.wav", format="wav")
    print("Brown noise saved to brown_noise.wav")

    # You can uncomment these lines to play the generated sounds (requires ffplay installed)
    # print("Playing white noise...")
    # play(white_noise)
    # print("Playing pink noise...")
    # play(pink_noise)
    # print("Playing brown noise...")
    # play(brown_noise)


