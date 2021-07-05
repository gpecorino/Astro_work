  
import ugradio
import numpy as np
timing = ugradio.timing

ifm = ugradio.interf.Interferometer()

endtime = 3600 * 9
t = ugradio.timing.julian_date()
starttime = ugradio.timing.unix_time()
last = starttime
point = np.array([])
altazs = np.array([])
filename = input('Filename?')

radec_orion = [83.82, -5.391]
radec_m17 = [275.2, -16.2]

radec = radec_m17

try:
    while True:
        unixnow = ugradio.timing.unix_time()
        passedtime = unixnow - starttime
        interval = unixnow - last

        if interval > 30:

            jdnow = timing.julian_date()
            # radec = ugradio.coord.sunpos(jdnow)
            # radec = ugradio.coord.moonpos(jdnow,37.8372, -122.2753, 0)

            precessed = ugradio.coord.precess(
                radec[0], radec[1], jdnow, 'J2000')
            altaz = ugradio.coord.get_altaz(
                precessed[0], precessed[1], jdnow, ugradio.nch.lat, ugradio.nch.lon, ugradio.nch.alt)
            ifm.point(altaz[0], altaz[1])
            print('precessed alt az = ', altaz)
            ptg = ifm.get_pointing()
            print(ptg)
            point = np.append(point, ptg)
            altazs = np.append(altazs, altaz)
            last = ugradio.timing.unix_time()

        if passedtime > endtime:
            break
finally:
    np.savez(str(t) + 'pointing_' + filename, point=point, altaz=altazs)
    ifm.stow()