# -*- coding: utf-8 -*-
import os
import librosa
import numpy as np
from sys import float_info
from graph_frequency_result import output_transition, output_one_time
from wav_io import input_wav_file


class Settings:
    def __init__(self):
        self.sr = 44100
        self.win_frames = 4410
        self.shift_frames = 441
        self.window = 'hann'
        self.start_sec = 0.0
        self.end_sec = float_info.max


# 両方モノラルと両方ステレオに対応
def cut_wav(wav_1, wav_2, start_sec, end_sec, sr):
    start_frame = max(int(sr * start_sec), 0)
    end_frame = int(min(sr * end_sec, wav_1.shape[0], wav_2.shape[0]))
    if wav_1.ndim == 1 and wav_2.ndim == 1:
        wav_1 = wav_1[start_frame:end_frame]
        wav_2 = wav_2[start_frame:end_frame]
    elif wav_1.ndim == 2 and wav_2.ndim == 2:
        wav_1 = wav_1[:, start_frame:end_frame]
        wav_2 = wav_2[:, start_frame:end_frame]
    else:
        print('Mixed stereo and mono.')
        assert False


def output(wav_path_1, wav_path_2, settings, name_1, name_2, output_dir_path):
    wav_1, _ = librosa.load(wav_path_1, sr=settings.sr, mono=False)
    wav_2, _ = librosa.load(wav_path_2, sr=settings.sr, mono=False)
    cut_wav(wav_1, wav_2, settings.start_sec, settings.end_sec, settings.sr)
    # とりあえずステレオでも片側チャンネルのみ
    if wav_1.ndim == 2:
        wav_1 = wav_1[0, :]
    if wav_2.ndim == 2:
        wav_2 = wav_2[0, :]

    F_1 = librosa.stft(wav_1,
                       n_fft=settings.win_frames,
                       win_length=settings.win_frames,
                       hop_length=settings.shift_frames,
                       window=settings.window)
    F_2 = librosa.stft(wav_2,
                       n_fft=settings.win_frames,
                       win_length=settings.win_frames,
                       hop_length=settings.shift_frames,
                       window=settings.window)
    db_1 = librosa.amplitude_to_db(np.abs(F_1), ref=np.max)
    db_2 = librosa.amplitude_to_db(np.abs(F_2), ref=np.max)
    assert db_1.ndim == 2 and db_2.ndim == 2
    ave_db_1 = np.average(db_1, axis=1)
    ave_db_2 = np.average(db_2, axis=1)

    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    file_path = output_dir_path + 'transition.png'
    output_transition(db_1, db_2, settings, name_1, name_2, file_path)
    file_path = output_dir_path + 'time_average.png'
    output_one_time(ave_db_1, ave_db_2, settings, name_1, name_2, file_path)


if __name__ == '__main__':
    settings = Settings()
    wav_path_1 = 'input/test1.wav'
    wav_path_2 = 'input/test2.wav'
    name_1 = 'original'
    name_2 = 'converted'
    output_dir_path = 'output/test/'
    output(wav_path_1, wav_path_2, settings, name_1, name_2, output_dir_path)
