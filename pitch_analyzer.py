# -*- coding: utf-8 -*-
import numpy as np
import pyworld
from common import small_val


def small_val_to_nan(array):
    return np.where(array < small_val, np.nan, array)


def analyze_pitch(wav, sr, replace_zero_to_nan=True, method='harvest'):
    wav_f = wav.astype(np.float64)
    if method == 'dio':
        pitch_temp, time = pyworld.dio(wav_f, sr)
        pitch = pyworld.stonemask(wav_f, pitch_temp, time, sr)
    elif method == 'harvest':
        pitch, time = pyworld.harvest(wav_f, sr)
    else:
        raise Exception('Select dio or harvest.')

    if replace_zero_to_nan:
        return small_val_to_nan(pitch)
    else:
        return pitch
