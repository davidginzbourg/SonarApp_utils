import json
import numpy as np
import matplotlib.pyplot as plt

CHIRP_DURATION = 0.01
SAMPLE_RATE = 44100
F_START = 4000
F_END = 8000
JAVA_SHORT_MAX = 32767


def get_chirp():
    k = (F_END - F_START) / CHIRP_DURATION
    chirp_size = int(np.ceil(CHIRP_DURATION * SAMPLE_RATE)) + 1
    chirp = np.ndarray(shape=(chirp_size,))
    inc = 1.0 / SAMPLE_RATE
    t = 0.0
    for i in range(len(chirp)):
        if t > CHIRP_DURATION:
            break
        chirp[i] = np.sin(2.0 * np.pi * (F_START * t + 0.5 * k * t ** 2))
        t += inc

    chirp *= np.hanning(len(chirp))
    return chirp * np.full((chirp_size,), JAVA_SHORT_MAX)


def show_cross_correlation(number):
    ccorrelation_file = 'samples/cross_correlation_of_' + str(number)
    with open(ccorrelation_file, 'r') as f:
        data = json.load(f)['data']
    y = list(float(n) for n in data)
    y = y[:len(y) / 2]
    return get_graph_figure(y, ccorrelation_file)


def show_recording(number):
    recording_file = 'samples/recording_of_' + str(number)
    with open(recording_file, 'r') as f:
        data = json.load(f)['data']
    y = list(int(n) for n in data)
    argmax = np.argmax(y)
    start_y = max(int(np.floor(argmax - CHIRP_DURATION * SAMPLE_RATE * 0.5)),
                  0)
    y = y[start_y:]
    return get_graph_figure(y, recording_file)


def get_graph_figure(y, title):
    x = list(range(len(y)))

    plt.grid(True, axis='y')
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlabel('Sample #')
    ax.set_ylabel('Amplitude')
    ax.set_title(title)
    ax.plot(x, y)
    return fig
