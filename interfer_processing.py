import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LogNorm
from sys import argv


def fftshift_n_square(f):
    return np.fft.fftshift(np.abs(np.square(f)))



entries = [str(argv[-1])]
# nu_filter = 0.032  # To be calculated for 2458920.963951614_moon_trial_2
nu_filter_1 = 0.039
nu_filter = 0.011  # To be calculated for 2458921.4215891543_trial_3
t_snippet = 600
index_cut_start = 12510
index_cut_end = 17060

data = np.array([])
time = np.array([])
for i in entries:
    dat = np.load(i, allow_pickle=True)
    data = np.append(data, dat['dat'])
    time = np.append(time, dat['timestamp'])

time, indices = np.unique(time, return_index=True)
data = data[indices]


print('Time', time[0], time[-1])
len_data = len(data)
print('len', len_data)
dt = np.median(time[1:] - time[:-1])
sampling_rate = 1 / dt
print('nu = ', sampling_rate)

baseline = np.polyfit(time, data, 3)[::-1]
poly = np.polynomial.polynomial.polyval(
    time, baseline)
orig = np.copy(data)
data = data - poly
time = time - time[0]


plt.figure()
ft = np.fft.fft(data)
ft[0] = 0
freq = np.fft.fftfreq(len(ft)) * sampling_rate
freq_shift = np.fft.fftshift(freq)
plt.plot(freq_shift, fftshift_n_square(ft), label='Full')
plt.xlabel('$\\nu$ / Hz', fontsize=12)
index_filter = int(nu_filter * len(freq) / sampling_rate)
index_filter_1 = int(nu_filter_1 * len(freq) / sampling_rate) + 1
ft[0:index_filter] = 0
ft[-index_filter:] = 0
ft[index_filter_1:-index_filter_1] = 0
plt.plot(freq_shift, fftshift_n_square(ft), label='Filtered')
plt.legend()

ift = np.fft.ifft(ft)

plt.figure()
plt.plot(time, orig, label='Raw')
plt.plot(time, poly, label='Polynomial fit of raw data')
plt.plot(time, data, label='Subtracted w/ polynomial')
plt.plot(time, ift, label='Filtered', alpha=0.5)
plt.xlabel('t / s', fontsize=12)
plt.ylabel('Power (Arbitrary unit)', fontsize=12)
plt.legend()

plt.figure()
time_mid = time[len_data - 100:len_data + 100]
data_mid = data[len_data - 100:len_data + 100]
plt.plot(time_mid, data_mid - np.mean(data_mid),
         label='Unfiltered, translated')
plt.plot(time_mid, ift[len_data - 100:len_data + 100], label='Filtered')
plt.xlabel('t / s', fontsize=12)
plt.ylabel('Power (Arbitrary unit)', fontsize=12)
plt.legend()

# Start dividing into snippets
n_snippet = int(len_data / t_snippet + 0.5)
len_snippet = len_data // n_snippet
split_data = np.split(ift[:n_snippet * len_snippet], n_snippet)
split_time = np.split(time[:n_snippet * len_snippet], n_snippet)
freq = np.fft.fftfreq(len_snippet) * sampling_rate
freq_shift = np.fft.fftshift(freq)
ft = [0 for i in range(n_snippet)]
times = np.median(split_time, axis=1)
maxima = [0 for i in range(n_snippet)]
spectra = [0 for i in range(n_snippet)]

list_shown = (0, 1, n_snippet // 2, n_snippet)

for i in range(n_snippet):
    ft[i] = np.fft.fft(split_data[i])
    ft[i][0] = 0
    power_spectrum = np.abs(np.square(ft[i]))
    maxima[i] = np.abs(freq[np.argmax(power_spectrum)])
    spectra[i] = np.fft.fftshift(power_spectrum)
    if i in list_shown:
        plt.figure()
        plt.plot(freq_shift, spectra[i])
        plt.xlim(-nu_filter_1, nu_filter_1)
        plt.xlabel('$\\nu$ / Hz', fontsize=12)

plt.figure()
plt.plot(times,  maxima, 'o-')
plt.xlabel('t / s', fontsize=12)
plt.ylabel('$\\nu_{max}$ / Hz', fontsize=12)

plt.imshow(spectra, cmap='afmhot', interpolation='gaussian',
           aspect='auto', extent=(-nu_filter_1, nu_filter_1, times[0], times[-1]), norm=LogNorm(vmin=0.001, vmax=np.max(spectra)))
plt.xlabel('$\\nu$ / Hz', fontsize=12)
plt.ylabel('t / s', fontsize=12)
plt.colorbar()

plt.show()