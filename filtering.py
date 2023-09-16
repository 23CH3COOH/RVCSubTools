# -*- coding: utf-8 -*-
import os
import librosa
import numpy as np
from graph_filtering_result import output_graph
from pitch_analyzer import analyze_pitch
from wav_io import input_wav_file, output_wav_file


class Settings:
    def __init__(self):
        self.sr = 44100
        self.win_frames = 4410
        self.shift_frames = 441
        self.window = 'hann'


def get_pitch(input_wav_path):
    sr, wav = input_wav_file(input_wav_path, to_mono=True)
    return analyze_pitch(wav, sr)


# フーリエ変換後の1時刻分の周波数軸配列に対して乗算する係数配列を求める
def make_filtering_operator_onetime(pitch, base_hz, freq_dims):
    res = np.full(freq_dims, 1.0)
    if np.isnan(pitch):
        return res
    for i in range(freq_dims):
        freq = base_hz * i
        if freq < pitch:
            continue
        res[i] = 0.5 + 0.5 * np.cos(2 * np.pi * (freq - pitch) / pitch)
    return res


# フーリエ変換後の（周波数軸×時間軸）の2次元配列に対して乗算する係数配列を求める
def make_filtering_operator(pitch, settings):
    class IndexConverter:
        def __init__(self, pitch_shifts, fourier_shifts):
            self.__p = pitch_shifts
            self.__f = fourier_shifts

        def to_pitch_index(self, fourier_index):
            assert 0 <= fourier_index and fourier_index < self.__f
            r = float(fourier_index) / float(self.__f - 1)
            return int(r * (self.__p - 1))

    freq_dims = 1 + settings.win_frames // 2
    # rate: ピッチ取得時のシフト長さ÷フーリエ変換時のシフト長さ
    rate = 0.005 * settings.sr / settings.shift_frames
    shift_su = int((pitch.shape[0] - 1) * rate) + 1

    ic = IndexConverter(pitch.shape[0], shift_su)
    res = np.full((freq_dims, shift_su), 1.0)
    for i in range(shift_su):
        res[:, i] = make_filtering_operator_onetime(
            pitch[ic.to_pitch_index(i)],
            settings.sr / settings.win_frames,
            freq_dims)
    return res


# 非整数次倍音の成分を減らす
def reduce_inharmonic_partials(input_wav_path, settings, output_wav_path):
    if not os.path.exists(input_wav_path):
        print('Not Exist: {}'.format(input_wav_path))
        return

    wav, sr = librosa.load(input_wav_path, sr=settings.sr, mono=True)
    # フーリエ変換時のシフト長さの倍数に調節し、未満は切り捨てる
    wav = wav[:(wav.size // settings.win_frames) * settings.win_frames]
    F = librosa.stft(wav,
                     n_fft=settings.win_frames,
                     win_length=settings.win_frames,
                     hop_length=settings.shift_frames,
                     window=settings.window)
    pitch = get_pitch(input_wav_path)
    filtering = make_filtering_operator(pitch, settings)

    logmsg_fmt = '[DEBUG] Time Counts: pitch {}, stft {}, stft_filtered {}'
    print(logmsg_fmt.format(pitch.shape[0], F.shape[1], filtering.shape[1]))
    assert F.shape == filtering.shape

    F_fil = F * filtering
    wav_fil = librosa.istft(F_fil,
                            win_length=settings.win_frames,
                            hop_length=settings.shift_frames,
                            window=settings.window)

    logmsg_fmt = '[DEBUG] Wav Frames: original {}, filtered {}'
    print(logmsg_fmt.format(wav.shape[0], wav_fil.shape[0]))
    output_wav_file(wav_fil, sr, output_wav_path)
    output_path_without_ext = output_wav_path.replace('.wav', '')
    output_graph(wav, pitch, F, F_fil, settings, output_path_without_ext)


if __name__ == '__main__':
    settings = Settings()
    input_wav_path = 'input/test.wav'
    output_wav_path = 'output/test_conv.wav'
    reduce_inharmonic_partials(input_wav_path, settings, output_wav_path)
