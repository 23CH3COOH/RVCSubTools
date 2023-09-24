# -*- coding: utf-8 -*-
import numpy as np
from scipy.io import wavfile


'''
return_type == 'wav_val' ⇒ 元の波形のみ返す
上記以外の場合、サンプリング周波数と元の波形を返す
'''
def input_wav_file(input_wav_path, return_type='all', to_mono=True):
    sr, wav = wavfile.read(input_wav_path)
    if to_mono and wav.ndim > 1:
        assert wav.shape[1] == 2
        if np.all(wav[:, 0] == wav[:, 1]):
            wav = wav[:, 0]
        else:
            wav = (0.5 * wav[:, 0] + 0.5 * wav[:, 1]).astype(wav.dtype)
    if return_type == 'wav_val':
        return wav
    return sr, wav


'''
出力のビット数はPCM_16固定
引数wavのデータ型はnp.int16か-1以上1未満の浮動小数どちらでも可
'''
def output_wav_file(wav, output_samling_rate, output_file_path):
    try:
        if wav.dtype == np.int16:
            wavfile.write(output_file_path, output_samling_rate, wav)
            return True
        else:
            if -1.0 <= np.min(wav) and np.max(wav) < 1.0:
                wav_int16 = ((2 ** 15) * wav).astype(np.int16)
                wavfile.write(output_file_path, output_samling_rate, wav_int16)
                return True
            if -1.25 <= np.min(wav) and np.max(wav) < 1.25:
                print('Shrinked Wav Amp 80%.')
                wav_int16 = ((2 ** 15) * 0.8 * wav).astype(np.int16)
                wavfile.write(output_file_path, output_samling_rate, wav_int16)
                return True
            print('Invalid wav format.')
            return False
    except Exception as e:
        print(e)
        return False
