import numpy as np
import math


def jonswap(f:np.ndarray, Hm0:float, Tp:float, gamma:float=3.3, sigma_low:float=.07, sigma_high:float=.09,
            g:float=9.81, method:str='yamaguchi', normalize:bool=False):
    '''Generate JONSWAP spectrum using a function
    taken from https://github.com/openearth/oceanwaves-python/blob/master/oceanwaves/spectral.py
    and then simplified (temporary solution to circumvent the need to use WAFO). Checked against
    wafo for specified gamma
    
    TODO: Set gamma's default value to one based on a formula
    
    To use:
    >> from teklib.wave_theory.spectrums import jonswap
    >> import matplotlib.pyplot as plt
    >> plt.plot(f, jonswap(f, 10, 15))
    >> plt.show()
    
    Parameters
    ----------
    f : numpy.ndarray
        Array of frequencies [Hz]
    Hm0 : float, numpy.ndarray
        Required zeroth order moment wave height
    Tp : float, numpy.ndarray
        Required peak wave period
    gamma : float
        JONSWAP peak-enhancement factor (default: 3.3)
    sigma_low : float
        Sigma value for frequencies <= ``1/Tp`` (default: 0.07)
    sigma_high : float
        Sigma value for frequencies > ``1/Tp`` (default: 0.09)
    g : float
        Gravitational constant (default: 9.81)
    method : str
        Method to compute alpha (default: yamaguchi)
    normalize : bool
        Normalize resulting spectrum to match ``Hm0``
    Returns
    -------
    E : numpy.ndarray
        Array of shape ``f, Hm0.shape`` with wave energy densities
    '''

    # Pierson-Moskowitz
    if method.lower() == 'yamaguchi':
        alpha = 1. / (.06533 * gamma ** .8015 + .13467) / 16.
    elif method.lower() == 'goda':
        alpha = 1. / (.23 + .03 * gamma - .185 / (1.9 + gamma)) / 16.
    else:
        raise ValueError('Unknown method: %s' % method)

    E_pm = alpha * Hm0**2 * Tp**-4 * f**-5 * np.exp(-1.25 * (Tp * f)**-4)

    # JONSWAP
    sigma = np.ones(f.shape) * sigma_low
    sigma[f > 1./Tp] = sigma_high

    E_js = E_pm * gamma**np.exp(-0.5 * (Tp * f - 1)**2. / sigma**2.)

    if normalize:
        # axis=0 seems to work fine with all kinds of inputs
        E_js *= Hm0**2. / (16. * np.trapz(E_js, f, axis=0))

    return E_js



# Torsethaugen 1996 two-peak wave spectrum.
def torsethaugen1996(h_s, t_p, w, g=9.80665):
    """ Input parameters:
    h_s : Significant wave height [m].
    t_p : Spectral peak period [s].
    w   : Wave frequencies [rad/s].
    
    The spectrum is modified by a factor h1 and h2 to ensure that output Hm0 is equal to the h_s.
 
    Reference:
    DNVGL-RP-C205 2010 p110.
    """
    
    gamma = np.math.gamma
    
    # response variables
    wave_spectrum = {}

    # fetch length
    af = 6.6

    # wind or swell distinction
    Tf = af * h_s ** (1/3.)
    if t_p <= Tf:
        sd = 'wind'
    elif t_p > Tf:
        sd = 'swell'

    # for all frequencies
    frequencies = w/2/np.pi + 0.0001
    ncomp = len(frequencies)
    
    S = np.zeros((len(frequencies), 4))

    for fc, f in enumerate(frequencies):

        # common parameters
        N = 0.5 * np.sqrt(h_s) + 3.2

        #---------------------------------------------------------------------#
        # if wind dominated seas
        #---------------------------------------------------------------------#
        if sd == 'wind':

            rpw = 0.7 + 0.3 * np.exp(-(2*(Tf - t_p)/(Tf - 2*math.sqrt(h_s)))**2)

            # primary peak
            HS1 = rpw * h_s
            TP1 = t_p
            M = 4
            gma1 = 35. * (1 + 3.5*np.exp(-h_s)) * (2*np.pi/g * HS1/t_p**2)**0.857
            f2 = (2.2 * M**-3.3 + 0.57) * N**(0.53 -
                                              0.58*M**0.37) + 0.94 - 1.04*M**-1.9
            Agma1 = (4.1 * (N - 2*M**0.28 + 5.3)**(0.96 - 1.45*M**0.1)
                     * np.log(gma1)**f2 + 1.0) / gma1
            fn1 = f * TP1
            if fn1 < 1:
                sig = 0.07
            elif fn1 >= 1:
                sig = 0.09

            gmaF1 = gma1 ** np.exp(-1/(2*sig**2)*(fn1 - 1)**2)
            GMAS1 = fn1 ** -N * np.exp(-N/M * fn1**-M)
            G0 = (1/M * (N/M) ** (-(N-1)/M) * gamma((N-1)/M)) ** -1
            Sn1 = G0 * Agma1 * GMAS1 * gmaF1
            E1 = 1/16. * HS1**2 * TP1

            # secondary peak
            HS2 = np.sqrt(1-rpw**2)*h_s
            TP2 = Tf + 2.0
            M = 4
            gma2 = 1.
            f2 = (2.2 * M**-3.3 + 0.57) * N**(0.53 -
                                              0.58*M**0.37) + 0.94 - 1.04*M**-1.9
            Agma2 = (4.1 * (N - 2*M**0.28 + 5.3)**(0.96 - 1.45*M**0.1)
                     * np.log(gma2)**f2 + 1) / gma2
            gmaF2 = 1.
            fn2 = f * TP2
            GMAS2 = fn2 ** -N * np.exp(-N/M * fn2**-M)
            G0 = (1/M * (N/M) ** (-(N-1)/M) * gamma((N-1)/M)) ** -1
            Sn2 = G0 * Agma2 * GMAS2 * gmaF2
            E2 = 1/16. * HS2**2 * TP2

            #---------------------------------------------------------------------#
            # if swell dominated seas
            #---------------------------------------------------------------------#
        elif sd == 'swell':

            rps = 0.6 + 0.4 * np.exp(-((t_p - Tf)/(0.3 * (25 - Tf)))**2)

            # primary peak
            # disp('primary peak')
            HS1 = rps * h_s
            TP1 = t_p
            gma1 = 35. * (1 + 3.5*np.exp(-h_s)) * (2*np.pi/g * h_s/Tf **
                                                  2)**0.857 * (1. + 6*((t_p - Tf) / (25. - Tf)))
            M = 4.
            f2 = (2.2 * M**-3.3 + 0.57) * N**(0.53 -
                                              0.58*M**0.37) + 0.94 - 1.04*M**-1.9
            Agma1 = (4.1 * (N - 2*M**0.28 + 5.3)**(0.96 - 1.45*M**0.1)
                     * np.log(gma1)**f2 + 1.) / gma1
            fn1 = f * TP1
            if fn1 < 1:
                sig = 0.07
            elif fn1 >= 1:
                sig = 0.09

            gmaF1 = gma1 ** np.exp(-1/(2*sig**2)*(fn1 - 1)**2)
            GMAS1 = fn1 ** -N * np.exp(-N/M * fn1**-M)
            G0 = (1/M * (N/M) ** (-(N-1)/M) * gamma((N-1)/M)) ** -1
            Sn1 = G0 * Agma1 * GMAS1 * gmaF1
            E1 = 1/16. * HS1**2 * TP1

            # secondary peak
            # disp('secondary peak')
            HS2 = np.sqrt(1-rps**2)*h_s
            G0 = (1/M * (N/M) ** (-(N-1.)/M) * gamma((N-1.)/M)) ** -1
            s4 = np.max([0.01, 0.08 * (1. - np.exp(-1/3 * h_s))])
            tmp = ((16. * s4 * 0.4 ** N) / (G0 * HS2**2)) ** (-1./(N-1.))
            TP2 = np.max([2.5, tmp])
            gma2 = 1
            M = 4. * (1 - 0.7 * np.exp(-1/3 * h_s))
            f2 = (2.2 * M**-3.3 + 0.57) * N**(0.53 -
                                              0.58*M**0.37) + 0.94 - 1.04*M**-1.9
            Agma2 = (4.1 * (N - 2*M**0.28 + 5.3)**(0.96 - 1.45*M**0.1)
                     * np.log(gma2)**f2 + 1) / gma2
            gmaF2 = 1.
            fn2 = f * TP2
            GMAS2 = fn2 ** -N * np.exp(-N/M * fn2**-M)
            Sn2 = G0 * Agma2 * GMAS2 * gmaF2
            E2 = 1./16. * HS2**2 * TP2

        # spectrum frequency
        S[fc, 0] = f

        # primary spectrum
        S[fc, 1] = E1 * Sn1

        # secondary spectrum
        S[fc, 2] = E2 * Sn2

    # including factor to correct primary and secondary spectrum to input h_s
    f = S[:, 0]
    a1 = np.trapz(f**0 * S[:, 1], f)
    a2 = np.trapz(f**0 * S[:, 2], f)

    h1 = HS1**2 / (4*np.sqrt(a1))**2
    h2 = HS2**2 / (4*np.sqrt(a2))**2

    # corrected primary and secondary peak (to ensure Hm0 = h_s)
    S[:, 1] = S[:, 1] * h1
    S[:, 2] = S[:, 2] * h2
    S[:, 3] = S[:, 1] + S[:, 2]

    # calculating spectrum moments
    Sf = S[:, 3]
    m0 = np.trapz(f**0 * Sf, f)
    m1 = np.trapz(f**1 * Sf, f)
    m2 = np.trapz(f**2 * Sf, f)

    # calculating statistical parameters
    Hm0 = 4 * np.sqrt(m0)
    Tm01 = m0 / m1
    Tm02 = np.sqrt(m0/m2)

    wave_spectrum['spectrum'] = S
    wave_spectrum['m0'] = m0
    wave_spectrum['m1'] = m1
    wave_spectrum['m2'] = m2
    wave_spectrum['Hm0'] = Hm0
    wave_spectrum['Tm01'] = Tm01
    wave_spectrum['Tm02'] = Tm02

    if w is None:
        return Sf/(2*np.pi), f*2*np.pi
    else:
        return Sf/(2*np.pi)
    
    
    # Pierson-Moskowitz spectrum.
def pierson_moskowitz(h_s, t_p, w):
    """ Input parameters:
    h_s     : Significant wave height [m].
    t_p     : Spectral peak period [s].
    w       : Wave frequencies [rad/s].

    Reference:
    DNVGL-RP-C205 2019 p61.
    """
    w   = np.clip(w, 1e-8, np.max(w))                               # Limit frequencies downwards [rad/s].
    w_p = 2*np.pi/t_p                                               # Peak frequency [rad/s].
    s_w = (5/16)*h_s**2*w_p**4*w**(-5)*np.exp(-5/4*(w/w_p)**(-4))   # Spectral density [m^2.s].

    return s_w, w


# JONSWAP spectrum.
def jonswap2(h_s, t_p, w, gamma=None):
    """ Input parameters:
    h_s     : Significant wave height [m].
    t_p     : Spectral peak period [s].
    w       : Wave frequencies [rad/s].
    gamma   : Peak shape parameter [-].
        
    Reference:
    DNVGL-RP-C205 2019 p62.
    """
    # Peak shape parameter.
    if gamma is None:
        if h_s > 0:
            tp_hs = t_p/np.sqrt(h_s)
        else:
            tp_hs = 1e8
            print("jonswap(): h_s is zero.")
        
        if tp_hs <= 3.6:
            gamma = 5
        elif 3.6 < tp_hs and tp_hs < 5:
            gamma = np.exp(5.75-1.15*tp_hs)
        else:
            gamma = 1 # Default (the JONSWAP spectrum reduces to the Pierson-Moskowitz spectrum).
   
    # Normalizing factor.
    a_g = 0.2/(0.065*gamma**0.803+0.135)

    # Width parameter.
    w_p = 2*np.pi/t_p           # Peak frequency [rad/s].
    sig = 0.07*np.ones(len(w))
    sig[w > w_p] = 0.09         # Width parameter dependent on peak frequency.

    # Modify the Pierson-Moskowitz spectrum.
    s_w = pierson_moskowitz(h_s, t_p, w)
    s_w *= a_g*gamma**np.exp(-0.5*((w-w_p)/(sig*w_p))**2)

    return s_w

