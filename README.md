# Calculation of the expected fluence from axion-photon decays after SN 1987A

Code to calculate the expected fluence from axion-photon decays after SN 1987A by Marie Lecroq, Sebastian Hoof, and Csaba Balazs. Results of this code were published as a part of the **GAMBIT CosmoBit** paper.

## Summary

Axions are expected to be produced in supernovae and can subsequently e.g. decay into two photons or convert into one photon in a magnetic field on their way towards an observer. The non-observation of a such photons from the direction of SN 1987A [[Phys. Rev. Lett. 62, 505 (1989)]](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.62.505) can be used to place limits on the axion-photon coupling. Here, we focus on keV to GeV ALPs and reproduce and extend the work presented in Ref. [[arXiv:1702.02964]](https://arxiv.org/abs/1702.02964).

## Results

<p align="center">
  <img width="600" height="488" src="figures/exclusion_plot.png">
</p>

In the figure above, we show the limits obtained from using our code. The blue dashed line shows the limits for the range of validity obtained in Ref. [[arXiv:1702.02964]](https://arxiv.org/abs/1702.02964) for comparison. Note that their grid spacing in parameter space is 4x wider than ours (0.2 vs 0.05 dex).

## The code

Decription of the code in words. Say that we conduct a 'full' MC simulation without any rescaling factors and finer binning. More detailled description in the CosmoBit paper and as a PDF in the repo?

## References

* Experimental data: E. L. Chupp, W. T. Vestrand, and C. Reppin. [&ldquo;*Experimental Limits on the Radiative Decay of SN 1987A Neutrinos*&ldquo;](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.62.505), Phys. Rev. Lett. **62**, 505 (1989)
* Original study: J. Jaeckel, P. C. Malta, and J. Redondo. [&ldquo;*Decay photons from the axionlike particles burst of type II supernovae*&ldquo;](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.98.055032), Phys. Rev. D **98**, 055032 (2018)
* CosmoBit paper:
