# Comparison of TICRA GRASP and PyPO physical optics simulations

This repository holds the simulation files and Python notebooks for comparing [TICRA GRASP](https://www.ticra.com/software/grasp/)
and [PyPO](https://github.com/PyPO-dev/PyPO) physical optics simulations of a millimeter-wave astronomical telescope and receiver
beam waveguide.

We use the Submillimeter Array's Cassegrain antenna and frequency independent beam waveguide as a test case to compare
the accuracy and performance of the open-source PyPO package with that of GRASP, which is widely regarded as the 'gold standard'
for Physical Optics simulations.

## SMA Antenna Design

The SMA's Cassegrain antenna is a on-axis system, using a 6m diameter primary with focal ratio of 0.42 and a hyperbolic 350 mm 
diameter secondary mirror that gives a back focal distance of 2.472926 m.  A summary of the parameters of the optics is given
in the following table:

| Parameter | Value | Unit |
| --------- | ----- | ---- |
| Primary Diameter | 6.0 | m |
| Primary Focal Ratio  | 0.42 | |
| Primary Focal Length | 2.520 | m |
| Cassegrain Back Focal Distance | 2.472927 | m |
| Secondary Diameter | 0.350 | m |
| Secondary Distance To Focus (c) | 2.496463 | m |
| Secondary Distance To Vertex (a)  | 2.351026 | m |
| Secondary Eccentricity (e) | 1.06186123 | |
| Equivalent Focal Length | 83.9927 | m |
| Magnification | 33.33043 | |
| Feed Opening Angle | 2.04624 | ° |

### Cassegrain Feed

The SMA uses an aperture-plane fed frequency independent illumination of the primary aperture with an edge taper of -10 dB. This feed arrangement is optimized for interferometery, rather than single-dish operation.  For single-dish illumination, the antenna should be fed from an image plane, such as the Cassegrain focus. Single-dish telescopes typically use -12 dB edge taper, to give the best balance of aperture efficiency and sidelobe level.

In simulations comparing the performance of the two software packages for simulating a single-dish antenna, we illuminate the antenna with either a hybrid-mode feed at the Cassegrain focus, represented by a Bessel pattern illumination of the horn aperture, or by a simple Gaussian beam waist at the Cassegrain focus.  The phase center of the feed is placed at the Cassegrain focus.  The edge-taper of the feed pattern is chosen to be -12 dB in both cases.

## SMA Beam Waveguide Design

