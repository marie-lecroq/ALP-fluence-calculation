import numpy as np
from scipy.integrate import quad
from scipy.interpolate import interp1d
import numpy.random as rd


### Experimental and physical constants ###

alpha = 1.0/137.035999084 #Fine structure constant
c = 3.0e8 #Speed of light (in m/s)

d = 51.4*3.08567758149137e19 #Distance from Earth to SN1987A (in m)
Reff = 3.0e10 #Effective radius of the SN below which photons are not released (in m)
ks = 16.8e6 #Effective Debye screening scale (in eV)
C = 2.54e71 #Multiplicative constant in (eV^-1)
T = 30.6e6 #Effective temperature (in eV)

dt = 223.0 #Duration of the measurement (in s)
min_erg, max_erg = 0.0, 5.0e8 #Min. and max. values of the energy (for integrating the spectrum; in eV)
erg_window_lo, erg_window_up = 2.5e7, 1.0e8 #Min. and max. values of the energy (the experimental window; in eV)
number_alps = int(1e7) #Number of particles of fixed m and g in the simulation
# N.B.: according to arXiv:1702.02964, results are stable for number_alps >= 1e7.


### Auxiliary functions ###

# Beta factor in special relativity
def betafactor(m,E):
    return np.sqrt(1.0 - m*m/(E*E))

# ALP decay length (in m) [Eq. (3) in arXiv:1702.02964]
def l_ALP(m,g,E):
    x = 1.0e7/m
    x2 = x*x
    y = 1.0e-19/g
    return 4.0e13 * betafactor(m,E) * (E/1.0e8) * (x2*x2) * (y*y)

# Mass-dependent cross section (in eV^-2) [Eq. (9) in arXiv:1702.02964]
def sigma(m,g,E):
    res = 0.0
    if E > m:
        prefactor = 0.125*alpha*g*g
        if (m < 1.0e5):
            x = 0.25*ks*ks/(E*E)
            res = prefactor * ( (1.0 + x)*np.log(1.0 + 1.0/x) - 1.0 )
        else:
            e2 = E*E
            m2 = m*m
            m4 = m2*m2
            k2 = ks*ks
            bf = betafactor(m,E)
            yp = 2.0*e2*(1.0 + bf) - m2
            ym = 2.0*e2*(1.0 - bf) - m2
            res = prefactor * ( (1.0 + 0.25*k2/e2 - 0.5*m2/e2)*np.log((yp + k2)/(ym + k2)) - bf - (0.25*m4/(k2*e2))*np.log((m4 + k2*yp)/(m4 + k2*ym)) )
    return res

# Energy spectrum of the ALPs (in eV^-1) [Eq. (7) in arXiv:1702.02964]
def spectrum(m,g,E):
    res = 0.0
    if E > 0:
        res = C*E*E*sigma(m,g,E)/(np.exp(E/T) - 1.0)
    return res

# Axion fluence from SN1987A (= naive fluence for one photon per axion) in (cm^-2)
def axion_fluence(m,g):
    res = quad(lambda E : spectrum(m,g,E), min_erg, max_erg)[0]
    return (1.0/(4.0*np.pi*d*d)) * res / 1.0e4

# Compute the CDF for the low-mass energy spectrum:
erg_vals = np.linspace(min_erg, max_erg, num=5001)
cdf_vals = []
# N.B. It is okay to fix the coupling g to a convenient value as it just rescales the spectrum.
norm = quad(lambda E : spectrum(0.0,1.0e-20,E), min_erg, max_erg)[0]
for erg in erg_vals:
    temp = quad(lambda E : spectrum(0.0,1.0e-20,E), min_erg, erg)[0]
    if norm > 0 :
        cdf_vals.append(temp/norm)
    else :
        cdf_vals.append(0.0)
inv_cdf_massless = interp1d(cdf_vals, erg_vals, kind='linear')


### Main functions ###

# Theoretically measured fluence given mass m/eV and ALP-photon coupling g/eV^-1 (in cm^-2)
def expected_photon_fluence(m, g, verbose=0):
    naive_one_photon_fluence = axion_fluence(m,g)
    inv_cdf = inv_cdf_massless
    # Only recalculate CDF from spectrum for heavier axions; otherwise the m = 0 version above is used.
    if (m > 1.0e6):
        cdf_vals = []
        new_max_erg = min(500.0*m,1.5e9)
        n = int((new_max_erg-m)/(0.1*m))+1
        erg_vals = np.linspace(m, new_max_erg, num=n)
        #  N.B. It is okay to fix the value of g as it just rescales the spectrum.
        norm = quad(lambda E : spectrum(m,1.0e-20,E), m, new_max_erg)[0]
        for erg in erg_vals:
            temp = quad(lambda E : spectrum(m,1.0e-20,E), m, erg)[0]
            cdf_vals.append(temp/norm)
        inv_cdf = interp1d(cdf_vals, erg_vals, kind='linear')

    counts = 0

    # Generate random numbers from [0,1] and transform to random energies via the inverse CDF.
    rng_ergs = rd.random_sample(number_alps)
    rng_ergs = inv_cdf(rng_ergs)

    for i in range(number_alps):
        E = rng_ergs[i]
        if (E > m):
            l = l_ALP(m,g,E)
            L1 = rd.exponential(scale=l, size=None)
            if (L1 < d) and (L1 > Reff):
               bf = betafactor(m,E)
               # Draw random angles in the axion rest frame;
               # cos(angle) from [-1,1] (i.e. angle in [0,pi]) and phi from [0,2pi]:
               phi = 2.0*np.pi*rd.random_sample()
               cos_theta = 2.0*rd.random_sample() - 1.0
               sin_theta = np.sin(np.arccos(cos_theta))
               cos_phi = np.cos(phi)
               # Photon 1. Transform angle and energy into the lab frame:
               E1 = 0.5*E*(1.0 + bf*sin_theta*cos_phi)
               if (E1 > erg_window_lo) and (E1 < erg_window_up):
                   angle1 = np.arccos((bf + cos_phi*sin_theta)/np.abs(1.0 + bf*cos_phi*sin_theta))
                   y1 =  L1*np.sin(angle1)
                   L21 = -L1*np.cos(angle1) + np.sqrt(d*d - y1*y1)
                   time1 = (L1/bf + L21 - d)/c
                   if (time1 < dt) and (time1 > 0):
                       counts += 1
               # Photon 2. Transform angle and energy into the lab frame:
               E2 = 0.5*E*(1.0 - bf*sin_theta*cos_phi)
               if (E2 > erg_window_lo) and (E2 < erg_window_up):
                   angle2 = np.arccos((bf + cos_phi*sin_theta)/np.abs(1.0 + bf*cos_phi*sin_theta))
                   y2 =  L1*np.sin(angle2)
                   L22 = -L1*np.cos(angle2) + np.sqrt(d*d - y2*y2)
                   time2 = (L1/bf + L22 - d)/c
                   if (time2 < dt) and (time2 > 0):
                        counts += 1
    lgm, lgg = np.log10(m), np.log10(g)+9.0
    res = naive_one_photon_fluence*counts/float(number_alps)
    if (verbose > 0):
        print('{:.3f} {:.3f} {:.10e}'.format(lgm, lgg, res))
    return np.array([lgm, lgg, res])

# Alternative routine that saves the result for each parameter point to a local/unique file.
# Needs outfile = open('./results_new_{}.txt'.format(rank),'a') and outfile.close() for each rank.
def expected_photon_fluence_checkpoints(m,g,outfile):
    res = expected_photon_fluence(m,g)
    outfile.write('{:.3f} {:.3f} {:.10e}\n'.format( np.log10(m), np.log10(g)+9.0, res ))
