# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np
from pitch_analyzer import analyze_pitch
from wav_io import input_wav_file


class MusicalScaleDivider:
    def __init__(self):
        self.__min_steps_from_A4 = -17
        self.__step_size = 30
        self.__scales = ['E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3',
                         'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4',
                         'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5',
                         'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5']
        assert len(self.__scales) == self.__step_size
        self.__seconds = [0.0 for i in range(self.__step_size)]

    def add_pitch(self, pitch, seconds_per_frame=0.005):
        for v in pitch:
            if np.isnan(v):
                continue
            steps_from_A4 = 12 * np.log2(v / 440)
            index = int((-1) * self.__min_steps_from_A4 + 0.5 + steps_from_A4)
            if index < 0:
                index = 0
            if index >= self.__step_size:
                index = self.__step_size - 1
            self.__seconds[index] += seconds_per_frame

    def get_scales(self):
        return self.__scales

    def get_seconds(self):
        return self.__seconds


def output_graph(scales, seconds, dir_path, adding_label):
    size = len(scales)
    assert len(seconds) == size

    plt.figure(figsize=(19.2, 10.8)) 
    plt.xlabel('pitch')
    plt.ylabel('seconds')
    title_str = 'Pitch Distribution {}'.format(adding_label)
    desc_str = 'Total: {:.3f}[sec]'.format(np.sum(np.array(seconds)))
    plt.title(title_str + '\n' + desc_str)

    plt.bar(np.arange(size), seconds, width=0.8, tick_label=scales)
    # 保存直前にplt.show()すると保存しても中身が描かれない模様
    file_path = dir_path + 'pitch_distribution_{}.png'.format(adding_label)
    if os.path.exists(file_path):
        print('Already Exist: {}'.format(file_path))
    else:
        plt.savefig(file_path)


def output_pitch_distribution(input_dir_path, output_dir_path, adding_label):
    msd = MusicalScaleDivider()

    for file_name in os.listdir(input_dir_path):
        if not '.wav' in file_name:
            continue

        print('Start analyzing pitch: {}'.format(file_name))
        sr, wav = input_wav_file(input_dir_path + file_name, to_mono=True)
        pitch = analyze_pitch(wav, sr)
        msd.add_pitch(pitch, seconds_per_frame=0.005)

    scales = msd.get_scales()
    seconds = msd.get_seconds()
    output_graph(scales, seconds, output_dir_path, adding_label)


if __name__ == '__main__':
    input_dir_path = 'input/'
    output_dir_path = 'output/'
    adding_label = 'Test'
    output_pitch_distribution(input_dir_path, output_dir_path, adding_label)
