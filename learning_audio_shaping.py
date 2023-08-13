# -*- coding: utf-8 -*-
import os
import numpy as np
from librosa.core.audio import resample
from wav_io import input_wav_file, output_wav_file
from edge_fading import fade_edge
from silence import change_length_edge_silence


class Settings:
    def __init__(self):
        self.amp_rate = 1.0  # リサンプリング時の波形倍率（オーバーフロー対策）
        self.length_fade_in = 50.0  # フェードインさせる長さ[msec]
        self.length_fade_out = 50.0  # フェードアウトさせる長さ[msec]
        self.length_start_silence = 50.0  # 開始の無音の長さ[msec]
        self.length_end_silence = 50.0  # 終了の無音の長さ[msec]
        self.output_samling_rate = 40000  # 出力wavのサンプリングレート[Hz]


def shape_wavs(input_dir_path, settings, output_dir_path):
    for file_name in os.listdir(input_dir_path):
        if not '.wav' in file_name:
            continue

        print('Start shaping: {}'.format(file_name))
        isr, wav = input_wav_file(input_dir_path + file_name, to_mono=True)

        amp = settings.amp_rate
        lfi = settings.length_fade_in
        lfo = settings.length_fade_out
        lss = settings.length_start_silence
        les = settings.length_end_silence
        osr = settings.output_samling_rate

        if not isr == osr:
            wav_f = amp * wav.astype(np.float64)
            wav = resample(wav_f, orig_sr=isr, target_sr=osr).astype(wav.dtype)
        fade_edge(osr, lfi, lfo, wav)
        wav = change_length_edge_silence(wav, osr, lss, les)
        output_wav_file(wav, osr, output_dir_path + file_name)


if __name__ == '__main__':
    input_dir_path = 'input/'
    output_dir_path = 'output/'
    settings = Settings()
    shape_wavs(input_dir_path, settings, output_dir_path)
