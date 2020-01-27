# Calculation of the expected photon fluence from ALP decays after SN 1987A

Code to calculate the expected fluence from decays of axion-like particles (ALPs) into photons after SN 1987A. Written by Marie Lecroq, Sebastian Hoof, and Csaba Balazs. Results of this code were published as a part of the **GAMBIT CosmoBit** paper.

## Summary

Axion-like particles are produced in supernovae and can subsequently decay into two photons or convert into one photon inside of magnetic fields on their way towards the observer. The non-observation of a such photons from the direction of SN 1987A [[Phys. Rev. Lett. 62, 505 (1989)]](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.62.505) can be used to place limits on the axion-photon coupling. Here, we focus on ALPs with masses of keV to GeV and reproduce and extend the work presented in Ref. [[arXiv:1702.02964]](https://arxiv.org/abs/1702.02964).

## Results

<p align="center">
  <img width="600" height="488" src="figures/exclusion_plot.png">
</p>

In the figure above, we show the limits obtained from using our code. The blue dashed line shows the limits for the range of validity obtained in Ref. [[arXiv:1702.02964]](https://arxiv.org/abs/1702.02964) for comparison. Note that their grid spacing in parameter space is 4x wider than ours (0.2 vs 0.05 dex).

## The code

The code implements a full Monte Carlo simulation without any rescaling factors. We also use a finer binning and perform the calculation in a wider region of parameter space than than Ref. [[arXiv:1702.02964]](https://arxiv.org/abs/1702.02964). We provide a documentation in [the documentation](documentation.pdf). The following Python (code tested with version 3.5.7) packages need to be installed in order to use all features of the code: `numpy`, `scipy`, `mpi4py`, `matplotlib`, and `time`.

As a quick start guide, the file [`functions.py`](functions.py) contains the function `expected_photon_fluence(m, g, verbose=0)`, which computes the expected photon flunce (in cm<sup>-2</sup>) given and ALP mass `m` (in eV) and ALP-photon coupling `g` (in GeV<sup>-1</sup>). A parallel run of the code can be invoked by e.g.

   `mpiexec python run_analysis_mpi.py`

Finally, the Python script [`plot_results.py`](plot_results.py) can be used to generate maps of the photon fluence, likelihood, and accepted fraction of decay photons.

## References

* Experimental data: E. L. Chupp, W. T. Vestrand, and C. Reppin. [&ldquo;*Experimental Limits on the Radiative Decay of SN 1987A Neutrinos*&ldquo;](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.62.505), Phys. Rev. Lett. **62**, 505 (1989)
* Original study: J. Jaeckel, P. C. Malta, and J. Redondo. [&ldquo;*Decay photons from the axionlike particles burst of type II supernovae*&ldquo;](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.98.055032), Phys. Rev. D **98**, 055032 (2018)
* CosmoBit paper: tba
