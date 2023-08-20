# -*- coding: utf-8 -*-
import os
import csv
import pytesseract
from PIL import Image, ImageGrab


'''
[tesseractの導入に関するメモ]
tesseractをpythonで使用するには、pytesseractをpipでインストールするだけでは不可。
'https://github.com/UB-Mannheim/tesseract/wiki' からtesseractをダウンロードし、
格納されたtesseract.exeのパスをtesseract_cmdに指定しなければならない。
'''


tesseract_path = '../../../AppData/Local/Programs/Tesseract-OCR/tesseract.exe'


'''
start_time_boxの範囲に映る開始時刻とend_time_boxの範囲に映る終了時刻の
画像キャプチャから開始時刻と終了時刻の値を認識し、指定CSVファイルの新行に追記する。
画面キャプチャで得られる時刻フォーマットはとりあえずH:MM:SS.SSSを前提とする。
開始時刻と終了時刻は必ず画面に映っている必要があり、隠れてはいけない。
'''
def recognize_time_range(start_time_box, end_time_box, adding_csv_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    temp_image_path = 'temp.jpg'

    # 一旦画像ファイルに出力してからそのファイルを読み込む方法でないと
    # 時刻文字列を正しく認識できない模様
    temp_image_start_time = ImageGrab.grab(bbox=start_time_box)
    temp_image_start_time.save(temp_image_path)
    image_start_time = Image.open(temp_image_path)
    start_time_hms = pytesseract.image_to_string(image_start_time).strip()
    start_time_ms = start_time_hms[2:]
    print('Start time {}'.format(start_time_ms))

    temp_image_end_time = ImageGrab.grab(bbox=end_time_box)
    temp_image_end_time.save(temp_image_path)
    image_end_time = Image.open(temp_image_path)
    end_time_hms = pytesseract.image_to_string(image_end_time).strip()
    end_time_ms = end_time_hms[2:]
    print('End time   {}'.format(end_time_ms))

    if not os.path.exists(adding_csv_path):
        with open(adding_csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Start', 'End'])
    # newline=''を指定しないと余分な改行が出力されてしまう
    with open(adding_csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([start_time_ms, end_time_ms])
    os.remove(temp_image_path)


if __name__ == '__main__':
    start_time_box = (292, 156, 364, 176)
    end_time_box = (392, 156, 464, 176)
    adding_csv_path = 'output/test.csv'
    recognize_time_range(start_time_box, end_time_box, adding_csv_path)
