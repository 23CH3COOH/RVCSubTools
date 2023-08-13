# -*- coding: utf-8 -*-
import numpy as np


def fade_edge(sr, length_fade_in, length_fade_out, wav):
    frames_fade_in = int(sr * float(length_fade_in) / 1000)
    frames_fade_out = int(sr * float(length_fade_out) / 1000)

    if wav.size < frames_fade_in + frames_fade_out:
        rate = float(wav.size) / (frames_fade_in + frames_fade_out)
        frames_fade_in = int(rate * frames_fade_in)
        frames_fade_out = int(rate * frames_fade_out)

    op_fade_in = np.linspace(0.0, 1.0, frames_fade_in).astype(np.float64)
    wav_fi = (op_fade_in * wav[:frames_fade_in]).astype(wav.dtype)
    wav[:frames_fade_in] = wav_fi

    op_fade_out = np.linspace(1.0, 0.0, frames_fade_out).astype(np.float64)
    wav_fo = (op_fade_out * wav[(-1) * frames_fade_out:]).astype(wav.dtype)
    wav[(-1) * frames_fade_out:] = wav_fo


if __name__ == '__main__':
    arr = np.full(20, 64).astype(np.int16)
    fade_edge(1000, 5, 8, arr)
    print(arr)  # [ 0 16 32 48 64 64 64 64 64 64 64 64 64 54 45 36 27 18  9  0]
