# figure-note-spec-N4

Scope: ea083 ea084 ea085 ea030 ea038 ea039, aligned to figure-style-spec.md and ea023. Each original is backed up as `<key>.pre-spec.html`. Posters were regenerated with `node poster.mjs`.

## ea083 / ea084 / ea085 (inline-4 generator; identical runtime)
- Removed the custom CSS overrides (orange `data-lit`, heavier edges, `.model-base` recolor). Kit light variables only.
- Label: `FX.label` and `LABEL` (bottom, y=426, Chinese tags) replaced with the ea023 `label()` at (16,24). Tags: `TURBO I4 · 72° TILT`, `VTEC · DOHC I4`, `ATKINSON · VVT I4`, plus phase `000°`.
- Camera: pad 26/6 -> 14, el 30 -> 28 (`CFG.el`), az -58. The min-scale scan over 360° is kept. el is clamped to 8–70.
- Highlight: removed `lit` from cam lobes, rockers and valve head/retainer. Only the power-stroke piston crown is lit.
- Motion: 55°/s. `?still` / `?embed` / `?phi` are supported. `FIG.view` and `FIG.setPhi` were added. touch-action is none.

## ea030 / ea038 / ea039 (g8 scene runtime)
- Removed the custom CSS for the hot/air/dark/cut/sig colors and the lbl/lead/ro text.
- Removed the leader-line part labels, the bottom readout (Chinese, including "示意") and the pulse-width chart overlays (`ov`) from the source.
- Added the ea023 base plate (halo, 4 feet, `slabOf` mid with thickness 11, faint inset line), built from `SCENE.bounds` plus 14 on each side.
- Camera is az -58 / el 28 with pad 14. The scale is the minimum over a 360° scan, and the base plate is included in the fit.
- Lines and dots are now `var(--anatomy-lo)` at .6 non-scaling stroke, with no opacity. All scene hex colors are now `lo`.
- Highlight: the `sig`/`hot` class maps to kit `lit` (the firing injector or the spark only). The ea039 pressure-sensor `sig` became plain.
- Speed: scene time is scaled so the phase advances 55°/s (`SCENE.rate`). The label is `EFI · SEQ 1-3-4-2`, `GDI · 200 BAR` or `COMMON RAIL · 1600 BAR`, plus phase.
- `?still/?embed/?az/?el/?phi` are supported. `FIG.play/reset/playing/view/setPhi` are present.

## Checks (headless Chrome, az -58/32/122/212 plus autoplay)
- All 6 keys: no console errors, exactly 1 `<text>`, bbox inside 720×440, `data-lit` ≤ 1, autoplay on and off under `?still`.
