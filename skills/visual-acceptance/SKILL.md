---
name: visual-acceptance-loop
description: Pre-delivery acceptance recipe for paper figures — live-page screenshots, tiling self-check, vision-judge dispatch templates, and evidence-driven fix discipline.
---

# Visual acceptance loop

Delivery standard is not "looks fine to me" — it is an **independent vision judge** comparing render vs reference at pixel level and returning PASS.

## The three checks

1. **Live page must be screenshotted.** Exported PNGs have blind spots (they bypass on-screen layout/scaling; fit-to-view white-screen bugs only show on the live page). Set the viewport to a user-like window, screenshot, and emit the image for inspection.
2. **Export self-check.** Run `check_tiling.py` (this folder) — half-image diffs near zero mean the capture tiled. Checking file size alone never catches it. And when re-exporting after a fix, **rebuild the inline export page after the edit** (reverse order bakes the stale version into the page).
3. **Vision-judge comparison.** Dispatch with replica path + reference path + criteria + a list of intentional deviations. Fresh figures with no bitmap reference get criteria + an element inventory instead; declare the style contract so taste differences are not flagged as defects.

## Judge dispatch template (a vision-capable subagent that reads image paths)

```
You are the visual acceptance gate ... Compare REPLICA vs REFERENCE:
- replica: <absolute path.png>   (note coordinate system / scale factor)
- reference: <absolute path.png>
## What the figure is   (element inventory / topology so the judge need not guess)
## Acceptance bar       (structural-semantic fidelity + every string + arrow
                        source→target topology + no overflow/overlap/broken lines;
                        explicitly list intentional deviations: "box widened by
                        request — do not flag", "style upgrades — do not flag")
## Your job             (per-item checklist: text / topology / colors / quality;
                        "pixel measurements beat impressions")
Return ONE JSON verdict line per page:
{"page":"...","verdict":"PASS"|"FAIL","issues":[{"severity":"major"|"minor",
 "what":"...","where":"...","evidence":"..."}]}
```

Batch 3–4 figures per judge, several judges in parallel. Re-checks are targeted: only the previous FAILs + regression points, never a full re-run.

## Fix discipline

- Fix **root causes** from the judge's pixel evidence, not spot patches. (Real examples: titles turning black → root cause was CSS overriding SVG presentation attributes; a box off by 33 px → true position recovered from an alignment relation.)
- After fixes, dispatch a targeted re-check. If PASS but minor issues remain, decide whether to polish to zero (do it when the user cares about detail).
- Defects flagged by the user live the same loop: quantify → fix root cause → judge re-check.

## Browser-automation notes

- Every JS call is a fresh kernel: re-bootstrap, list tabs, bind by verified id — never reuse stale handles.
- Cache-bust reloads with `?v=<timestamp>`.
- Occasional screenshot failure ("activity capture failed") → wait 1 s and retry; prefer exact-content-size viewports with plain screenshots over huge viewports.
- **Never trust `screenshot({fullPage: true})` on over-one-screen pages.** Even with a correct viewport it can stitch viewport-sized tiles that repeat the page — a correct-sized PNG whose content is 4 copies (real case, in-app browser). Measure `scrollWidth`/`scrollHeight` via `evaluate`, set the viewport to exactly that (cap 3840×2160), and take a plain no-clip screenshot. Always re-verify with `check_tiling.py`.

## Dark-theme contrast check (before dispatching the judge)

- **1.2 px hairlines lose ~60 % of their theoretical contrast to antialiasing.** A dark-theme table grid drawn `#22304d` on `#111a2e` (theoretical Δ≈50) renders at Δ≤12 and the judge reads the table as "borderless" — it took two fix rounds (`#33507a` still Δ12–22 rendered, `#6288b8` → rendered Δ27–43, line pixels 53–69) to pass.
- Rule: pick line/text colors by **rendered pixel measurement, not the hex math** — scan the exported PNG and require ≥40 gray-level difference for body text and grid lines on their actual background. Self-scan before the judge does (one `PIL/numpy` column-min scan at the expected line x-positions).
