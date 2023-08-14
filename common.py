# -*- coding: utf-8 -*-


small_val = 0.0001


def insert_index(file_name, index, digit=3):
    if digit == 3:
        return file_name.replace('.wav', '') + '_{:03d}.wav'.format(index)
    else:
        return file_name.replace('.wav', '') + '_{:02d}.wav'.format(index)


def insert_label(file_name, label):
    return file_name.replace('.wav', '') + '_{}.wav'.format(label)
