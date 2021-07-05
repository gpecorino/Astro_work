import ugradio as ugr
import matplotlib.pyplot as plt
import numpy as np
import os

flag = 'True'
sampling_rate = 62.5 #MHz
volt_rang = 0.05 *1000# volts
num = 100 # number of loops
numb = 100 # number of blocks per loop
divi = 1 # divisor of sampling freq
slic = 500
lo_lo = 190
lo_hi = 1230

def fftshift_n_square(f):
    return np.abs(np.square(np.fft.fftshift(f)))

print('\n Let the data taking begin! \n')

sampling_rate /= divi
while flag:
    flag = input('Filename >>> ')
    os.mkdir(flag)
    for i in np.arange(0,num):
        if (i % 10 == 0):    
            print('data capturing... \n Block =', i+1 )
        dat = ugr.pico.capture_data(
            volt_range='50mV', divisor=divi, dual_mode = True, nblocks = numb) *volt_rang/65535 #nsamples can't go above 16340
        print('Done \n')

        filename = str(flag)+'/block_'+str(i+1)
        np.savez(filename, dat = dat)
    print('All done! Have a nice day')
    half_length = int(len(dat) / 2)
    datA = dat[0:half_length]
    datB = dat[half_length:]
    plt.plot(datA[:slic], label = 'Re')
    plt.plot(datB[:slic], label = 'Im')
    plt.legend(loc = 1)
    
    plt.figure()
    plt.hist(datA, bins = 100)
    
    #forming a complex array
    imag = complex(0,1)
    dat = datA + datB * imag

    ft = np.fft.fft(dat)
    freq = np.fft.fftfreq(ft.size) * sampling_rate
    fig, ax = plt.subplots()

    ft[np.argwhere(freq == 0)] = 0
    maxfreq = freq[np.argwhere(ft == np.max(ft))]
    print(maxfreq)
    plt.plot(np.fft.fftshift(freq), fftshift_n_square(ft), label = 'Raw max freq =' + str(maxfreq[0][0]))
    lab = 'Actual max freq = '+ str(maxfreq[0][0]+lo_lo+lo_hi)
    ax.minorticks_on()
    plt.xlim(-2,2)
    plt.vlines(maxfreq, 0, np.max(ft), color = 'black', label = lab)
    plt.legend(loc = 1)
    # plt.title('Spectrum at ' + times + 'v_s')
    plt.show()