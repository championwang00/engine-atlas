# figure-note-spec-N5

Scope: ea041 ea057 ea058 ea060 ea049 ea087, modified in place to match figure-style-spec.md. Each original is backed up as `<key>.pre-spec.html`. Posters were regenerated with `node poster.mjs`.

## Changes
- **g8 runtime (ea041/057/058/060)**
  - Removed the leader-line labels, the bottom readout and the overlay. Removed the custom CSS colour classes (hot/air/dark/cut/sig) and the text styles. Removed `tabindex`, the dblclick handler and the keyboard handler. Removed the lift ruler from ea041.
  - The `hot` part maps to kit `lit`. All other parts use tone hi, or mid for dark/cut. Particles are drawn as `--anatomy-mid` dots and lines as `--anatomy-lo`, with no colour and no opacity.
  - Added a base plate (slabOf, 11 units thick, tone mid, faint inset outline, feet, no halo) under the scene bounds, with 14 units added on each side. The camera now fits with pad 14 at the minimum scale over a 360° sweep and is centred at (360,220). The default camera is az -58 / el 28.
  - The figure now has one label at (16,24) in the spec style. Animation runs at 55°/s nominal crank angle through a per-figure time factor K: ea060 matches its real crank, ea057 matches its firing cycle, and ea041/058 use a nominal phase.
  - Added `?still`, `?embed`, `?az`, `?el` and `?phi`. `FIG` now has play, reset, playing, view and setPhi.
- **Section-slice runtime (ea049/087)**
  - Rewrote `draw()`: removed the gradient defs, the glows, the sparks, the labels and the coloured inlays. Cavities and inlays now use kit shade-0/1 with `lo` strokes, and lines use `lineSvg` tone lo. Added the same base plate and label.
  - The camera now covers the full 360° at pad 14. Drag now works on both az and el. Speed is 55°/s on the 720° cycle. Added setPhi and view.
  - Unused colour constants are left in the shared scene library, but they are not rendered.

## Checks
Headless Chrome, az -58/32/122/212:
- No console errors.
- Exactly one runtime `<text>`.
- Bounding box inside 720x440.
- FIG API complete.
- Autoplay advances about 55° per second.

## Result
All 6 pass the checks above, so none were restored.

Caveat: in ea049 the block and linkage sit on the plate with no support underneath, so the block appears to float. That comes from the original geometry. Figures are smaller than ea023 because the scene bounds are tall.
