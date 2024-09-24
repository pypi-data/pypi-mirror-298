"""
### Wave crest distributions

Several functions returning the probability of exceedence function f(x) 
for the wave crest. Available distributions

* forristall - long crested and short crested distributions
* rayleigh - long crested gaussian seastate
* imperial - 

"""
from typing import Iterable, Tuple
from enum import Enum, auto

from ...signal_analysis.specpack import specdata
from ...signal_analysis.timetools import find_peaks
from ...signal_analysis.stats import empirical_cdf as ecdf

import numpy as np
from scipy.optimize import root_scalar

   

def compute_wavenumber(wi:float, depth:float, g=9.80665)->float:
    """ Returns the wave number k satisfying the first order linear dispersion relation 
        w**2 = gktanh(kh). Same relation for second order Stokes waves.
    """
    from scipy.optimize import root_scalar
    # To relax requirement on input allow for both iterable and non-iterable inputs
    sol = root_scalar(lambda k_, d, w: w**2 - g*k_*np.tanh(k_*d), 
                            args=(depth, wi), method='brentq', bracket=[0, 10])
    if not sol.converged: print(f"Period {2*np.pi/wi} is not converged.")
    return sol.root

def forristall(Hm0:float):
    """
    Returns a probability of exceedence function f(x) for the wave height of Ref /1/.
    This is 1 - F(x) where F(x) is the cumulative distribution function.

    References:        
        /1/ Forristall G.Z. On the Statistical Distribution of Wave Heights in a Storm,
            Journal of Geophysical Research Atmospheres, January 1978.
        
    Args:
        Hm0 (float) : Significant wave height (in practice) 
    """
    
    return lambda x: np.exp( -2.263*(x/Hm0)**2.126 )   

def rayleigh(Hm0:float):
    """
    Returns a probability of exceedence function f(x) for the wave height of Ref /1/.
    This is 1 - F(x) where F(x) is the cumulative distribution function.

    References:        
        /1/ Longuet-Higgins, M.S., On the statistical distribution of heights of sea waves.
            Journal of Marine Research 11, 245–266. 1952
    
    Args:
        Hm0 (float) : Significant wave height (in practice)
    """
    
    return lambda x: np.exp( -2.263*(x/Hm0)**2.126 )   


def rayleigh(Hm0:float, Tp:float, gamma:float=None, d:float=1E4):
    """
    Returns a probability of exceedence function f(x) for the wave height of Ref /1/.
    This is 1 - F(x) where F(x) is the cumulative distribution function.

    References:        
        /1/ Karmpadakis, I., Wave Statistics in Intermediate and Shallow Water Depths,
            Ph.D. Thesis, Department of Civil and Environmental Engineering, Imperial College, 2018
             
    Args:
        Hm0 (float) : Significant wave height (in practice)
    """
    if gamma is None: # use DNV-RP-C205
        f = Tp/Hm0**0.5
        if f <=3.6: gamma = 5.0
        elif f >= 5: gamma = 1.0
        else: gamma = np.exp(5.75-1.15*f)
    #gamma = max(1.0, 42.2*(2*np.pi*Hm0/9.80665/Tp**2)**(6/7))
    x = [-0.605022255841400, -0.055419059188722, 0.006343927287413, 
        -0.000434704468196, 0.000012702183100]      
    rho = sum([gamma**i * xi for i, xi in enumerate(x)])
    Hrms = 0.5316 * (1-rho)**0.5 * Hm0 - 0.03776 # rms wave height
    shape = 0.032*np.exp(10.02*Hrms/d)+2
    scale = np.math.gamma(2/shape+1)**(shape/2)
    return lambda x: np.exp(-scale*(x/Hrms)**shape) 
    
