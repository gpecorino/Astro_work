import numpy as np
import matplotlib.pyplot as plt

directory = ['Feb21_1844_LO=1230', 'Feb21_1828_LO=1231']
avgnum = 5
switch = ['avg', 'med']
titles = ['Mean', 'Median']

gain = 827.8759100745887
sampling_rate = 6.25
nu_0 = 1420.405
lo_hi = (1230.0, 1231.0)
lo_lo = 190.0
HIleft = nu_0 - lo_hi[1] - lo_lo
HIright = nu_0 - lo_hi[0] - lo_lo
diff = np.abs(np.abs(HIleft) - sampling_rate / 2) - np.abs(HIright)
print(diff)


def running_average(y, r):
    cumsum = np.cumsum(np.insert(y, 0, 0))
    return (cumsum[r:] - cumsum[:-r]) / float(r)


def convert_ax(ax_f):
    """
    Update second axis according with first axis.
    """
    x1, x2 = ax_f.get_xlim()
    def nu2v(nu): return (1 - nu / nu_0) * 299792.458
    ax_v.set_xlim(nu2v(x1), nu2v(x2))
    ax_v.figure.canvas.draw()


fig, axs = plt.subplots()
fto = [0, 0]
for i in range(0, len(directory)):
    for j in range(1, len(switch)):
        filename = directory[i] + '/' + switch[j] + '_pspec.npz'
        l = np.load(filename)
        ft = l['spectrum'] / 160000
        freq = l['freq']
        ft[np.argwhere(freq == 0)] = 0
        ft = np.fft.fftshift(ft)
        freq = np.fft.fftshift(freq)  # + float(directory[i][-4:])+190
        lab = '$\\nu_{LO, hi}$ = ' + directory[i][-4:]

    fto[i] = ft

fig, ax_nu = plt.subplots()
ax_v = ax_nu.twiny()
ax_nu.callbacks.connect("xlim_changed", convert_ax)
s = fto[0] / fto[1]
zer = np.argwhere(freq == 0)[0][0]
cut = int(diff / (sampling_rate / 2) * zer)
print(cut)
left = s[cut:zer]
right = s[zer:][:len(left)]
right[0] = 1
s = running_average((right - left) / 2, avgnum) * gain / 2
print(np.max(s))
start = lo_lo + lo_hi[0]
nu = np.linspace(start, start + sampling_rate / 2, len(s))
ax_nu.plot(nu, s, label='$s_{LSB}/s_{USB}$')
ax_nu.set_xlabel('$\\nu \\,/$ MHz', fontsize=12)
ax_v.set_xlabel('$v \\,/ \\, kms^{-1}$', fontsize=12)
ax_nu.set_ylabel('$T_B$ / K', fontsize=12)
np.savez('1231d1230', s=s, freq=freq)

plt.subplots_adjust(top=.83)
plt.show()