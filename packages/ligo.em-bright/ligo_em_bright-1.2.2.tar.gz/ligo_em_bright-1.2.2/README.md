# ligo.em_bright

This library provides the tools to compute the possibility of merging gravitational-wave binaries to have an electromagnetic counterpart or having a component in the lower mass-gap region. The data products are source properties
- `HasNS`: The mass of at least one of the compact binary coalescence is consistent with a neutron star.
- `HasRemnant`: A non-zero amount of remnant matter remained outside the final compact object (a necessary but not sufficient condition to produce certain kinds of electromagnetic emission such as a short GRB or a kilonova).
- `HasMassGap`: The mass of at least one of the compact binary coalescence is consistent with lower mass-gap region i.e. between 3-5 solar mass.

The `HasNS` and `HasRemnant` quantities depend on, and are marginalized over, several neutron star equations of state (EOS). The marginalization is done using data from [GW170817](https://www.gw-openscience.org/eventapi/html/GWTC-1-confident/GW170817/).
