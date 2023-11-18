# -*- coding: utf-8 -*-
import numpy as np
from wav_io import input_wav_file


# とりあえずモノラルのみ対応
def std_output_is_matching_two_wavs(wav_path_1, wav_path_2):
    wav_1 = input_wav_file(wav_path_1, return_type='wav_val')
    wav_2 = input_wav_file(wav_path_2, return_type='wav_val')
    frame_length_1 = wav_1.size
    frame_length_2 = wav_2.size
    print('Wav1 is {} frames.'.format(frame_length_1))
    print('Wav2 is {} frames.'.format(frame_length_2))
    if frame_length_1 == frame_length_2:
        if np.all(wav_1 == wav_2):
            print('Completely matching.')
        else:
            print('Different.')
    else:
        min_frame_length = min(frame_length_1, frame_length_2)
        if np.all(wav_1[:min_frame_length] == wav_2[:min_frame_length]):
            print('Common part is matching.')
        else:
            print('Different.')


if __name__ == '__main__':
    wav_path_1 = 'C:/Users/user_name/Downloads/test1.wav'
    wav_path_2 = 'C:/Users/user_name/Downloads/test2.wav'
    std_output_is_matching_two_wavs(wav_path_1, wav_path_2)
