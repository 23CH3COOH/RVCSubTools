# -*- coding: utf-8 -*-
import os
import numpy as np
from pitch_analyzer import analyze_pitch
from wav_io import input_wav_file


def calc_mean_pitch_variation(input_dir_path):
    for file_name in os.listdir(input_dir_path):
        if not '.wav' in file_name:
            continue

        sr, wav = input_wav_file(input_dir_path + file_name, to_mono=True)
        pitch = analyze_pitch(wav, sr)
        pitch_log = 12 * np.log2(pitch / 440)
        diff_abs = np.abs(np.diff(pitch_log))
        total_pitch_variation = np.nansum(diff_abs)
        available_shifts = np.count_nonzero(np.isfinite(diff_abs))
        available_sec = '{}[sec]'.format(0.005 * available_shifts)
        mean_pitch_variation = total_pitch_variation / available_shifts
        print(file_name, available_sec, mean_pitch_variation)


if __name__ == '__main__':
    input_dir_path = 'input/'
    calc_mean_pitch_variation(input_dir_path)
