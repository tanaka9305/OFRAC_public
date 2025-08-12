import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal

##CSVファイル名と時間設定（書き換える）
filename = '20250802_OF_25Iida_003.csv'
start_time = 30  # 秒
end_time = 33    # 秒
use_cols = 4
###################################

sampling_rate = 50  # サンプリングレート [Hz]
Ts = 1 / sampling_rate  # サンプリング周期 [s]
volt2disp = 0.075/5  # 電圧から変位への変換係数 [m/V]
cut_off = 25  # カットオフ周波数 [Hz]

def import_data():
    start_row = int(start_time / Ts + 17)  # データ開始行（ヘッダ込み）
    end_row = int(end_time / Ts + 17)

    # CSV読み込み（例：Shift-JIS）
    df = pd.read_csv(
        filename,
        encoding='shift_jis',
        usecols=[use_cols],  # 必要な列（0始まりの列番号）
        skiprows=start_row,
        nrows=end_row - start_row
    )
    return df

def diff_filter(time_series):
    fc = cut_off  # カットオフ周波数 [Hz]
    wc = 2 * np.pi * fc  # カットオフ角周波数 [rad/s]
    alpha = 1 / (1 + wc * Ts)

    # 差分器 + 一次遅れフィルタ
    y = np.zeros_like(time_series)  # 出力（微分近似）
    for k in range(1, len(time_series)):
        dx = (time_series[k] - time_series[k-1]) / Ts
        y[k] = alpha * y[k-1] + (1 - alpha) * dx

    return volt2disp * y

def diff_ideal(time_series):
    return np.gradient(volt2disp * time_series, Ts)

def main():
    # データのインポート
    imported_data = import_data()
    data = imported_data.values.flatten()  # ndarray に変換

    # 微分近似フィルタ適用
    diff_filter_data = diff_filter(data)
    diff_ideal_data = diff_ideal(data)

    # 時間軸
    t = np.arange(len(data)) * Ts

    # プロット
    plt.figure(figsize=(10, 5))
    plt.plot(t, diff_filter_data, label='Differentiated Data', linestyle='--')
    plt.plot(t, diff_ideal_data, label='Ideal Differentiated Data', linestyle=':')
    plt.title('Damper Speed with Low-pass Filter')
    plt.xlabel('Time [s]')
    plt.ylabel('Velocity [m/s]')
    plt.legend()
    plt.grid()
    plt.show()


main()
