# -*- coding: utf-8 -*-
import os
import numpy as np
from wav_io import input_wav_file, output_wav_file


def change_wavs_amp(input_dir_path, amp_rate, output_dir_path):
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    for file_name in os.listdir(input_dir_path):
        if not '.wav' in file_name:
            continue

        print('Start changing amp rate: {}'.format(file_name))
        sr, wav = input_wav_file(input_dir_path + file_name, to_mono=False)
        wav_amp = (amp_rate * wav.astype(np.float64)).astype(wav.dtype)
        output_wav_file(wav_amp, sr, output_dir_path + file_name)


if __name__ == '__main__':
    input_dir_path = 'input/'
    output_dir_path = 'output/'
    change_wavs_amp(input_dir_path, 0.5, output_dir_path)
