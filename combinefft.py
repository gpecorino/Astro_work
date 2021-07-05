import numpy as np
import matplotlib.pyplot as plt

sampling_rate = 62.5
volt_range = 0.05 * 1000 # milivolts
slic = 200

def fftshift_n_square(f):
    return np.abs(np.square(np.fft.fftshift(f)))

while True:
    filename = input('Filename to load?')
    dat = np.load(str(filename)+'.npz')
    dat = dat[dat.files[0]]
    dat = np.array(dat) # *volt_range/2/65535
    
    print(len(dat))
    half_length = int(len(dat) / 2)
    datA = dat[0:half_length]
    datB = dat[half_length:]
    plt.plot(datA[:slic], label = 'Re')
    plt.plot(datB[:slic], label = 'Im')
    plt.legend()
    
    plt.figure()
    plt.hist(datA, bins=100)
    
    #forming a complex array
    imag = complex(0,1)
    dat = datA + datB * imag
    ft = np.fft.fft(dat)
    freq = np.fft.fftfreq(ft.size) * sampling_rate
    fig, ax = plt.subplots()
    
    ft[np.argwhere(freq == 0)] = 0
    maxfreq = freq[np.argwhere(ft == max(ft))]
    print(maxfreq[0])
    plt.plot(np.fft.fftshift(freq), fftshift_n_square(ft), label = 'Raw max freq =' + str(maxfreq[0][0]))
    lab = 'Actual max freq = '+ str(maxfreq[0][0]+190+1230)
    ax.minorticks_on()
    plt.xlim(-2.5, 2.5)
    # plt.vlines(maxfreq, 0, max(ft), color = 'black', label = lab)
    plt.legend()
    plt.show()