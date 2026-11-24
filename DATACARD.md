# Dataset card for the 1858-1861 Bavarian medical survey (BSB Cgm 6874)

**Publisher:** 13fragments
**Date:** 2026-11-24
**Repository:** `https://github.com/13fragments/bavarian-physikatsberichte`
**Model:** `Kurrent Transcriber 1B` (`https://huggingface.co/13fragments/kurrent-transcriber-1b`, Zenodo DOI `10.5281/zenodo.24342061`, release stack `re-v1`)
**Source collection:** Bayerische Staatsbibliothek (BSB), Munich, call numbers `BSB Cgm 6874(1)` through `BSB Cgm 6874(207)` (`Public Domain Mark 1.0`)
**Verification status:** Full-corpus machine transcription (`26,325` pages) plus LLM-agent image verification (`Agent-checked`) on `226` of `239` canonical districts, `57` folk-medicine accounts, `7` secondary quoted passages, and a `30`-page accuracy sample. Independent review by a professional historical paleographer is open prior to public release.

## 1. Overview

On 21 April 1858, King Maximilian II of Bavaria ordered every royal district physician (*Gerichtsarzt*) to compile a standardized medical, topographic, and ethnographic report (*Physikatsbericht*) covering geography, housing, diet, child-rearing, infant mortality, endemic disease, and folk medicine. The surviving manuscripts for seven of Bavaria's eight historical administrative regions (*Regierungsbezirke*) are preserved at the Bayerische Staatsbibliothek under call number `Cgm 6874` and digitized online by the Munich Digitization Center (MDZ) under `Public Domain Mark 1.0`.

This companion dataset releases three linked layers:

1. **Full-corpus machine transcription** of all `212` digitized `BSB Cgm 6874` volumes (`26,325` archival page images, `25,827` unique non-duplicate pages, `10,231,643` completion tokens).
2. **Volume-clustered `30`-page in-corpus accuracy evaluation** across `30` distinct volumes, reporting both strictly blind-keyed (`4.33%` median `cer_norm`) and ink-adjudicated (`3.45%` median `cer_norm`) metrics under the `Kurrent Pages Benchmark` protocol, along with all reference texts (`eval_sample_references.tar.gz`).
3. **Image-verified structured tables** covering all `239` canonical 1860 districts (separated birth-cohort infant mortality vs. infant share of all deaths, feeding practice, pacifiers, sedatives, and goiter), `57` folk-medicine passages, and a normalized `verified_passages.csv` table indexing every published quotation.

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

- **Oberbayern is absent from `BSB Cgm 6874`.** Reports for Upper Bavaria passed to the *Historischer Verein von Oberbayern* and are held as a deposit in the **Stadtarchiv München** (Munich Municipal Archive; see *Historisches Lexikon Bayerns*, "Physikatsberichte").
- **Collective volumes and catalog discrepancy.** Eleven volumes bundle multiple Lower Franconian or Palatinate jurisdictions into a single shelfmark. We mapped exact sub-district canvas boundaries across all collective volumes. In `BSB Cgm 6874(14)` (`bsb00140582`), the BSB MARCXML catalog lists `Babenhausen` alongside `Baunach`, `Bischofsheim (Rhön)`, and `Brückenau`, but the bound volume contains only those three Lower Franconian reports; `Babenhausen` (Swabia) is bound separately as `BSB Cgm 6874(13a)` (`bsb00140581`).
- **Duplicate archival frames.** Consecutive-frame comparison flagged `498` duplicate or re-shot consecutive frames across `7` volumes, chiefly in `Bissingen` (`BSB Cgm 6874(20)`, `bsb00009735`: `363` frames) and `Lauingen` (`BSB Cgm 6874(100)`, `bsb00009733`: `130` frames), plus `1` each in `Berneck`, `Erlangen (Stadt)`, `Hengersberg`, `Höchstadt an der Aisch`, and `Kempten`. Of those `498` pairs, `493` share an identical processed-image `sent_sha256` hash (`exact_image_hash_and_text`), while `5` are `text_near_duplicate` singleton pairs. Every frame is preserved in `cgm6874_pages.jsonl.gz` for exact canvas alignment and flagged with `duplicate_of_canvas` and `duplicate_same_image_sha256`.

## 3. Transcription stack and corpus audit

Every page image was fetched via the MDZ IIIF Image API (`Public Domain Mark 1.0` verified programmatically per manifest) and transcribed with `Kurrent Transcriber 1B` using the `re-v1` release stack (`vllm==0.23.0`, `transformers==5.13.0`, `pillow==12.3.0`, `numpy==2.4.6`) with `furniture_fp_v16` (`fp-v16`) surround masking. Completeness checks verify exact `1..canvas_count` canvas-number sets per volume with zero missing or duplicate canvas numbers.

| Metric | Value |
| --- | ---: |
| Admitted and completed volumes | `212 / 212` |
| Total page images transcribed | `26,325` |
| Unique non-duplicate pages | `25,827` |
| Flagged consecutive duplicate frames (`exact_hash` / `text_near`) | `498` (`493` / `5`) |
| Non-loop completions (`incomplete == null`) | `26,149` (`99.33%`) |
| Repetition loop-cut pages (`incomplete != null`) | `176` (`0.67%`) |
| Run-stripped pages (`runs_removed == true`) | `143` (`0.54%`) |
| Empty model outputs (`text == ""`) | `264` (`1.00%`) |
| Total completion tokens | `10,231,643` |
| Median per-page inference latency (under batch concurrency) | `8.54 s` |

## 4. In-corpus accuracy evaluation

To measure accuracy on 1858-1861 Bavarian medical Kurrent, we drew a deterministic volume-clustered random sample of `30` text-bearing interior pages across `30` distinct volumes (`seed=18580421`, the royal rescript date). Eligibility required `canvas > 2`, `80` to `450` model-transcribed words, digit share below `0.12`, and non-duplicate status; because eligibility uses model output, blank sheets and catastrophic short/long outputs are excluded from this estimand.

An LLM agent first transcribed each full-resolution IIIF image blind (without viewing model output) and then adjudicated differences word-for-word against the ink (`28,929` reference characters, `4,129` reference words). To guard against adjudication anchoring toward the model, we release both the strictly blind-keyed scores and the adjudicated scores under the exact `Kurrent Pages Benchmark` normalization and alignment protocol (`10,000`-draw bootstrap 95% confidence intervals).

| Slice | Pages | Median `cer_norm` | 95% Bootstrap CI | Median `wer_norm` | Mean `cer_norm` |
| --- | ---: | ---: | --- | ---: | ---: |
| Full sample, strictly blind-keyed | `30` | `4.33%` | `[2.96%, 7.14%]` | `16.51%` | `19.02%` |
| Full sample, ink-adjudicated | `30` | `3.45%` | `[2.54%, 5.98%]` | `15.73%` | `18.27%` |
| Running prose only, ink-adjudicated | `25` | `2.99%` | n/a (`3.19%` blind) | `13.61%` | `4.41%` |

The gap between median (`3.45%`) and mean (`18.27%`, micro `cer_norm = 19.05%`, `mean_nls_norm = 0.867`) comes from five non-prose sheets in the draw (`page_type` recorded per row in `in_corpus_accuracy_eval.csv`): one hand-drawn district map (`Wertingen`, `bsb00009732` canvas `50`, `68.66%`), one ruled two-column trade table where the model emitted HTML table tags (`Fürth`, `bsb00142852` canvas `43`, `217.95%`), and three dense tabular spreads (`Kastl Lit. B`, `Herzogenaurach`, `Ludwigshafen`, `44.17%` to `53.85%`). Across the `25` running-prose pages, adjudicated `cer_norm` spans `0.37%` (`Neumarkt`) to `18.46%` (`Lauf an der Pegnitz`).

## 5. Verified structured tables

Machine transcripts served for corpus-wide candidate discovery, never as unchecked primary evidence. For all `239` canonical jurisdictions, top candidate pages for infant feeding, mortality, sedatives, and goiter were fetched locally and checked by an LLM agent against the archival images (`226` `Agent-checked`; `13` `No-relevant-section` where no infant-feeding or mortality section was retrieved in the initial candidate pass). A post-audit dialect regex pass (`säugen`, `Selbststillen`, `Zulze`, `Saugschlozer`) confirmed `11` of those `13` remain empty and surfaced candidate feeding paragraphs in `Hilpoltstein` (`bsb00137059` canvas `41-42`) and `Immenstadt` (`bsb00060144` canvas `62`), queued for the paleographer review pass.

Of the `239` reports, `191` document infant feeding (`122` predominantly breastfed, `36` mixed or short duration, `23` rarely or not breastfed, and `10` documenting other feeding details without stating breastfeeding prevalence). Among the `226` `Agent-checked` rows, `217` log explicit OCR ink corrections.

To prevent denominator mixing, `verified_bavaria_1860_infant_feeding.csv` and `map_bavaria_1860_infant_feeding.geojson` store birth-cohort mortality (`imr_pct_of_births`, `n = 37`) separately from infant share of all deaths (`infant_share_of_all_deaths_pct`, `n = 18`), accompanied by `numerator_includes_stillbirths`, `is_approximate`, and `age_window` flags. Sensitivity checks in `epidemiology_summary_stats.json` confirm the feeding-mortality gap across strict subsets: `23.0%` (`n = 17`) vs. `40.0%` (`n = 9`) across all birth-cohort rates (`AUC = 0.922`), `24.05%` (`n = 15`) vs. `40.0%` (`n = 7`) on strict `live_births` rows only, and `24.05%` (`n = 15`) vs. `39.45%` (`n = 6`) excluding `Eggenfelden`'s verbal approximate `"fast die Hälfte"`.

## 6. Files and schemas

| File | Description |
| --- | --- |
| `cgm6874_pages.jsonl.gz` | Deterministic (`mtime=0`) gzipped JSONL of all `26,325` pages in volume and canvas order with `duplicate_of_canvas` and `duplicate_same_image_sha256` flags. |
| `cgm6874_volumes.csv` | Catalog of all `212` admitted `BSB Cgm 6874` volumes with shelfmarks, canvas counts, and `PDM 1.0` URIs. |
| `districts_index.csv` | Canonical gazetteer of `239` 1860 Bavarian *Physikatsbezirke* with historical *Regierungsbezirk*, coordinates, and exact sub-volume canvas slices. |
| `verified_bavaria_1860_infant_feeding.csv` | Verified `239`-jurisdiction epidemiology table with separated `imr_pct_of_births` and `infant_share_of_all_deaths_pct` columns, denominator/stillbirth/approximate/age-window flags, MDZ/IIIF links, quotes, translations, and OCR correction logs. |
| `map_bavaria_1860_infant_feeding.geojson` | Point `FeatureCollection` mirroring `verified_bavaria_1860_infant_feeding.csv` with separated mortality properties. |
| `verified_bavaria_1860_folk_medicine.csv` | `57` verified folk-medicine, superstition, and healer passages from `64` checked pages. |
| `verified_passages.csv` | Normalized passage-level evidence table indexing every primary and secondary verified quotation cited in Articles 1 and 2 by stable `passage_id`. |
| `in_corpus_accuracy_eval.csv` & `.json` | Per-page and aggregate accuracy metrics (`cer_dipl`, `cer_norm`, `wer_norm`, `nls_norm`, `blind_cer_norm`, `page_type`) across the `30`-page sample. |
| `eval_sample_references.tar.gz` | Deterministic archive of all `30` blind keyings, `30` ink-adjudicated references, and sample manifests for full evaluation reproducibility. |
| `corpus_audit.json` & `epidemiology_summary_stats.json` | Machine-readable completeness audit and full regional/sensitivity statistics. |
| `DATACARD.md`, `LICENSE-CODE.txt`, `LICENSE-DATA.txt`, `CITATION.cff`, `SHA256SUMS` | Documentation, separated code (MIT) and data (CC BY-SA 4.0) licenses, citation metadata, and SHA-256 checksums. |

## 7. Licensing and attribution

- **Original manuscript images:** Bayerische Staatsbibliothek (Munich), `BSB Cgm 6874(1)`-`Cgm 6874(207)`, `Public Domain Mark 1.0`. Cite `Bayerische Staatsbibliothek`, the individual volume call number, and `bsb_id` when reusing images.
- **Transcriptions, verified tables, and evaluation references:** Released by `13fragments` under `CC BY-SA 4.0` (`LICENSE-DATA.txt`), matching `Kurrent Transcriber 1B` (`10.5281/zenodo.24342061`).
- **Pipeline scripts:** Released by `13fragments` under the `MIT License` (`LICENSE-CODE.txt`).
