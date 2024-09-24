from typing import Iterable, Tuple

import numpy as np
import matplotlib.pyplot as plt
from ..signal_analysis.specpack import specdata
from ..signal_analysis.timetools import find_peaks
from ..signal_analysis.stats import empirical_cdf as ecdf


class IrregularWave():
    """Irregular wave class
    
    Example of use:
    
    import numpy as np
    from teklib.wave_theory.irregular import IrregularWave

    # Specified condition from some test program ('d' is water depth)
    Hm0, Tp, T1, d = 7, 10, 8, 300 # [m], [s], [s], [m]

    # Number of wave seeds
    nseeds = 30
    
    # Wave seed to highlight 
    ifocus = 11

    # Plot the semi-empirical distributions
    fig, ax = IrregularWave.plot_wave_crest_distribution(Hm0, Tp, T1, d, return_ax=True)

    for i in range(nseeds):
        # Read measured or simulated wave elevation from some file
        z, t = np.loadtxt(f"wave_elevation{i:d}.txt")
        # Make an instance
        a_wave = IrregularWave(z, t)
        # Add the empirical distribution to the plot that we want to highlight
        a_wave.add_empirical_crest_distribution(ax, highlight=True if ifocus==i else False, 
                                                label="Empirical" if ifocus==i else None)

    plt.show()
    plt.clf(fig)
    """
    
    def __init__(self,z:Iterable[float],t:Iterable[float],d:float=1E10,g:float=9.80665):
        """Instantiates a irregular wave class based on an inputted

        Args:
            z (Iterable[float]): time series of wave elevation
            t (Iterable[float]): time
            d (float, optional): water depth. Defaults to 1E10 m (deep water)
            g (float, optional): gravity. Defaults to 9.80665 m/s/s
        """
        m0,m1,m2,m4,T1,T2,Tp,Hm0,Sf,f = specdata(z,t)  
        self.m0 = m0
        self.m1 = m1
        self.m2 = m2
        self.m4 = m4
        self.T1 = T1
        self.T2 = T2
        self.Tp = Tp
        self.Hm0 = Hm0
        self.Sf = Sf
        self.f = f
        self.z = z
        self.t = t
        self.g = g
        self.d = d
        self.sp = 2*np.pi/g*Hm0/Tp**2 # steepness parameter

    @staticmethod
    def wave_crest_distribution(Hm0, T1, distribution="forristall2d", g=9.80665, d=1E4):
        """Returns a probability of exceedence function f(x) for the wave crest. This
        is 1 - F(x) where F(x) is the cumulative distribution function.
        
        Note that these are ensemble distributions, so comparing against a single
        wave crest distribution may cause misinterpretation. An exception is the
        HuangPDSR distribution, which provides a mean, upper 99% and lower 99% 
        curve for the probability distribution of a single realization. 

        Args:
            Hm0 (float): Significant wave height (in practice). 
            T1 (float): The mean period. 
            distribution (str, optional): The distribution function. Options include:
            
                "forristall2d": Function given in reference /1/ for a long crested wave
                "forristall3d": Function given in reference /1/ for a short crested wave
                "rayleigh": Rayleigh distributed wave heights (ref /1/). 
                "huangPDSR": Huang's single wave condition distribution for long crested waves (ref /2/)
                "huangPDER": Huang's emsemble wave condition distribution for long crested waves (ref /2/)
                Defaults to "forristall2d". 
                
            g (float, optional): gravitational constant (Default: 9.80665 m/s)
            d (float, optional): water depth (Default: 10000 m [deep water])


            References:
            
            /1/ Forristall G.Z. Wave Crest Distribution: Observations and Second-Order Theory,
            American Meteorological Society, 1 August 2000.
            /2/ Huang, Z., Zhang, Yu. Semi-Empirical Single Realizations and Ensemble Crest
            Distributions of Long-Crest Nonlinear Waves, OMAE2018-78192, June 2018

        Returns:
            hc(x): crest height probability of exceedence function
        """
        from .regular import StokesSecond
        s1 = 2*np.pi/g*Hm0/T1**2
        ss = StokesSecond(height=Hm0, period=T1, depth=d)
        if distribution == "forristall2d" or distribution == "forristall3d":
            k1 = ss.wavenumber # independent of StokesSecond's height
            urs = Hm0/k1**2/d**3
            if distribution == "forristall2d":
                ac = 0.3536 + 0.2892*s1 + 0.1060*urs
                bc = 2 - 2.1597*s1 + 0.0968*urs**2
            else:
                ac = 0.3536 + 0.2568*s1 + 0.0800*urs
                bc = 2 - 1.7912*s1 - 0.5302*urs + 0.2824*urs**2                
            return lambda x, ac=ac, bc=bc: np.exp( -(x/ac/Hm0)**bc  ) #NOTE: defaults bind at creation
        elif distribution == "rayleigh":
            return lambda x: np.exp( -8*(x/Hm0)**2 )
        elif distribution == "huangPDSR" or distribution == "huangPDER":
            k1 = 4*np.pi**2/g/T1**2  # Deep water dispersion eq. used by Huang
            urs = Hm0/k1**2/d**3
            pa = np.r_[1,s1,s1**2,s1**3,s1**4,urs,urs**2]
            pb = np.r_[1,s1,s1**2,s1**3,s1**4,urs**2]
            if distribution == "huangPDSR":
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
            elif distribution == "huangPDER":
                a1 = np.r_[0.3242, 11.7467, -652.1470, 12308.3001, -70529.2504, 0.3785, -3.8837]
                b1 = np.r_[1.7321,72.7179,-4093.6916,72132.2957,-386504.7502,-9.9594]
                a2 = np.r_[0.3733, 0.9398, -40.0095, 512.0601, -849.0734, 0.1294, 0.2882]
                b2 = np.r_[2.0411, 3.6068,-272.2806,-58.9649,32786.2976,0.9003]
                ac1, bc1 = sum(a1*pa), sum(b1*pb)
                ac2, bc2 = sum(a2*pa), sum(b2*pb)
                xlimit = (-np.log(0.01))**(1/bc1)*Hm0*ac1
                return lambda x, ac1=ac1, ac2=ac2, bc1=bc1, bc2=bc2, xlimit=xlimit: \
                    np.where(x > xlimit, np.exp( -(x/ac1/Hm0)**bc1 ), np.exp( -(x/ac2/Hm0)**bc2) ) 
        elif distribution == "loads_ocg":
            s1 = 2*np.pi/g*Hm0/T1**2
            k1 = ss.wavenumber # independent of StokesSecond's height
            urs = Hm0/k1**2/d**3
            # Coefficients from Forristall's 3D distribution
            ac = 0.3536 + 0.2568*s1 + 0.0800*urs
            bc = 2 - 1.7912*s1 - 0.5302*urs + 0.2824*urs**2                
            method = "posterior_predictive"
            f = {"medium":(0.08,0.37,0.78),
                "posterior_predictive":(0.10,0.37,0.80)}
            f1,f2,f3 = f[method]
            # GP tail parameters (Equation set 12)
            sigma = 1.4*s1 + f1*urs
            gamma = max(f2*(1+1.7*urs-4.6*urs**2),0.3)*np.math.tanh(k1*d)/(k1*Hm0)
            delta = f3*np.math.tanh(k1*d)/(k1*Hm0)
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
        else:
            raise NotImplementedError(f"The {distribution} distribution is not implemented")        

    @staticmethod
    def wave_height_distribution(Hm0, Tp, distribution="forristall", gamma=None, d=1E4):
        """Returns a probability of exceedence function f(x) for the wave height. This
        is 1 - F(x) where F(x) is the cumulative distribution function.

        Args:
            Hm0 (float): Significant wave height (in practice). 
            Tp  (float): Spectral peak period (used in imperial distribution to compute peakedness)
            distribution (str, optional): The distribution function. Options include:
            
                "forristall": Forristal distribution of wave heights (ref. /1/). Default
                "rayleigh": Rayleigh distributed wave heights (ref. /2)
                "imperial": Imperial wave distribution for intermediate 
                            and shallow water depths (ref /3/)
                                
            gamma (float, optional): peakedness factor (used in imperial distribution)
            d (float, optional): water depth (used in the imperial distribution)

            References:
            
            /1/ Forristall G.Z. On the Statistical Distribution of Wave Heights in a Storm,
            Journal of Geophysical Research Atmospheres, January 1978.
            /2/ Longuet-Higgins, M.S., On the statistical distribution of heights of sea waves.
            Journal of Marine Research 11, 245–266. 1952
            /3/ Karmpadakis, I., Wave Statistics in Intermediate and Shallow Water Depths,
            Ph.D. Thesis, Department of Civil and Environmental Engineering, Imperial College, 2018
            

        Returns:
            hc(x): wave height probability of exceedence function
        """
        if distribution == "rayleigh":
            return lambda x: np.exp( -2*(x/Hm0)**2 )
        elif distribution == "forristall": # 1978
            return lambda x: np.exp( -2.263*(x/Hm0)**2.126 )   
        elif distribution == "imperial":
            if gamma is None:
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
        else:
            raise NotImplementedError(f"The {distribution} distribution is not implemented")

    @staticmethod
    def plot_wave_crest_distribution(Hm0:float, Tp:float, T1:float, d:float=1E4, return_ax=False, figname:str=None, figsize:Tuple[float]=(10,6)):
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_yscale("log");ax.set_xlim(0,2);ax.set_ylim(1E-6,1);ax.grid(True, which="both")
        ax.set_title(f"Wave crest distribution: Hs={Hm0:.1f}m Tp={Tp:.1f}s T1={T1:.1f}s")
        # Plot semi-empirical distributions
        h = np.arange(0,30) # local crest height variable
        if d > 100: # Huang's distribution seems to become ill-conditioned in shallow water
            f_huangPDSR = __class__.wave_crest_distribution(Hm0, T1, distribution="huangPDSR", d=d, g=9.80665) # single realization distro
            f_huangPDER = __class__.wave_crest_distribution(Hm0, T1, distribution="huangPDER", d=d, g=9.80665)
        f_forristall2d = __class__.wave_crest_distribution(Hm0, T1, distribution="forristall2d", d=d, g=9.80665)
        f_rayleigh = __class__.wave_crest_distribution(Hm0, T1, distribution="rayleigh", d=d, g=9.80665)
        f_loads, gamma, P_gamma = __class__.wave_crest_distribution(Hm0, T1, distribution="loads_ocg", d=d, g=9.80665)
        if d > 100:
            ax.plot(h/Hm0, f_huangPDSR[0](h), color="black",linewidth=2,label="Huang PDSR (mean)")
            ax.plot(h/Hm0, f_huangPDSR[1](h), color="black",linewidth=2,label="Huang PDSR (limits)", linestyle='--')
            ax.plot(h/Hm0, f_huangPDSR[2](h), color="black",linewidth=2, linestyle='--')
            ax.plot(h/Hm0, f_huangPDER(h), color="grey",linewidth=2,label="Huang PDER")
        ax.plot(h/Hm0, f_forristall2d(h), color="green",linewidth=2,label="Forristall")
        ax.plot(h/Hm0, f_rayleigh(h), color="blue",linewidth=2,label="Rayleigh") 
        ax.plot(h/Hm0, f_loads(h), color="magenta",linewidth=2,label="LOADS OCG") 
        ax.scatter([gamma], [P_gamma], color="magenta")
        ax.legend(loc=0)
        ax.set_xlabel("$\eta_c / H_{m0}$  [-]", fontsize=14)
        ax.set_ylabel("POE [-]", fontsize=14)
        if figname is not None: 
            plt.savefig(figname) 
            plt.close(fig)
        else: 
            return (fig, ax)

    @staticmethod
    def plot_wave_height_distribution(Hm0:float=None, Tp:float=None, figname:str=None, figsize:Tuple[float]=(10,6)):
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_yscale("log");ax.set_xlim(0,2.5);ax.set_ylim(1E-6,1);ax.grid(True, which="both")
        ax.set_title(f"Wave height distribution: Measured Hs={Hm0:.1f}m Tp={Tp:.1f}s")
        # Plot semi-empirical distributions
        h = np.linspace(0,2.5*Hm0)
        f_forristall = __class__.wave_height_distribution(Hm0, distribution="forristall")
        f_rayleigh = __class__.wave_height_distribution(Hm0, distribution="rayleigh")
        ax.plot(h/Hm0, f_forristall(h), color="green",linewidth=2,label="Forristall")
        ax.plot(h/Hm0, f_rayleigh(h), color="blue",linewidth=2,label="Rayleigh") 
        ax.legend(loc=0)
        ax.set_xlabel("$H / H_{m0}$  [-]", fontsize=14)
        ax.set_ylabel("POE [-]", fontsize=14)
        if figname is not None: 
            plt.savefig(figname) 
            plt.close(fig)
        else: 
            return (fig, ax)     


    def _instance_wave_crest_distribution(self, distribution="forristall2d", Hm0=None, T1=None):
        """ See staticmethod "wave_crest_distribution" for a description
        
        Returns:
            hc(x): crest height probability of exceedence function
        """
        from .regular import StokesSecond
        Hm0 = Hm0 if Hm0 is not None else self.Hm0
        T1 = T1 if T1 is not None else self.T1    
        return self.__class__.wave_crest_distribution(Hm0, T1, distribution=distribution, g=self.g, d=self.d)
        
            
    def _instance_wave_height_distribution(self, distribution="forristall", Hm0=None):
        """See staticmethod "wave_height_distribution" for a description

        Returns:
            hc(x): wave height probability of exceedence function
        """
        Hm0 = Hm0 if Hm0 is not None else self.Hm0
        return self.__class__.wave_height_distribution(Hm0, distribution=distribution)


    def add_empirical_crest_distribution(self, ax, highlight=True, label=None):
        """Adds instances empirical crest distribution to a probability of exceedance (POE) plot

        Args:
            ax (axes): Matplotlib plot axes
            highlight (bool, optional): highlight this case. Defaults to True.
            label (str, optional): legend label for this case. Defaults to None.

        Returns:
            ax: returns the plot ax (this is likely unnecessary)           
        """
        ix = find_peaks(self.z, global_peaks=True)
        Fe, ze = ecdf(len(self.z[ix])), np.sort(self.z[ix])
        zorder, colour = (1000, 'r') if highlight else (1, 'k')
        if label is None:
            ax.scatter(ze/self.Hm0,1-Fe, color=colour, zorder=zorder)        
        else:        
            ax.scatter(ze/self.Hm0,1-Fe, label="Empirical", color=colour, zorder=zorder)  
            ax.legend(loc=0)      
    

    def add_empirical_height_distribution(self, ax, highlight=True, label=None):
        """Adds instances empirical wave height distribution to a probability of exceedance (POE) plot

        Args:
            ax (axes): Matplotlib plot axes
            highlight (bool, optional): highlight this case. Defaults to True.
            label (str, optional): legend label for this case. Defaults to None.

        Returns:
            ax: returns the plot ax (this is likely unnecessary)           
        """
        # Plot empirical distribution
        ix_max, = find_peaks(self.z, global_peaks=True, maxima=True)
        ix_min, = find_peaks(self.z, global_peaks=True, maxima=False)
        k = 0 if ix_min[0] < ix_max[0] else 1
        zh = [self.z[j] - self.z[i] for i, j in zip(ix_min, ix_max[k:])]
        Fe, ze = ecdf(len(zh)), np.sort(zh)
        zorder, colour = (1000, 'r') if highlight else (1, 'k')        
        if label is None:
            ax.scatter(ze/self.Hm0,1-Fe, color=colour, zorder=zorder)        
        else:        
            ax.scatter(ze/self.Hm0,1-Fe, label="Empirical", color=colour, zorder=zorder)  
            ax.legend(loc=0)      