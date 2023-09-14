# -*- coding: utf-8 -*-
import numpy as np
import pyworld
from common import small_val


def small_val_to_nan(array):
    return np.where(array < small_val, np.nan, array)


def analyze_pitch(wav, sr, replace_zero_to_nan=True):
    wav_f = wav.astype(np.float64)
    pitch_temp, time = pyworld.dio(wav_f, sr)
    if replace_zero_to_nan:
        return small_val_to_nan(pyworld.stonemask(wav_f, pitch_temp, time, sr))
    else:
        return pyworld.stonemask(wav_f, pitch_temp, time, sr)
