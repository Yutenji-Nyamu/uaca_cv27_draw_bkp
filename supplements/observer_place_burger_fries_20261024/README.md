# N39 observer supplementary frames

Original π0.5, place_burger_fries, N10/H50, batch16. The two trajectories below share the N39 instances: burger 006_hamburg/base3, tray 008_tray/base1 at scale2, fries 005_french-fries/base0. Opposite observer view is captured through get_observer_rgb(), synchronized to the head camera.

- Seed340500, slot7: success. [Contact sheet](previews/contact_seed340500.jpg).
- Seed340700, slot14: success. [Contact sheet](previews/contact_seed340700.jpg).

[Editable two-page Draw.io](previews/observer_candidates.drawio). Each page contains six independent image objects and editable labels. Frames were selected by visible execution stages from the same complete trajectory.

Labels give exact frame and physics-step indices. Per-arm model action projections are in manifest.json; these are geometric approximations with raw residuals preserved locally. Do not reuse the old N39 signal curve with new frames without checking correspondence.

Full head/observer videos, per-action U and four-noise disagreement, original model outputs/noises, denoising chains, observations and controller logs are retained locally. This GitHub package contains selected still frames and figure material only. No Overleaf or existing final-figure changes.
