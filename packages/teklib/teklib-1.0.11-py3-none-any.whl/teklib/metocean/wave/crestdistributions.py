"""
### Wave crest distributions

Several functions returning the probability of exceedence function f(x) 
for the wave crest. Available distributions

* forristall - long crested and short crested distributions
* rayleigh - long crested gaussian seastate
* huang - long crested (provides single realization bounds)
* loads_ocg - short crested distribution with breaking

Note that these are ensemble distributions, so comparing against a single
wave crest distribution may cause misinterpretation. An exception is the
huang(PDSR=True) distribution, which provides a mean, upper 99% and lower 99% 
curve for the probability distribution of a single realization. 
"""
from typing import Iterable, Tuple

import numpy as np
from scipy.optimize import root_scalar

def compute_wavenumber(wi:float, depth:float, g=9.80665)->float:
    """ Returns the wave number k satisfying the first order linear dispersion relation 
        w**2 = gktanh(kh). Same relation for second order Stokes waves.
    """
    # To relax requirement on input allow for both iterable and non-iterable inputs
    sol = root_scalar(lambda k_, d, w: w**2 - g*k_*np.tanh(k_*d), 
                            args=(depth, wi), method='brentq', bracket=[0, 10])
    if not sol.converged: print(f"Period {2*np.pi/wi} is not converged.")
    return sol.root

def forristall(Hm0:float, T1:float, depth:float, dim=2, g=9.80665):
    """
    Returns a probability of exceedence function f(x) for the wave crest of Ref /1/.
    This is 1 - F(x) where F(x) is the cumulative distribution function.

    References:
            
        /1/ Forristall G.Z. Wave Crest Distribution: Observations and Second-Order Theory,
        American Meteorological Society, 1 August 2000.

    This is the most commonly used crest height model and is currently proposed as
    recommended practice in most international codes, such as DNV-RP-C205 (2010)
    and API-RP-2MET (2014). Based on SORWT numerical simulations the Forristall
    model incorporates effects up to a second-order of wave steepness. 
    Thus, it is usually referred to as a second-order model.

    Args:
        Hm0 (float) : Significant wave height (in practice)
        T1 (float): Mean wave period (m0/m1)
        dim (int, optional): 2 = unidirectional sea states (Default)
                             3 = directional sea states 
    """
    s1 = 2*np.pi/g*Hm0/T1**2
    w1 = 2*np.pi/T1
    k1 = compute_wavenumber(w1, depth) # from linear dispersion relation
    urs = Hm0/k1**2/depth**3
    if dim == 2:
        ac = 0.3536 + 0.2892*s1 + 0.1060*urs
        bc = 2 - 2.1597*s1 + 0.0968*urs**2
    else: # 3D
        ac = 0.3536 + 0.2568*s1 + 0.0800*urs
        bc = 2 - 1.7912*s1 - 0.5302*urs + 0.2824*urs**2                
    return lambda x, ac=ac, bc=bc: np.exp( -(x/ac/Hm0)**bc  ) #NOTE: defaults bind at creation

def rayleigh(Hm0:float):
    """
    Returns a probability of exceedence function f(x) for the wave crest of Ref /1/.
    This is 1 - F(x) where F(x) is the cumulative distribution function.

    References:
            
        /1/ Longuet-Higgins, M.S., On the Statistical Distribution of the Heights
        of Sea Waves, 1952
        
    Similarly to the wave height distribution, the Rayleigh crest height model is based
    on the representation of a sea-state as a Gaussian and narrow-banded process.

    Args:
        Hm0 (float) : Significant wave height (in practice)
    """
    return lambda x: np.exp( -8*(x/Hm0)**2 )


def gram_charlier(x:Iterable):
    raise NotImplementedError() 
    
        
def huang(Hm0:float, T1:float, depth:float, PDSR=False, g=9.80665):
    """
    Returns a probability of exceedence function f(x) for the wave crest of Ref /1/.
    This is 1 - F(x) where F(x) is the cumulative distribution function.

    References:
            
        /1/ Huang, Z., Zhang, Yu. Semi-Empirical Single Realizations and Ensemble Crest
        Distributions of Long-Crest Nonlinear Waves, OMAE2018-78192, June 2018

    Although water depth is used in the computation of the Ursell number, this distribution
    is a deep water distribution and becomes ill-conditioned for shallow water depth.
    The single realization limits (PDSR=True) provides a good fit to the spread seen
    in model tests experiments when performing a seeding analysis for a ULS seastate.

    Args:
        Hm0 (float) : Significant wave height (in practice)
        T1 (float): Mean wave period (m0/m1)
        depth (float): Water depth used to compute Ursell number
        PDSR (bool): 
            if True: return the lower, mean, upper distributions for a single realization
            Default: return the ensemble distribution
        
    """
    s1 = 2*np.pi/g*Hm0/T1**2
    k1 = 4*np.pi**2/g/T1**2  # Deep water dispersion eq. used by Huang
    urs = Hm0/k1**2/depth**3
    pa = np.r_[1,s1,s1**2,s1**3,s1**4,urs,urs**2]
    pb = np.r_[1,s1,s1**2,s1**3,s1**4,urs**2]
    if PDSR: # Probability distribution for a single wave realization
        # Mean, lower, upper curves for probability < 1E-2)
        a1 = np.r_[0.2894, 12.3011, -662.6320, 12153.3466, -68031.8045, 0.3779, -3.7904]
        b1 = np.r_[1.5277, 67.2118, -3683.1338, 63759.0846, -336712.3631, -8.1382]
        a2 = np.r_[0.3712,1.0087,-43.0667,567.5292,-1173.1204,0.1276,0.3115]
        b2 = np.r_[2.006,4.841,-321.181,846.332,27223.189,0.832]
        ac1, bc1 = sum(a1*pa), sum(b1*pb)
        ac2, bc2 = sum(a2*pa), sum(b2*pb)
        xlimit = (-np.log(0.01))**(1/bc1)*Hm0*ac1
        mean = lambda x, ac1=ac1, ac2=ac2, bc1=bc1, bc2=bc2, xlimit=xlimit: \
            np.where(x > xlimit, np.exp( -(x/ac1/Hm0)**bc1 ), np.exp( -(x/ac2/Hm0)**bc2) )             
        a1 = np.r_[0.1334, 13.0432, -751.0935, 14727.6571, -87711.0810, 0.0840, -5.2045]    
        b1 = np.r_[0.7965, 44.9229, -2525.6956, 47184.1324, -270084.1075, -13.3160]     
        a2 = np.r_[0.3516,2.3892,-105.4167,1557.3914,-5807.4512,0.0791,0.3550]
        b2 = np.r_[1.620,19.720,-909.665,10465.556,-22952.443,-3.726]
        ac1, bc1 = sum(a1*pa), sum(b1*pb)
        ac2, bc2 = sum(a2*pa), sum(b2*pb)
        xlimit = (-np.log(0.01))**(1/bc1)*Hm0*ac1
        upper = lambda x, ac1=ac1, ac2=ac2, bc1=bc1, bc2=bc2, xlimit=xlimit: \
            np.where(x > xlimit, np.exp( -(x/ac1/Hm0)**bc1 ), np.exp( -(x/ac2/Hm0)**bc2) )             
        a1 = np.r_[0.3752, 9.1269, -446.8393, 7837.5720, -42682.1177, 0.8351, -5.7942,]
        b1 = np.r_[2.4637, 82.5688, -4300.5362, 68857.4691, -337914.7489, 2.5661]
        a2 = np.r_[0.3708,0.9835,-39.9404,598.3819,-2144.4920,0.2427,-0.5379]
        b2 = np.r_[2.212,10.951,-637.673,6707.056,-10244.141,4.505]
        ac1, bc1 = sum(a1*pa), sum(b1*pb)
        ac2, bc2 = sum(a2*pa), sum(b2*pb)
        xlimit = (-np.log(0.01))**(1/bc1)*Hm0*ac1
        lower = lambda x, ac1=ac1, ac2=ac2, bc1=bc1, bc2=bc2, xlimit=xlimit: \
            np.where(x > xlimit, np.exp( -(x/ac1/Hm0)**bc1 ), np.exp( -(x/ac2/Hm0)**bc2) )             
        return (mean,lower,upper)
    else: # Huang's probability distribution for the ensemble
        a1 = np.r_[0.3242, 11.7467, -652.1470, 12308.3001, -70529.2504, 0.3785, -3.8837]
        b1 = np.r_[1.7321,72.7179,-4093.6916,72132.2957,-386504.7502,-9.9594]
        a2 = np.r_[0.3733, 0.9398, -40.0095, 512.0601, -849.0734, 0.1294, 0.2882]
        b2 = np.r_[2.0411, 3.6068,-272.2806,-58.9649,32786.2976,0.9003]
        ac1, bc1 = sum(a1*pa), sum(b1*pb)
        ac2, bc2 = sum(a2*pa), sum(b2*pb)
        xlimit = (-np.log(0.01))**(1/bc1)*Hm0*ac1
        return lambda x, ac1=ac1, ac2=ac2, bc1=bc1, bc2=bc2, xlimit=xlimit: \
            np.where(x > xlimit, np.exp( -(x/ac1/Hm0)**bc1 ), np.exp( -(x/ac2/Hm0)**bc2) ) 

def lowish3():
    pass

def loads_ocg(Hm0:float, T1:float, depth:float, g=9.80665):
    """
    Returns a probability of exceedence function f(x) for the wave crest of Ref /1/.
    This is 1 - F(x) where F(x) is the cumulative distribution function.

    References:
            
        /1/ LOADS JIP, Phase 2, Model Uncertainty, OCG-50-01-21B, Rev. B, June 2021

    This wave crest distribution takes into account higher than second order nonlinearities
    and wave breaking, and is based on an extensive set of model test and field measurements.

    Args:
        Hm0 (float) : Significant wave height (in practice)
        T1 (float): Mean wave period (m0/m1)
        depth (float): Water depth used to compute Ursell number

    Returns (tuple):
        1 - F(x): Probability of exceedance function,
        gamma: Onset of breaking occurs at crest height gamma*Hm0
        P_gamma: Corresponding exceedance probability for breaking waves 
    """

    # Tn = (m0/mn)**(1/n)
    s1 = 2*np.pi/g*Hm0/T1**2
    w1 = 2*np.pi/T1
    k1 = compute_wavenumber(w1, depth) # from linear dispersion relation
    urs = Hm0/k1**2/depth**3

    # Coefficients from Forristall's 3D distribution
    ac = 0.3536 + 0.2568*s1 + 0.0800*urs
    bc = 2 - 1.7912*s1 - 0.5302*urs + 0.2824*urs**2                

    method = "posterior_predictive"
    f = {"medium":(0.08,0.37,0.78),
         "posterior_predictive":(0.10,0.37,0.80)}
    f1,f2,f3 = f[method]

    # GP tail parameters (Equation set 12)
    sigma = 1.4*s1 + f1*urs
    gamma = max(f2*(1+1.7*urs-4.6*urs**2),0.3)*np.math.tanh(k1*depth)/(k1*Hm0)
    delta = f3*np.math.tanh(k1*depth)/(k1*Hm0)
    xi = -sigma/(delta-gamma)   # missing minus on metocean note.
    
    # Compute the nonlinear nondimensional crest height
    theta = 0 # main direction (?) TODO: check shortcrest
    epsilon = 1.04*np.math.cos(3*theta) + 0.26  # metocean note had 2*theta
    mu = 16*ac**3/bc*np.math.gamma(3/bc) - 0.25*(np.math.pi/2)**.5  
    kappa = 0.85  
    X = np.linspace(0, 2.0, 100)  # linear wave height
    Xn = X + (2*mu + kappa*epsilon*mu)*X**2  # nonlinear for equivalent POE

    a = (2*mu + kappa*epsilon*mu)
    b = 1
    c = -gamma
    X_gamma = (-b + (b**2 - 4*a*c)**0.5)/2/a    
    F_gamma = 1 - np.exp(-8*X_gamma**2) # CDF value at distribution boundary
    #Xn_gamma = X_gamma + (2*mu + kappa*epsilon*mu)*X_gamma**2
    #print(X_gamma, Xn_gamma, gamma)
    Yn = np.linspace(0, 2.0, 100)
    Y = (-b + (b**2 + 4*a*Yn)**0.5)/2/a 
    #fig, ax = plt.subplots()
    #ax.set_aspect("equal")    
    #ax.plot(X, Xn)
    #ax.plot(Y, Yn, linestyle='--')
    #plt.show()
    # In the following x is nonlinear
    #h = np.arange(gamma*Hm0,20) 
    #for hi in h:
    #    print(hi, 
    #          (1-F_gamma)*(1 + xi * ( hi/Hm0 - gamma ) / sigma )**( -1/xi ),
    #          1 - ((1-F_gamma)*( 1 - ( 1 + xi*(hi/Hm0 - gamma) / sigma )**(-1/xi) ) + F_gamma)              
    #        )
    #sys.exit()
    return (lambda x, Hm0=Hm0, gamma=gamma, a=a, F_gamma=F_gamma, xi=xi, sigma=sigma: \
            np.where(
                x/Hm0 <= gamma, 
                np.exp(-8*((-1 + (1**2 + 4*a*(x/Hm0))**0.5)/2/a)**2),
                (1-F_gamma)*( 1 + xi*(x/Hm0 - gamma) / sigma )**(-1/xi)
            ), gamma, 1-F_gamma)
            