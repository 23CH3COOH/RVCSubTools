# -*- coding: utf-8 -*-
import pandas as pd


def shift_time(time_str, sec):
    minites = int(time_str[0:2])
    seconds = int(time_str[3:5])
    mill_seconds = int(time_str[6:9])
    total_seconds = 60.0 * minites + seconds + 0.001 * mill_seconds
    shifted = total_seconds + sec
    minites = int(shifted / 60.0)
    seconds = int(shifted - 60.0 * minites)
    mill_seconds = int(1000 * (shifted - 60.0 * minites - seconds) + 0.001)
    return '{:02d}:{:02d}.{:03d}'.format(minites, seconds, mill_seconds)


def output_shifted_times(input_file_path, output_file_path, sec):
    df = pd.read_csv(input_file_path)
    df['Start'] = [shift_time(time_str, sec) for time_str in df['Start']]
    df['End'] = [shift_time(time_str, sec) for time_str in df['End']]
    df.to_csv(output_file_path, index=False)


if __name__ == '__main__':
    output_shifted_times('input/test_song.csv', 'output/test_song.csv', -0.180)
