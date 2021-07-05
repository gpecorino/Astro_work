import numpy as np
import ugradio.timing as timing

lati = 37.873199  # Coordinate on Earth

l = 120  # Galactic coorinates of Milky Way target
b = 0

lat = np.radians(lati)
l = np.radians(l)
b = np.radians(b)
print(timing.lst())

def convert(coor, R):
    """ Convert one set of coorinates COOR to another with matrix R """
    long = coor[0]
    lat = coor[1]
    x = [np.cos(lat) * np.cos(long), np.cos(lat) * np.sin(long), np.sin(lat)]
    xp = np.matmul(R, x)

    longp = np.degrees(np.arctan2(xp[1], xp[0]))
    latp = np.degrees(np.arcsin(xp[2]))
    return [longp, latp]


def R_Eq_HA_to_Az(lati):
    """ Return a rotation matrix from HA Equatorial coorinates to Azimuthal coorinates at local latitude LATI """
    sin_phi = np.sin(lati)
    cos_phi = np.cos(lati)
    return np.array([[-sin_phi, 0, cos_phi],
            [0, -1, 0],
            [cos_phi, 0, sin_phi]])


def R_Eq_RA_to_HA(lst):
    """ Return a rotation matrix from RA Equatorial coorinates to HA Equatorial coorinates at Local Sidereal Time LST in radians """
    cos_lst = np.cos(lst)
    sin_lst = np.sin(lst)
    return np.array([[cos_lst, sin_lst, 0],
            [sin_lst, -cos_lst, 0],
            [0, 0, 1]])


R_Eq_RA_to_Gal = np.array([[-0.054876, -0.873437, -0.483835],
                  [0.494109, -0.444830, 0.746982],
                  [-0.867666, -0.198076, 0.455984]])  # J2000

# Actually using the functions. CHANGE THINGS HERE ONLY
time = timing.lst()
print(time)
R = np.matmul(R_Eq_HA_to_Az(lati).T, 
    np.matmul(R_Eq_RA_to_HA(time), R_Eq_RA_to_Gal)).T


print(convert((l, b), R))