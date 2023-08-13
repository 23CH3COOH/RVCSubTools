# -*- coding: utf-8 -*-
# 【参考ページ】Pythonを用いた発話分割【AIボイスチェンジャーの学習で役立つ】
import os
import librosa
from pydub import AudioSegment
from pydub.silence import split_on_silence


'''
min_silence_len: 無音の最小長さ[msec]
silence_thresh: 無音と判断する音量閾値[dBFS]
※以下のRuntimeWarningが出てくるが特に問題ない模様:
'Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work'
'''
def split_wav(input_wav_path, min_silence_len=200, silence_thresh=-40):
    audio, sr = librosa.load(input_wav_path, sr=None)
    # 音声ファイルの長さを取得
    duration = librosa.get_duration(y=audio, sr=sr)
    # pydub用にAudioSegmentオブジェクトに変換
    audio_segment = AudioSegment.from_wav(input_wav_path)
    # 音声ファイルを発話単位に分割
    chunks = split_on_silence(
        audio_segment,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    return chunks


def insert_index(file_name, index):
    return file_name.replace('.wav', '') + '_{:03d}.wav'.format(index)


'''
指定フォルダにあるwavファイルそれぞれを発話分割して出力する
※サンプリング周波数とビット数は同じに保たれる
'''
def split_and_output_wavs(input_dir_path, output_dir_path):
    for input_file_name in os.listdir(input_dir_path):
        if not '.wav' in input_file_name:
            continue
        print('Start splitting: {}'.format(input_file_name))
        chunks = split_wav(input_dir_path + input_file_name)
        # 分割した発話を個別のファイルに保存
        for i, chunk in enumerate(chunks):
            output_file_name = insert_index(input_file_name, i)
            chunk.export(output_dir_path + output_file_name, format='wav')


if __name__ == '__main__':
    input_dir_path = 'input/'
    output_dir_path = 'output/'
    split_and_output_wavs(input_dir_path, output_dir_path)
