import ugradio as ugr
import matplotlib.pyplot as plt
import numpy as np
path = 'wk4/Feb16_'
flag = 'True'
sampling_rate = 62.5 #MHZ
while flag != 'exit':
    print('Type exit to exit')
    print('Anything else to take data')
    flag = input('Filename >>> ')
    dat = ugr.pico.capture_data(volt_range='50mV', divisor=1) #nsamples can't go above 16340
    print(dat[:200])
    np.save(path + str(flag), dat)
    dat = dat*50/2**16
    plt.plot(dat[:])
    plt.ylabel('Volt(mV)')
    plt.show()
    
    #plotting histogram
    counts, bins = np.histogram(dat, 50)
    bincenters = (bins[:-1]+bins[1:])*0.5
    plt.bar(bincenters, counts,edgecolor = 'black', width = bins[1]-bins[0])
    print(counts)
    plt.show()
    
    ft = np.fft.fft(dat)
    freq = np.fft.fftfreq(ft.size) * sampling_rate
    fig, ax = plt.subplots()
    #plt.plot(np.fft.fftshift(freq), np.fft.fftshift(ft.real))
    #plt.plot(np.fft.fftshift(freq), np.fft.fftshift(ft.imag))
    plt.plot(np.fft.fftshift(freq), abs(np.fft.fftshift(ft.imag))**2+abs(np.fft.fftshift(ft.imag))**2)
    ax.minorticks_on()
    # plt.title('Spectrum at ' + times + 'v_s')
    plt.show()