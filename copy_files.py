# -*- coding: utf-8 -*-
import os
import shutil


def add_extension(file_name, extension='.wav'):
    if extension in file_name:
        return file_name
    else:
        return file_name + extension


def get_file_names(list_file_path):
    f = open(list_file_path, 'r')
    rows = f.readlines()
    f.close()
    return [add_extension(row.strip()) for row in rows]


def copy_files(input_dir_path, list_file_path, output_dir_path):
    file_names = get_file_names(list_file_path)
    for file_name in file_names:
        if os.path.exists(input_dir_path + file_name):
            print('Start copy: {}'.format(file_name))
            shutil.copy2(input_dir_path + file_name, output_dir_path)
        else:
            print('Not exist: {}'.format(file_name))


if __name__ == '__main__':
    input_dir_path = 'input/wav/'
    list_file_path = 'input/file_list.txt'
    output_dir_path = 'output/'
    copy_files(input_dir_path, list_file_path, output_dir_path)
