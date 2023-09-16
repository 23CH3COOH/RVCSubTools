# -*- coding: utf-8 -*-
import librosa
import matplotlib.pyplot as plt
import numpy as np


def output_graph_5sec(wav, pitch, F, F_fil, settings, output_png_path, count):
    def repeat_to_wav_size(ar):
        shifts = 0.005 * settings.sr
        return np.array([ar[int(float(i) / shifts)] for i in range(wav.size)])

    fig = plt.figure(figsize=(19.2, 9.6))
    #plt.title(os.path.basename(output_png_path).replace('.png', ''))

    ax1 = fig.add_subplot(3, 1, 1)
    #ax1.subplots_adjust(left=0, right=0.8, bottom=0, top=1)
    xticks = np.arange(0, 1 + wav.size, int(0.5 * settings.sr))
    ax1.set_xlim(0, wav.size)
    ax1.set_xticks(xticks, 5.0 * count + xticks / float(settings.sr))
    ax1.set_xlabel('Time [sec]')
    ax1.set_ylim(-1.0, 1.0)
    ax1.grid()
    ax1.plot(wav, linewidth=0.1, color='blue')

    ax1r = ax1.twinx()
    yticks = [np.log2(440) + float(i) / 4 for i in range(-5, 4)]
    yticks_note = ['F#3', 'A3', 'C4', 'D#4', 'F#4', 'A4', 'C5', 'D#5', 'F#5']
    ax1r.set_ylim(yticks[0], yticks[-1])
    ax1r.set_yticks(yticks, yticks_note)
    ax1r.set_ylabel('pitch')
    ax1r.grid()
    ax1r.plot(repeat_to_wav_size(np.log2(pitch)), linewidth=1.0, color='red')

    hop = settings.shift_frames
    sr = settings.sr
    draw = librosa.display.specshow

    ax2 = fig.add_subplot(3, 1, 2)
    logF = librosa.amplitude_to_db(np.abs(F), ref=np.max)
    draw(logF, hop_length=hop, sr=sr, x_axis='time', y_axis='hz', ax=ax2)
    #fig.colorbar(img2, ax=ax2, format='%+2.f dB')
    xticks = np.linspace(0, 5, 11)
    ax2.set_xticks(xticks, 5.0 * count + xticks)
    ax2.set_xlabel('Time [sec]')
    ax2.set_ylim(0, 10000)
    ax2.set_ylabel('Freqency [Hz]')

    ax3 = fig.add_subplot(3, 1, 3)
    logF_fil = librosa.amplitude_to_db(np.abs(F_fil), ref=np.max)
    draw(logF_fil, hop_length=hop, sr=sr, x_axis='time', y_axis='hz', ax=ax3)
    #fig.colorbar(img3, ax=ax3, format='%+2.f dB')
    xticks = np.linspace(0, 5, 11)
    ax3.set_xticks(xticks, 5.0 * count + xticks)
    ax3.set_xlabel('Time [sec]')
    ax3.set_ylim(0, 10000)
    ax3.set_ylabel('Freqency [Hz]')

    plt.savefig(output_png_path)
    plt.clf()
    plt.close()


# 5秒ごとに分けて出力する
def output_graph(wav, pitch, F, F_fil, settings, output_path_without_ext):
    count = 0
    # frames: フーリエ変換配列F, F_filの5秒分の要素数
    frames = int(1000 * 0.005 * settings.sr / settings.shift_frames)

    while 1000 * count <= pitch.size:
        output_graph_5sec(
            wav[5 * settings.sr * count:5 * settings.sr * (count + 1)],
            pitch[1000 * count:1000 * (count + 1)],
            F[:, frames * count:frames * (count + 1)],
            F_fil[:, frames * count:frames * (count + 1)],
            settings,
            output_path_without_ext + '_{:02d}.png'.format(count),
            count)
        count += 1
