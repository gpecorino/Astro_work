import numpy as np
import ugradio.timing as timing
lb = np.array([120,0])
def to3(co):
    co = np.radians(co)
    return np.array([np.cos(co[1])*np.cos(co[0]),np.cos(co[1])*np.sin(co[0]), np.sin(co[1])])

def to2(co):
    return np.degrees(np.array([np.arctan2(co[1],co[0]), np.arcsin(co[2])]))

R_RG = np.array([[-0.054876, -0.873437, -0.483835],
                  [0.494109, -0.444830, 0.746982],
                  [-0.867666, -0.198076, 0.455984]])
R_RG50 = np.array([[-0.066989, -0.872756, -0.483539],
                  [0.492728, -0.450347, 0.744585],
                  [-0.867601, -0.188375, 0.460200]])
R_GR = np.transpose(R_RG)
R_GR50 = np.transpose(R_RG50)

def RDtolb50(co):
    co3 = to3(co)
    r3 = np.dot(R_RG50, co3)
    r2 = to2(r3)
    return  r2

def lbtoRD50(co):
    co3 = to3(co)
    r3 = np.dot(R_GR50, co3)
    r2 = to2(r3)
    return  r2

def RDtolb(co):
    co3 = to3(co)
    r3 = np.dot(R_RG, co3)
    r2 = to2(r3)
    return  r2
    
def lbtoRD(co):
    co3 = to3(co)
    r3 = np.dot(R_GR, co3)
    r2 = to2(r3)
    return  r2

def RDtoHD(co, time):
    R = np.array([[np.cos(time), np.sin(time), 0],
                  [np.sin(time), -np.cos(time), 0],
                  [0, 0, 1]]) 
    co3 = to3(co)
    r3 = np.dot(R, co3)
    r2 = to2(r3)
    return  r2

def HDtoAA(co):
    lati = np.radians(37.873199)
    R = np.array([[-np.sin(lati),0, np.cos(lati)],
                  [0,-1, 0],
                  [np.cos(lati), 0, np.sin(lati)]]) 
    co3 = to3(co)
    r3 = np.dot(R, co3)
    r2 = to2(r3)
    return  r2

def lbtoAA(co, time):
    co1 = lbtoRD50(co)
    co2 = RDtoHD(co1, time)
    co3 = HDtoAA(co2)
    return co3
    
r = [184.5, -5.8]
time = timing.lst()
print(lbtoRD(r))
print([5.5*15, 22])
print(r)
print(RDtolb(lbtoRD50(r)))