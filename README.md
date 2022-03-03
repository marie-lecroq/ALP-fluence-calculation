# The expected photon fluence from ALP decays after SN 1987A

Code for calculating the expected fluence from decays of axion-like particles into photons after SN 1987A.

Monte Carlo methods written by Marie Lecroq, Sebastian Hoof, and Csaba Balazs for ref. [[1]](#cosmoalp), based on ref. [[2]](#res2).

## Summary

Axion-like particles (ALPs) are produced in supernovae and subsequently decay into two photons or convert into photons inside magnetic fields on their way towards Earth. The non-observation [[3]](#data) of a such photons from the direction of SN 1987A can be used to place limits on the ALP-photon coupling [[4]](#res1). We focus on ALPs with masses of keV to GeV and reproduce and extend the work presented in ref. [[2]](#res2).

## Results

<p align="center">
  <img width="600" height="488" src="results/exclusion_plot.png">
</p>

The figure above shows the 3 &sigma; limit obtained from using our Monte Carlo routines (black line). The blue dashed line shows the limits obtained by ref. [[2]](#res2) for comparison; they only considered ALP masses up to 100 MeV and ALP-photon couplings up to 10<sup>-9</sup> GeV<sup>-1</sup>. Our fluxes tend to be higher than in ref. [[2]](#res2) by a factor of about 1.8 in agreement with ref. [[5]](#update).

## The code

The code implements a full Monte Carlo simulation without any rescaling factors. Details about the theoretical computations and the code can be found in [the documentation](documentation.pdf). The Python code was developed with Python version 3.5.7 and only rely on standard packages such as `numpy` and `scipy`.

The file [`fluence_calc_mc.py`](code/fluence_calc_mc.py ) contains the function `expected_photon_fluence(m, g, verbose=0)`, which computes the expected photon flunce (in cm<sup>-2</sup>) given and ALP mass `m` (in eV) and ALP-photon coupling `g` (in GeV<sup>-1</sup>). A parallel run of the code can be invoked by `mpiexec python run_analysis_mpi.py`.

## References

<a id="cosmoalp">[1]</a> CosmoALP paper.

<a id="res2">[2]</a> J. Jaeckel, P. C. Malta, and J. Redondo. [&ldquo;*Decay photons from the axionlike particles burst of type II supernovae,*&rdquo;](https://doi.org/10.1103/PhysRevD.98.055032) Phys. Rev. D **98**, 055032 (2018), [[arXiv:1702.02964]](https://arxiv.org/abs/1702.02964).

<a id="data">[3]</a>  E. L. Chupp, W. T. Vestrand, and C. Reppin. [&ldquo;*Experimental Limits on the Radiative Decay of SN 1987A Neutrinos,*&rdquo;](https://doi.org/10.1103/PhysRevLett.62.505) Phys. Rev. Lett. **62**, 505 (1989).

<a id="res1">[4]</a>  M. Giannotti, L. D. Duffy, and R. Nita, [&ldquo;*New constraints for heavy axion-like particles from supernovae,*&rdquo;](https://doi.org/10.1088/1475-7516/2011/01/015) JCAP **01** (2011) 015, [[arXiv:1009.5714]](https://arxiv.org/abs/1009.5714).

<a id="update">[5]</a>  A. Caputo, G. Raffelt, and E. Vitagliano, [&ldquo;*Muonic Boson Limits: Supernova Redux,*&rdquo;](https://doi.org/10.1103/PhysRevD.105.035022) Phys. Rev. D **105**, 035022 (2022), [[arXiv:2109.03244]](https://arxiv.org/abs/2109.03244).
