# Narration Script — Beyond the Six-Factor Formula: Neutron Leakage, Spectral Effects, and Reactivity Feedback in Compact Space Fission Reactors

**Irais Strong** · Ph.D. student, Nuclear Engineering · Idaho State University · NSEN 6684
Target length: 18:00 · Speaking pace assumed: ~130 words per minute

> Recording notes: each section below is also the speaker notes of the matching slide. Times are targets. Every calculated number comes from `code/run_analysis.py` (see `results/analysis_output.txt`); every KRUSTY number comes from the cited papers. The calculations use idealized benchmark cross sections and are not predictions for any real reactor.

---

## Slide 1 — Beyond the Six-Factor Formula (0:40)

Hi, I'm Irais Strong, a Ph.D. student in nuclear engineering at Idaho State University. My thesis for this presentation is simple. Classical neutron life cycle theory gives us the conceptual foundation for criticality. But compact, fast-spectrum space reactors require a more detailed treatment of neutron transport, leakage, reflector interactions, and temperature-dependent reactivity. I'll spend about two minutes on the classical picture, and the rest of the talk on what has to replace it, using calculations I verified against exact benchmarks and published KRUSTY data.

## Slide 2 — Why Compact Fast Reactors Are Different (1:00)

The motivation is lunar and Martian surface power. Near the lunar equator, night lasts about fourteen Earth days, and NASA's draft requirements for Lunar Reactor-1, as reported this year, call for operation through at least three hundred fifty-four hours of darkness.

Reactors that can be launched are small. KRUSTY, the NASA and DOE ground test in 2018, had a highly enriched uranium core eleven centimeters across and twenty-five centimeters tall. In a core that size, leakage is not a small correction. It is the largest single loss in the neutron balance, and it is what the operators used to control the reactor. That's why the physics in this talk centers on leakage, and on how leakage couples to reflection, energy, and temperature.

## Slide 3 — The Classical Life Cycle in Two Minutes (1:30)

Here is the classical picture we've used in class. Start with a thousand thermal absorptions in fuel and follow them through eta, the fast fission factor, fast non-leakage, resonance escape, thermal non-leakage, and thermal utilization. With these assumed light-water-reactor-like values, the next generation has about one thousand eleven absorptions, so k-effective is about one point zero one.

This framework works because a thermal reactor has two well-separated neutron populations and a moderator that connects them. A fast reactor breaks all three assumptions. There is no moderator, so p and f lose their meaning. Fast and slow populations overlap. And leakage, which the six-factor formula treats as two correction factors, becomes the dominant loss. Even the bookkeeping changes. In a thermal reactor you can ask what fraction of neutrons reach thermal energy. In KRUSTY almost every fission is caused by a neutron that never slowed down much, so that question has no useful answer. So for the rest of the talk I'll work from the general neutron balance at the bottom of the slide: production divided by absorption plus leakage, with leakage written explicitly as a surface term.

## Slide 4 — Generalized Neutron Balance and the k-Eigenvalue Problem (1:40)

Formally, the steady-state transport equation describes the angular flux as a function of position, direction, and energy. Streaming plus collisions on the left balances scattering into that phase-space point plus the fission source on the right. A finite, source-free system generally has no steady solution, so we divide the fission source by a number k and ask which value of k makes a steady solution possible. That is the multiplication eigenvalue problem. In operator form, L psi equals one over k times F psi, and k-effective is the dominant eigenvalue.

In practice we solve it by power iteration. Guess a fission source, transport it for one generation, compute the new source, take the ratio, and repeat until the source shape converges. The plot is my own Monte Carlo code doing exactly that for a published benchmark sphere. The first fifty generations let the source converge. After that, k averages to zero point nine nine nine seven, plus or minus zero point zero zero zero three, against an exact answer of one. The six-factor formula is just a two-group, separable approximation to this eigenvalue. In multigroup form, each energy group has its own leakage, absorption, and scattering into other groups, and the eigenvalue couples all of them. That coupling is what the next slides take apart.

## Slide 5 — Deriving One-Group Diffusion (1:45)

Diffusion theory comes from two approximations to that transport equation. First, integrate over all directions and energies to get a one-group balance between leakage, absorption, and fission. Second, assume the angular flux is only linearly anisotropic. That gives Fick's law: the current equals minus D times the gradient of the flux, with D equal to one over three times the transport cross section.

Substituting gives the one-group diffusion equation. Dividing by D turns it into a Helmholtz equation. For a bare sphere, the fundamental mode is sine of B r over r, and the flux must vanish at an extrapolated radius. That sets the geometric buckling, pi over R-extrapolated, squared. Criticality requires material buckling equal to geometric buckling, which gives k-effective equals k-infinity over one plus L-squared B-squared. The term L-squared B-squared is the ratio of leakage to absorption, so one over one plus L-squared B-squared is the non-leakage probability. The extrapolation distance, about zero point seven one transport mean free paths, comes from the Milne problem. It's the first sign that the boundary is a transport effect diffusion has to patch.

The catch is in the assumptions. Fick's law needs the flux to vary slowly over a mean free path, weak absorption, and distance from boundaries. A compact fast core fails all three.

## Slide 6 — Sensitivity Study: k-effective vs Size and Leakage (1:30)

To test that, I used published one-group cross sections from the Los Alamos LA-13511 analytic benchmark set. I chose them because the exact transport solutions are known, so nothing here is tuned. These are idealized verification constants, not a real reactor.

On the left, the curve is one-group diffusion and the points are Monte Carlo transport, for a bare sphere from four to fourteen centimeters. Diffusion is low at every size. The exact critical radius is seven point four three centimeters, while diffusion predicts seven point nine seven, about seven percent too large. In the table on the right, between forty-five and seventy-five percent of the neutrons leak in the radius range a compact core would occupy. The diffusion error in k shrinks from almost ten percent at one point three mean free paths to under two percent at four and a half. In other words, diffusion's error is set by how many mean free paths fit inside the core. Because one group with isotropic scattering makes k equal k-infinity times the non-leakage probability exactly, the Monte Carlo leakage tally is a direct measurement of what diffusion is approximating. The table on the slide lists every value, so the comparison can be checked line by line.

## Slide 7 — Reflectors from Boundary Conditions (1:30)

A reflector should be treated through boundary conditions, not a multiplier. In two-region diffusion, the core flux is sine of B r over r, and the reflector flux is a hyperbolic sine that vanishes at the extrapolated outer surface. Flux and current must be continuous at the interface, which gives the transcendental equation on the slide. Solving it gives k for any core radius and reflector thickness. Reflector savings is then the reduction in critical radius compared with the bare core.

Using the published water-like reflector constants, transport gives savings of one point zero two, one point two eight, and one point three six centimeters for one, two, and three mean free paths of reflector. Two-region diffusion underestimates the savings by fifteen to twenty-seven percent. The familiar large-core slab formula overestimates it by a factor of almost three to four. Curvature matters in a six-centimeter core. The slab formula assumes a flat flux next to the reflector, and in a core this small the flux is anything but flat. In the exact benchmark configurations, fifteen to nineteen percent of all fissions are caused by neutrons that had already visited the reflector.

## Slide 8 — Transport Check: Where Diffusion Fails (1:30)

Before trusting those comparisons, I verified the Monte Carlo code against five exact LA-13511 solutions. That covers the bare sphere, three reflected spheres, and a two-group sphere. All five come out within about one standard deviation of k equal to one, with a standard deviation around three hundredths of a percent.

Diffusion, evaluated at those same exact critical configurations, gives k between zero point eight eight and zero point nine four. That's six percent low for the bare spheres and ten to twelve percent low for the reflected ones. Diffusion does worse with a thin reflector because the reflector is only one to three mean free paths thick and the interface is close to everything. Ten percent in k is more than fourteen dollars of reactivity for a uranium system, which is why nobody designs a compact fast reactor with one-group diffusion.

The flux plot shows why. At the core surface, the exact flux relative to its value at a quarter radius is zero point one eight. Monte Carlo gives zero point one nine. Diffusion gives zero point two nine, too high by more than half, because Fick's law can't represent the strongly outward-directed angular flux near a vacuum boundary.

## Slide 9 — Spectral Effects (1:20)

Now energy. The published two-group benchmark lets me separate fast and slow neutrons. In an infinite medium, thirty-two percent of the flux is in the fast group. In the critical sphere, forty-five percent of the neutrons that leak are fast. Leakage preferentially removes fast neutrons, so the whole finite core has a harder spectrum than the infinite medium, and it hardens further toward the surface.

That matters when cross sections are collapsed. Collapsing to one group with the infinite-medium spectrum gives a transport critical radius one point one percent too small. Using a leakage-weighted spectrum cuts the error to zero point six percent. In this idealized case, the spectral error is about seven times smaller than diffusion's angular error. That ranking is specific to these constants, but it shows the order to fix things in: transport first, then energy. KRUSTY adds the opposite spectral effect: the published analyses report fission-rate peaking at the core edges, driven by neutrons moderated in the beryllium oxide reflector and returned to the fuel.

## Slide 10 — KRUSTY: Reflector Worth as Reactivity Control (1:30)

KRUSTY shows what leakage dominance means experimentally. Reactivity was controlled by lifting the beryllium oxide radial reflector on the COMET platen. The measured platen worth was about twelve cents per millimeter at startup and about ten point seven later in the test. The central boron carbide rod was worth about four cents per millimeter, roughly one-third as sensitive. A millimeter of reflector motion is worth more than a millimeter of absorber.

To bring the fuel to eight hundred degrees Celsius, the operators inserted about one point four two dollars. The design paper's model gives a fuel temperature defect of minus one hundred forty-eight cents at one thousand ninety-three kelvin, and minus one hundred forty-six cents for all components together. That's my inference from two published numbers, not a measured balance: the reactivity added by the reflector roughly equals the reactivity the hot fuel takes away. The MCNP models predicted the first critical within thirty cents and incremental changes within a few cents, which is the level of fidelity this requires. Compare that with the five to twelve percent errors from diffusion on the previous slides.

## Slide 11 — Decomposing KRUSTY's Negative Feedback (1:45)

Where does that feedback come from? The design paper attributes about ninety-five percent of the net feedback to the fuel. About ninety percent of the fuel feedback comes from thermal expansion and about ten percent from changes in fuel cross sections, which includes Doppler broadening. With ninety-three percent enriched fuel there is little uranium-238, so Doppler is small. The component chart on the left shows something less obvious: the vacuum can and the radial reflector had positive coefficients at their low test temperatures. The authors explain that axial expansion of the vacuum can lowers the fuel relative to the reflector, and that in the beryllium oxide the expansion and cross-section effects balance near six hundred kelvin.

On the right, I estimated the fuel expansion coefficient from first principles. I took the computed sensitivity of k to uniform expansion of the benchmark sphere, times a published uranium-molybdenum expansion coefficient, divided by KRUSTY's beta. That gives about minus zero point four cents per kelvin bare, and minus zero point three six with a reflector. KRUSTY's published expansion share is about minus zero point one seven. The sign and order of magnitude agree. The factor-of-two difference is expected for an idealized sphere instead of a reflected, finite cylinder with a different fuel, so I treat it as a consistency check, not a prediction.

## Slide 12 — Findings: Calculated, Observed, Inferred (1:30)

Here are the findings, kept in three separate categories.

Calculated: diffusion underpredicts k by six to twelve percent in compact benchmark systems and overpredicts the critical radius by about seven percent. Its error scales with core size in mean free paths. Reflector savings from transport are one to one point four centimeters, and the slab formula is off by a factor of three to four. Leakage preferentially removes fast neutrons. In this idealized case, spectral collapse error is about one percent against seven for diffusion.

Observed in KRUSTY: reflector motion was the control, with feedback around two tenths of a cent per degree and passive load following.

Inferred: in compact fast cores, criticality is mostly a question of geometry and leakage. Small dimensional changes are reactivity changes, and feedback signs depend on which component heats. The higher-fidelity path is continuous-energy Monte Carlo, such as OpenMC, with the real geometry, validated against the KRUSTY benchmarks. I've included an OpenMC input as the next step. It hasn't been run yet, so I'm not reporting any results from it. The model is only part of the job: the benchmark comparison is what turns a calculation into evidence.

## Slide 13 — Conclusions (0:50)

Three conclusions. First, the six-factor formula is a special case of the k-eigenvalue problem. It is useful for thinking, but not for small fast cores. Second, leakage, reflection, and spectrum are coupled, and in compact systems one-group diffusion misses them at the five to twelve percent level, which is many dollars of reactivity. Third, KRUSTY shows that this physics is not academic: reflector position controlled the reactor and fuel expansion stabilized it. This is the part of reactor physics that a space reactor makes impossible to ignore. Classical theory is where the analysis starts. Transport, validated against experiments, is where design conclusions have to come from. Thank you.
