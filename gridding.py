import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import csv

F_list = np.arange(3.36,9.13,step=0.72) #Specified frequncy range and step size for ATA, all values in units of GHz

for i in range(len(F_list)):
    F_sky = F_list[i]
    FWHM = 3.5/F_sky
    name_1 = "grid_for_{}GHz_1.csv".format(F_sky) #We create 3 csv files, 1 for each subarray
    name_2 = "grid_for_{}GHz_2.csv".format(F_sky) 
    name_3 = "grid_for_{}GHz_3.csv".format(F_sky) 

    lmin = -1; lmax = 9
    bmin = -5; bmax = 5

    coordinates_l = []
    coordinates_b = []
    b = np.arange(bmin,bmax,step=FWHM)
    for bi in b:
        l = lmin
        while l<lmax:
            if l<0:
                l_c = 360+l  #converts negative coordinates into positive
                coordinates_l.append(l_c)
                coordinates_b.append(bi)
            else:
                coordinates_l.append(l)
                coordinates_b.append(bi)
            l += FWHM

    coordinates_l_1 = []
    coordinates_b_1 = []
    coordinates_l_2 = []
    coordinates_b_2 = []
    coordinates_l_3 = []
    coordinates_b_3 = []

    for i in range(len(coordinates_l)):
        if i <= (len(coordinates_l)*(1/3)):
            coordinates_l_1.append(coordinates_l[i])
            coordinates_b_1.append(coordinates_b[i])
        elif (i > (len(coordinates_l)*(1/3))) and (i <= (len(coordinates_l)*(2/3))):
            coordinates_l_2.append(coordinates_l[i])
            coordinates_b_2.append(coordinates_b[i])
        elif i > (len(coordinates_l)*(2/3)):
            coordinates_l_3.append(coordinates_l[i])
            coordinates_b_3.append(coordinates_b[i])


    coord_gal_1 = SkyCoord(coordinates_l_1*u.degree,coordinates_b_1*u.degree,frame='galactic') #galactic coordinates
    coord_icrs_1 = coord_gal_1.transform_to('icrs')                                            #ra,dec
    coord_gal_2 = SkyCoord(coordinates_l_2*u.degree,coordinates_b_2*u.degree,frame='galactic')
    coord_icrs_2 = coord_gal_2.transform_to('icrs')
    coord_gal_3 = SkyCoord(coordinates_l_3*u.degree,coordinates_b_3*u.degree,frame='galactic')
    coord_icrs_3 = coord_gal_3.transform_to('icrs')

    print(len(coordinates_l))

    with open(name_1, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Pointing#","RA", "Dec", "G.Long(l)", "G.Lat(b)"])
        for i in range(len(coordinates_l_1)):
            writer.writerow([i,coord_icrs_1.ra.hour[i],coord_icrs_1.dec.degree[i],coord_gal_1.l.degree[i],coord_gal_1.b.degree[i]])

    with open(name_2, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Pointing#","RA", "Dec", "G.Long(l)", "G.Lat(b)"])
        for i in range(len(coordinates_l_2)):
            writer.writerow([i,coord_icrs_2.ra.hour[i],coord_icrs_2.dec.degree[i],coord_gal_2.l.degree[i],coord_gal_2.b.degree[i]])

    with open(name_3, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Pointing#","RA", "Dec", "G.Long(l)", "G.Lat(b)"])
        for i in range(len(coordinates_l_3)):
            writer.writerow([i,coord_icrs_3.ra.hour[i],coord_icrs_3.dec.degree[i],coord_gal_3.l.degree[i],coord_gal_3.b.degree[i]])


    """This produces a plot of our pointings across the whole sky in galactic coordinates"""
    plt.figure()
    plt.subplot(2,2,1)
    plt.scatter(coordinates_l_1,coordinates_b_1,c='g')
    plt.xlim(0,360)
    plt.ylim(-6,6)
    plt.title("Array1")

    plt.subplot(2,2,2)
    plt.scatter(coordinates_l_2,coordinates_b_2,c='b')
    plt.xlim(0,360)
    plt.ylim(-6,6)
    plt.title("Array2")

    plt.subplot(2,2,3)
    plt.scatter(coordinates_l_3,coordinates_b_3,c='r')
    plt.xlim(0,360)
    plt.ylim(-6,6)
    plt.title("Array3")

    plt.subplot(2,2,4)
    plt.scatter(coordinates_l_1,coordinates_b_1,c='g')
    plt.scatter(coordinates_l_2,coordinates_b_2,c='b')
    plt.scatter(coordinates_l_3,coordinates_b_3,c='r')
    plt.xlim(0,360)
    plt.ylim(-6,6)
    plt.title("Total Gridding for {}GHz".format(F_sky))

    plt.show()

exit()