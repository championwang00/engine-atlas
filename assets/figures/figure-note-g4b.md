# g4b figures: ea005 and ea002

Both figures follow figure-style-spec.md. The anatomy kit and G are copied verbatim from ea023 (lines 1-1976). Other conventions:
- light theme, a base plate with tone mid
- camera az -58 / el 28, scale taken as the minimum over the full 360° sweep
- exactly one top-left mono `<text>`, speed 55°/s
- window.FIG {play, reset, playing, view, setPhi, set}; ?still, ?embed, ?az, ?el, ?phi; reduced motion; _embed-lite.js

- **ea005, EA-005 Brayton**
  - One crank pin drives a compressor cylinder (-32°) and an expander cylinder (+32°) in a V. The receiver tank sits on a column and the combustion chamber is a box.
  - Pipes: air in, compressor to receiver, receiver to chamber to expander, exhaust. One flow line follows the gas that is moving.
  - Expander: admission at constant pressure for 0-110° after TDC, then cut-off and expansion to 180°, then exhaust. The expander piston is lit while gas pushes it.
  - Label: `BRAYTON · 2 CYL · ADM|EXP|EXH nnn°`.
  - The V layout and the timing are schematic. The real Ready Motor arrangement differs.
- **ea002, EA-002 de Rivaz 1807**
  - Vertical closed-bottom cylinder on a four-wheel cart, hydrogen bladder with a hand valve, and a Volta pile wired to the electrode.
  - Cycle: CHG, IGN, UP (piston lit), then FALL. On the fall the piston and rack turn the pinion and the cart wheels roll.
  - The rack and pinion transmission and the cart proportions are schematic. The spec forbids text in the figure, so this note is the only place that says so.
- Verification (headless Chrome, 720x440): az -58, 0, 90, 180 and -140 × phase 20, 76, 140 and 260. No clipping, no console errors, and exactly one `<text>` in each poster.
