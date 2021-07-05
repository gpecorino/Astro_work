%matplotlib qt 
%config InlineBackend.figure_format = 'retina'
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FFMpegWriter
metadata = dict(title='My first animation in 2D', artist='Matplotlib',comment='Wakanda is coming.')
writer = FFMpegWriter(fps=15, metadata=metadata)

def KeplerODE(t,y):
    global mp,ma1,ma2,ma3,G

    rp = y[0:2]
    vp = y[2:4]
    r1 = y[4:6]
    v1 = y[6:8]
    r2 = y[8:10]
    v2 = y[10:12]
    r3 = y[12:14]
    v3 = y[14:16]
    
    #distance between planet and object
    rp1 = rp-r1
    rp2 = rp-r2
    rp3 = rp-r3

    drdtp = vp 
    drdt1 = v1 
    drdt2 = v2 
    drdt3 = v3 

    #for planet
    Fp    = - ma1 * mp * G / np.linalg.norm(rp1)**3 * rp1
    ap    = Fp / mp
    dvdtp = ap # only use rp1 since the acceleration on the planet will be neglegent.
    
    #for object 1
    F1    = - ma1 * mp * G / np.linalg.norm(rp1)**3 * rp1
    a1    = F1 / ma1
    dvdt1 = a1
    
    #for object 2
    F2    = - ma2 * mp * G / np.linalg.norm(rp2)**3 * rp2
    a2    = F2 / ma2
    dvdt2 = a2
    
    #for object 3
    F3    = - ma3 * mp * G / np.linalg.norm(rp3)**3 * rp3
    a3    = F3 / ma3
    dvdt3 = a3 *0 # this object is set to not interact with planet to act as a reference for the other 2 objects
    
    return np.concatenate((drdtp,dvdtp,drdt1,dvdt1,drdt2,dvdt2,drdt3,dvdt3))

#constants
mp = 5.97e24 #mass of earth [kg]
Rad = 6.371e6 #radius of earth [m]
ma1 = 7.35 #mass of object [kg]
ma2 = 7.35
ma3 = 7.35
G = 6.67e-11 #Gravitational constant [m^3 kg s^-2]
vel = 0.2*np.sqrt(2*G*mp/Rad) #velocity of objects based off escape velocity of earth
theta1 = 60 #angle that object 1 travels at relative to earth
rad1 = (np.pi/180)*theta1 #angle in radians

#initial position
rp = np.array([2e8, 0])

# initial velocities
vp = np.array([-10000,0]);

# initial positions
r1 = np.array([0,4e7])

# initial velocities
v1 = np.array([vel*np.cos(rad1),-vel*np.sin(rad1)]);

# initial positions
r2 = np.array([-1e8,4e7])

# initial velocities
v2 = np.array([-vel*np.cos(rad2),-vel*np.sin(rad2)]);

# initial positions
r3 = np.array([0,4e7])

# initial velocities
v3 = np.array([0, -vel]);

y = np.concatenate((rp,vp,r1,v1,r2,v2,r3,v3))

#setting up arrays
t = 0
tMax = 3.2e4
dt   = tMax/1000
tt = []
xtp = []
ytp = []
xt1 = []
yt1 = []
xt2 = []
yt2 = []
xt3 = []
yt3 = []
vo1 = []
vo2 = []
vo3 = []

def init_figure():
    fig = plt.figure(figsize=(12.,6.))
    plt.show()
    return fig

def update_figure():
        plt.clf()
        #position graph
        ax1 = fig.add_subplot(121)
        ax1.set_title('Path of Objects')
        ax1.plot(xtp,ytp,'r-',label='planet')
        ax1.plot(xt1,yt1,'b-',label='object 1')
        ax1.plot(xt2,yt2,'g-',label='object 2')
        ax1.plot(xt3,yt3,'y-',label='object 3')
        ax1.legend()

        #velocity graph
        ax2 = fig.add_subplot(122,aspect='equal')
        ax2.set_title('Velocity vs Time')
        ax2.xlabel('Time(s)')
        ax2.ylabel('Velocity(m/s)')
        ax2.plot(tt,vo1,'b-',label='object 1')
        ax2.plot(tt,vo2,'g-', label = 'object 2')
        ax2.plot(tt,vo3,'y-', label = 'object 3')
        ax2.legend()
        


        #plt.show()
        plt.draw()
        plt.pause(0.0001)

fig = init_figure()
with writer.saving(fig, "Final.mp4", dpi=200):

    update_figure()

    while (t<tMax):
        #grap values from y
        tt.append(t)
        rp = y[0:2]
        vp = y[2:4]
        r1 = y[4:6]
        v1 = y[6:8]
        r2 = y[8:10]
        v2 = y[10:12]
        r3 = y[12:14]
        v3 = y[14:16]


        #append new positions
        xtp.append(rp[0])
        ytp.append(rp[1])
        xt1.append(r1[0])
        yt1.append(r1[1])
        xt2.append(r2[0])
        yt2.append(r2[1])
        xt3.append(r3[0])
        yt3.append(r3[1])
    
        #calculate new velocities
        v1t = np.sqrt(v1[0]**2 + v1[1]**2)
        v2t = np.sqrt(v2[0]**2 + v2[1]**2)
        v3t = np.sqrt(v3[0]**2 + v3[1]**2)
    
        #append new velocities
        vo1.append(v1t)
        vo2.append(v2t)
        vo3.append(v3t)
 
        #Runge-Kutta Integration 
        f1 = KeplerODE(t       ,y          )
        f2 = KeplerODE(t+dt/2.0,y+f1*dt/2.0)
        f3 = KeplerODE(t+dt/2.0,y+f2*dt/2.0)
        f4 = KeplerODE(t+dt    ,y+f3*dt    )

        y = y + (f1 + 2.0*f2 + 2.0*f3 + f4) / 6.0 * dt
        t = t + dt

            

        update_figure()
        print(' Simulation finished.')
        plt.draw()
        plt.pause(0.01)
        writer.grab_frame()