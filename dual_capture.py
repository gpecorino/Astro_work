import ugradio as ugr
import matplotlib.pyplot as plt
import numpy as np

path = 'wk4/Feb17_'
flag = 'True'
sampling_rate = 62.5 #MHz
volt_rang = 0.05 # volts

def fftshift_n_square(dat):
    return np.abs(np.square(np.fft.fftshift(ft)))

while flag != 'exit':
    print('Type Ctrl+D to exit')
    print('Anything else to take data')
    flag = input('Filename >>> ')
    print('data capturing')
    dat = ugr.pico.capture_data(
        volt_range='50mV', divisor=1, dual_mode = True, nblocks = 100) *volt_rang/65535 #nsamples can't go above 16340
    print(len(dat))
    print('Done')
    np.save(path + str(flag), dat)
    half_length = int(len(dat) / 2)
    datA = dat[0:half_length]
    datB = dat[half_length:]
    plt.plot(datA[:], label = 'Re')
    plt.plot(datB[:], label = 'Im')
    plt.legend(loc = 1)
    
    #forming a complex array
    imag = complex(0,1)
    dat = datA + datB * imag

    ft = np.fft.fft(dat)
    freq = np.fft.fftfreq(ft.size) * sampling_rate
    fig, ax = plt.subplots()
    #plt.plot(np.fft.fftshift(freq), np.fft.fftshift(ft.real), label='Re')
    #plt.plot(np.fft.fftshift(freq), np.fft.fftshift(ft.imag), label='Im')
    
    # plt.plot(np.fft.fftshift(freq), fftshift_n_square(ft))
    ft[np.argwhere(freq == 0)] = 0
    maxfreq = freq[np.argwhere(ft == max(ft))]
    print(maxfreq)
    plt.plot(np.fft.fftshift(freq), fftshift_n_square(ft), label = 'Raw max freq =' + str(maxfreq[0][0]))
    lab = 'Actual max freq = '+ str(maxfreq[0][0]+190+1230)
    ax.minorticks_on()
    #plt.xlim(-1,1)
    plt.vlines(maxfreq, 0, max(ft), color = 'black', label = lab)
    plt.legend(loc = 1)
    # plt.title('Spectrum at ' + times + 'v_s')
    plt.show()
    break