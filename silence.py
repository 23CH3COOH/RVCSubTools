# -*- coding: utf-8 -*-
import numpy as np


def change_length_edge_silence(wav, sr, len_start_silence, len_end_silence):
    frames_start_silence = int(sr * float(len_start_silence) / 1000)
    frames_end_silence = int(sr * float(len_end_silence) / 1000)

    start_zeros = np.full(frames_start_silence, 0).astype(wav.dtype)
    end_zeros = np.full(frames_end_silence, 0).astype(wav.dtype)

    non_zero_inds = np.where(wav)[0]
    wav_cut_zero = wav[non_zero_inds[0]:1 + non_zero_inds[-1]]

    return np.hstack((start_zeros, wav_cut_zero, end_zeros))
