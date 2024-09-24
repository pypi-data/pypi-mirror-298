from collections.abc import Iterable
import numpy as np

def pipe_mmatrix(D:float, h:float, t:float, rho:float=7.850, 
                 horizontal:bool=False, angle:float=0, 
                 origin:np.ndarray=np.r_[0,0,0], exclude_Steinar=False):
    """Returns the moment of inertia of the pipe

    Args:
        D (float): Diameter of the pipe
        h (float): Length of the pipe
        t (float): Thickness of the pipe
        rho (float, optional): Density of the material. Defaults to 7.850.
        horizontal (bool, optional): Defaults to False.
            if True the starting position of the pipe is horizontal (so x is axial)
            else the starting position of the pipe is vertical (so z is axial)
        angle (float, optional): Angle to rotate pipe about global z-axis. Defaults to 0.
        origin (np.ndarray, optional): Origin of global system. Defaults to np.r_[0,0,0].
        exclude_Steinar (bool, optional): If True, the Steiner term is excluded. Defaults to False.

    Returns:
        tuple: _description_
    """
    pi = np.pi
    if isinstance(t, Iterable): t = t[0]
    r2, r1 = D/2, (D-2*t)/2
    m = pi*(r2**2 - r1**2)*rho*h
    Izz = 0.5*m*(r1**2 + r2**2)
    Ixx = Iyy = 1/12 * m * (3*(r1**2 + r2**2) + h**2)
    #Ixx = 1/12*m*(3*(r2**2+r1**2) + h**2)
    #Iyy = 1/12*m*(3*(r2**2+r1**2) + h**2)
    #Izz = 1/2*m*(r2**2 + r1**2)
    #print(Ixx, Iyy, Izz, m, r1, r2)
    if horizontal:
        Ixx, Iyy, Izz = Izz, Iyy, Ixx   
    T = np.array([[Ixx,   0,   0],
                  [  0, Iyy,   0],
                  [  0,   0, Izz]])
    # Now rotate, irrelevant if not horizontal
    a = angle*np.pi/180.
    ca, sa = np.cos(a), np.sin(a)
    R = np.array([[ca, -sa, 0],
                  [sa,  ca, 0],
                  [ 0,  0,  1]])
    T = R@T@R.T  
    # Steinar term
    xc, yc, zc = origin
    S = np.array([[yc**2+zc**2,  0,  0],
                  [0,  xc**2+zc**2,  0],
                  [0,  0, xc**2+yc**2]])
    return (m, T) if exclude_Steinar else (m, T+m*h*S)