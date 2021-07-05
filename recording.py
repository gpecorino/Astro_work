import ugradio as ugr
import os
import numpy as np

ugr.interf_delay.DelayClient().delay_ns(0)

hpm = ugr.hp_multi.HP_Multimeter()

dt = 1

flag = input('Folder name >>> ')
time = ugr.timing.julian_date()
flag = 'wk7/' + str(time) + '_' + flag
os.mkdir(flag)

starttime = ugr.timing.unix_time()
last = starttime
savetime = 300  # time in seconds before saving a temp file
endtime = 9 * 3600
slic = 4700  # len of temp files

try:
    hpm.start_recording(dt)
    while True:
        unixnow = ugr.timing.unix_time()
        passedtime = unixnow - starttime
        interval = unixnow - last

        if interval > savetime:
            print(hpm.get_recording_status())

            time = ugr.timing.julian_date()

            dat, timestamp = hpm.get_recording_data()
            np.savez(flag + '/temp_' + str(time),
                     dat=dat[-slic:], timestamp=timestamp[-slic:])
            last = ugr.timing.unix_time()

        if passedtime > endtime:
            break
finally:
    dat, timestamp = hpm.get_recording_data()
    np.savez(flag + '/' + str(endtime // 3600) + 'hrdata_' +
             str(time), dat=dat, timestamp=timestamp)
    hpm.end_recording()