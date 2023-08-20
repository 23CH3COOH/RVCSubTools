# -*- coding: utf-8 -*-
import os
import pandas as pd
from wav_io import input_wav_file, output_wav_file
from common import small_val, insert_index, insert_label


# MM:SS.SSSの文字列を秒数のfloatに直す（文字列に0埋め不要）
def to_seconds(time_str):
    try:
        if ':' in time_str:
            strs = time_str.split(':')
            return 60 * int(strs[0]) + float(strs[1])
        else:
            return float(time_str)
    except:
        print('Invalid time string: {}'.format(time_str))
        assert False


def get_times(input_csv_path):
    df = pd.read_csv(input_csv_path)
    start_times = [to_seconds(time_str) for time_str in df['Start']]
    end_times = [to_seconds(time_str) for time_str in df['End']]
    return start_times, end_times


# 同名のwavファイルとcsvファイルがセットで入っている必要がある
def split_and_output_wavs(input_dir_path, output_dir_path):
    input_file_names = os.listdir(input_dir_path)

    for wav_name in input_file_names:
        if not '.wav' in wav_name:
            continue
        csv_name = wav_name.replace('.wav', '.csv')
        if not csv_name in input_file_names:
            print('Warning: Not exist {}'.format(csv_name))
            continue

        print('Start splitting: {}'.format(wav_name))
        sr, wav = input_wav_file(input_dir_path + wav_name, to_mono=False)
        start_times, end_times = get_times(input_dir_path + csv_name)

        for i, time in enumerate(zip(start_times, end_times)):
            start_frame = int(small_val + sr * time[0])
            end_frame = int(small_val + sr * time[1])
            wav_cut = wav[start_frame:end_frame]
            if wav_cut.ndim > 1:
                assert wav_cut.ndim == 2
                assert wav_cut.shape[1] == 2
                name = insert_index(insert_label(wav_name, 'L'), i, digit=2)
                output_wav_file(wav_cut[:, 0], sr, output_dir_path + name)
                name = insert_index(insert_label(wav_name, 'R'), i, digit=2)
                output_wav_file(wav_cut[:, 1], sr, output_dir_path + name)
            else:
                name = insert_index(wav_name, i)
                output_wav_file(wav_cut, sr, output_dir_path + name)


if __name__ == '__main__':
    input_dir_path = 'input/'
    output_dir_path = 'output/'
    split_and_output_wavs(input_dir_path, output_dir_path)
