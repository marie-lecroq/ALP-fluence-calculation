import os
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator
from scipy.interpolate import griddata

script_path = os.path.dirname(os.path.realpath(__file__))

plt.rc('text', usetex=True)
plt.rc('text.latex',
    preamble=r'\usepackage{lmodern}\usepackage[T1]{fontenc}\usepackage{amsmath}\usepackage{amssymb}\usepackage{siunitx}'
)
plt.rc('font', **{'family':'serif', 'size': 8})


def minloc(x0,x1):
    return plt.FixedLocator(np.array([i + np.log10(range(2,10)) for i in range(x0,x1)]).flatten())

def majloc(x0,x1):
    return plt.FixedLocator(np.arange(x0,x1,1.0))

def log10_special_formatter(x, pos, offset=0, is_yaxis=True):
    res = "$10^{%g}$" % (x+offset)
    if np.abs(x+offset) < 3:
        if is_yaxis:
            res = "$%g^{\phantom{0}}$" % (10.0**(x+offset))
        else:
            res = "$%g$" % (10.0**(x+offset))
    return res


# Exclusion curve from [arXiv:1702.02964]
excl_jaeckel18 = np.array([[7.603263,-9.001022], [7.842580,-9.475538], [8.100544,-9.990374],
                           [8.100544,-11.39896], [8.001088,-11.49833], [7.500699,-11.49872],
                           [6.422222,-10.96280], [5.073349,-10.29057], [4.007304,-9.754647],
                           [4.000000,-9.001022], [7.603263,-9.001022]])


# The likelihood; see
eff_area = 63.0 # cm^2
sigma = np.sqrt(1393)/eff_area
def loglike(x):
    y = x/sigma
    return -0.5*y*y


# Import results and interpolate
npoints = 300
lgm, lgg, fluence = np.genfromtxt(script_path+"/../results/SN1987A_DecayFluence.dat", unpack=True)
lgm -= 6
x = np.linspace(lgm.min(), lgm.max(), npoints)
y = np.linspace(lgg.min(), lgg.max(), npoints)
z = griddata((lgm, lgg), fluence, (x[None,:], y[:,None]), method='linear')
z = loglike(z)


fig, ax = plt.subplots(figsize=(3.05,2.55))

plt.contourf(x, y, np.exp(z), cmap='YlOrRd', levels=25, zorder=-9)
cs = plt.colorbar(ticks=[0.2*i for i in range(6)], pad=0.025)
cs.ax.set_ylabel('Profile likelihood', labelpad=12, rotation=270)
cs.ax.tick_params(labelsize=6, length=2, pad=2)
cs.ax.set_ylim(0,1)

ax.contour(x, y, -2.0*z, colors='k', linestyles='-', linewidths=1, levels=[9.0])
ax.set_rasterization_zorder(-1)

ax.plot(excl_jaeckel18[:,0]-6, excl_jaeckel18[:,1], c='b', ls='--', lw=1,
        label=r"Jaeckel \textit{et al.} '18"
)
ax.plot([-1,-1], [0,1], 'k-', lw=1.25, label='Our result')

ax.tick_params(which='both', direction='in',
               bottom=True, top=True, left=True, right=True, pad=6, labelsize=8)
ax.xaxis.set_major_locator(majloc(-2,4))
ax.xaxis.set_minor_locator(minloc(-2,4))
ax.xaxis.set_major_formatter(log10_special_formatter)
ax.yaxis.set_major_locator(majloc(-13,-2))
ax.yaxis.set_minor_locator(minloc(-13,-2))
ax.yaxis.set_major_formatter(log10_special_formatter)

ax.set_title(r'\textsf{GAMBIT::CosmoBit}', loc='right', fontsize=6, pad=2)
ax.set_xlabel(r'ALP mass $m_a$ [MeV]')
ax.set_ylabel(r'ALP-photon coupling $g_{a\gamma}$ [$\text{GeV}^{-1}$]')
ax.legend(frameon=False, handlelength=1.6, handletextpad=0.5, labelcolor='w')

ax.set_xlim([-2,3])
ax.set_ylim([-13,-3])

fig.tight_layout(pad=0.3)
plt.savefig(script_path+"/../results/alp_decay_constraints_sn1987a.pdf")
plt.show()
