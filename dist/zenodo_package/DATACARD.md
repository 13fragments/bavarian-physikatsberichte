# Dataset card for the 1858-1861 Bavarian medical survey (BSB Cgm 6874)

**Publisher:** 13fragments
**Date:** 2026-11-24
**Model:** `Kurrent Transcriber 1B` (`huggingface.co/13fragments/kurrent-transcriber-1b`, Zenodo DOI `10.5281/zenodo.24342061`, release stack `re-v1`)
**Source collection:** Bayerische Staatsbibliothek (BSB), Munich, call numbers `BSB Cgm 6874(1)` through `BSB Cgm 6874(207)` (`Public Domain Mark 1.0`)
**Verification status:** Automated full-corpus transcription (`26,325` pages) plus agent image verification (`Agent-checked`) on `226` of `239` canonical districts, `57` folk-medicine passages, and a `30`-page stratified accuracy sample. Independent review by a professional historical paleographer is open prior to external release.

## 1. Overview

On 21 April 1858, King Maximilian II of Bavaria ordered every royal district physician (*Gerichtsarzt*) to compile a standardized medical, topographic, and ethnographic report (*Physikatsbericht*) covering geography, housing, diet, child-rearing, infant mortality, endemic disease, and folk medicine. The surviving manuscripts for seven of Bavaria's eight historical administrative regions (*Regierungsbezirke*) are preserved at the Bayerische Staatsbibliothek under call number `Cgm 6874` and digitized online by the Munich Digitization Center (MDZ) under `Public Domain Mark 1.0`.

This companion dataset releases three linked layers:

1. **Full-corpus machine transcription** of all `212` digitized `BSB Cgm 6874` volumes (`26,325` archival page images, `25,827` unique non-duplicate pages, `10,231,643` completion tokens).
2. **Stratified `30`-page in-corpus accuracy evaluation** across `30` distinct volumes, scored with the exact `Kurrent Pages Benchmark` normalization and alignment protocol (`median cer_norm = 3.45%`, `median wer_norm = 15.73%`).
3. **Image-verified structured datasets** covering all `239` canonical 1860 districts (geocoded infant feeding, *Mehlbrei* flour gruel, pacifiers, poppy and alcohol sedatives, first-year mortality rates, and goiter) and `57` image-verified folk-medicine passages.

## 2. Corpus coverage and catalog notes

The Bayerische Staatsbibliothek digitization covers `212` volumes representing `239` canonical 1860 *Physikatsbezirke* across seven historical *Regierungsbezirke*:

- **Unterfranken und Aschaffenburg:** `48` districts
- **Schwaben und Neuburg:** `38` districts
- **Mittelfranken:** `32` districts
- **Niederbayern:** `32` districts
- **Oberfranken:** `32` districts
- **Oberpfalz und Regensburg:** `32` districts
- **Pfalz (Bavarian Palatinate):** `25` districts

Three archival caveats apply to downstream analysis:

- **Oberbayern is absent from `BSB Cgm 6874`.** Reports for Upper Bavaria were retained separately by the Staatsarchiv München rather than transferred to the Bavarian State Library.
- **Collective volumes and catalog discrepancy.** Eleven volumes bundle multiple Lower Franconian or Palatinate jurisdictions into a single shelfmark. We mapped exact sub-district canvas boundaries across all collective volumes. In `BSB Cgm 6874(14)` (`bsb00140582`), the BSB MARCXML catalog lists `Babenhausen` alongside `Baunach`, `Bischofsheim (Rhön)`, and `Brückenau`, but the bound volume contains only those three Lower Franconian reports; `Babenhausen` (Swabia) is bound separately as `BSB Cgm 6874(13a)` (`bsb00140581`).
- **Duplicate microfilm exposures.** Automated consecutive-frame comparison caught `498` duplicate consecutive images across `7` volumes, chiefly in `Bissingen` (`BSB Cgm 6874(20)`, `bsb00009735`: `363` duplicate frames) and `Lauingen` (`BSB Cgm 6874(100)`, `bsb00009733`: `130` duplicate frames), plus `1` each in `Berneck`, `Erlangen (Stadt)`, `Hengersberg`, `Höchstadt an der Aisch`, and `Kempten`. Every duplicate frame is preserved in `cgm6874_pages.jsonl.gz` for exact canvas alignment and flagged with `duplicate_of_canvas`.

## 3. Transcription stack and corpus audit

Every page image was downloaded via the MDZ IIIF Image API (`Public Domain Mark 1.0` verified programmatically per manifest) and transcribed with `Kurrent Transcriber 1B` using the pinned `re-v1` release stack (`vllm==0.23.0`, `transformers==5.13.0`, `pillow==12.3.0`, `numpy==2.4.6`) with `furniture_fp_v16` (`fp-v16`) surround masking.

| Metric | Value |
| --- | ---: |
| Admitted and completed volumes | `212 / 212` |
| Total page images transcribed | `26,325` |
| Unique non-duplicate pages | `25,827` |
| Flagged consecutive duplicate frames | `498` |
| Clean non-loop completions | `26,149` (`99.33%`) |
| Repetition loop-cut pages (`incomplete != null`) | `176` (`0.67%`) |
| Run-stripped pages (`runs_removed == true`) | `143` (`0.54%`) |
| Empty or blank pages | `264` (`1.00%`) |
| Total completion tokens | `10,231,643` |
| Median transcription duration per page | `8.54 s` |

## 4. In-corpus accuracy evaluation

To measure accuracy directly on 1858-1861 Bavarian medical Kurrent, we drew a deterministic stratified sample of `30` pages across `30` distinct volumes (`seed=18580421`, the royal rescript date). Each page was keyed blind from full-resolution IIIF images without viewing model output and then adjudicated word-for-word against the ink (`28,929` reference characters, `4,129` reference words). Scoring used the exact `Kurrent Pages Benchmark` normalization and alignment protocol with `10,000`-draw nonparametric bootstrap confidence intervals.

| Slice | Pages | Median `cer_norm` | 95% Bootstrap CI | Median `wer_norm` | Mean `cer_norm` |
| --- | ---: | ---: | --- | ---: | ---: |
| Full stratified sample | `30` | `3.45%` | `[2.54%, 5.98%]` | `15.73%` | `18.27%` |
| Running prose pages only | `25` | `2.99%` | n/a | `13.61%` | `4.41%` |

The gap between median (`3.45%`) and mean (`18.27%`, micro `cer_norm = 19.05%`, `mean_nls_norm = 0.867`) comes from five non-prose sheets in the random draw: one hand-drawn district map (`Wertingen`, `bsb00009732` canvas `50`, `cer_norm = 68.66%`), one two-column ruled trade table where the model emitted HTML table markup (`Fürth`, `bsb00142852` canvas `43`, `cer_norm = 217.95%`), and three dense tabular or multi-column spreads (`Kastl Lit. B`, `Herzogenaurach`, `Ludwigshafen`, `cer_norm = 44.17%` to `53.85%`). Across the `25` running-prose pages, `cer_norm` ranges from `0.37%` (`Neumarkt`, `bsb00145132` canvas `303`) to `18.46%` (`Lauf an der Pegnitz`, `bsb00143129` canvas `54`). Per-page metrics are in `in_corpus_accuracy_eval.csv`.

## 5. Verified structured tables

Machine transcripts served for corpus-wide discovery, never as unchecked primary evidence. For all `239` canonical jurisdictions, top candidate pages for infant feeding, mortality, sedatives, and goiter were fetched locally and checked directly against the archival images (`226` marked `Agent-checked`; `13` marked `No-relevant-section` where the digitized report omits those topics).

Of the `239` canonical reports, `191` document infant feeding: `122` predominantly breastfed, `36` mixed or short duration, `23` rarely or not breastfed, and `10` documenting other feeding practices without stating breastfeeding prevalence. Across the `26` jurisdictions reporting both feeding status and a birth-denominator first-year mortality rate, median first-year mortality is `23.0%` (`n = 17`) where breastfeeding prevailed versus `40.0%` (`n = 9`) where breastfeeding was mixed, brief, or rare.

First-year infant mortality percentages are strictly separated by denominator (`live_births`, `total_births_incl_stillborn`, or `all_deaths`) in `infant_mortality_denominator` so that death-share percentages are never conflated with birth-cohort mortality rates. Every quoted German passage in `verified_bavaria_1860_infant_feeding.csv` and `verified_bavaria_1860_folk_medicine.csv` logs the exact ink-level corrections made to the machine transcript (`216` district entries include explicit OCR correction notes).

## 6. Files and schemas

| File | Description |
| --- | --- |
| `cgm6874_pages.jsonl.gz` | All `26,325` pages in deterministic volume and canvas order. Fields: `bsb_id`, `volume_number`, `district`, `canvas_number`, `canvas_label`, `iiif_image_url`, `mdz_page_url`, `width`, `height`, `text`, `raw_text`, `duplicate_of_canvas`, `incomplete`, `loop_rule`, `runs_removed`, `completion_tokens`, `sent_sha256`, `painted_share`. |
| `cgm6874_volumes.csv` | Catalog of all `212` admitted `BSB Cgm 6874` volumes with shelfmark numbers, canvas counts, ethnography start canvases, and `PDM 1.0` license URIs. |
| `districts_index.csv` | Canonical gazetteer of `239` 1860 Bavarian *Physikatsbezirke* with historical *Regierungsbezirk*, jurisdiction type, coordinates, shelfmarks, and exact sub-volume canvas ranges. |
| `verified_bavaria_1860_infant_feeding.csv` | Verified structured epidemiology table across all `239` jurisdictions, including breastfeeding, *Mehlbrei*, pacifiers, poppy/opiate and alcohol sedatives, mortality with explicit denominator, goiter, direct MDZ/IIIF links, verified German quotes, English translations, and OCR correction logs. |
| `map_bavaria_1860_infant_feeding.geojson` | Point `FeatureCollection` mirroring `verified_bavaria_1860_infant_feeding.csv` for interactive web cartography. |
| `verified_bavaria_1860_folk_medicine.csv` | `57` verified folk-medicine, superstition, and quackery passages with category tags, coordinates, MDZ/IIIF links, verified German quotes, translations, and OCR correction logs. |
| `in_corpus_accuracy_eval.csv` | Per-page accuracy scores (`cer_dipl`, `cer_norm`, `cer_norm_lc`, `wer_norm`, `nls_norm`) across the `30`-page stratified sample. |
| `DATACARD.md` | This dataset documentation file. |
| `SHA256SUMS` | SHA-256 integrity checksums for every file in the package. |

## 7. Licensing and attribution

- **Original manuscript images:** Bayerische Staatsbibliothek (Munich), `BSB Cgm 6874(1)`-`Cgm 6874(207)`, `Public Domain Mark 1.0`. Please cite the holding institution (`Bayerische Staatsbibliothek`) and the individual volume call number and `bsb_id` when reusing images.
- **Transcriptions, structured annotations, and evaluation tables:** Released by `13fragments` under `Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)`, matching `Kurrent Transcriber 1B` (`10.5281/zenodo.24342061`).
