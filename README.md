# The 1858-1861 Bavarian medical survey (BSB Cgm 6874)

End-to-end harvesting, transcription, accuracy evaluation, and image-verified extraction pipeline for the 1858-1861 Bavarian district medical, topographic, and ethnographic reports (*Medizinisch-topographische und ethnographische Beschreibung der Physikatsbezirke Bayerns*, Bayerische Staatsbibliothek shelfmarks `BSB Cgm 6874(1)` through `BSB Cgm 6874(207)`).

**Dataset release:** version `0.9.0-pre-paleographer-review`, Zenodo DOI `10.5281/zenodo.24523214` (`https://doi.org/10.5281/zenodo.24523214`), Hugging Face `https://huggingface.co/datasets/13fragments/bavarian-physikatsberichte`. Cite all versions with the concept DOI `10.5281/zenodo.24523213`.

## Summary of outputs

1. **Complete transcription (`212` volumes, `26,325` pages):** Compressed per-volume `JSONL` files under `data/transcripts/`, produced with `Kurrent Transcriber 1B` (`https://huggingface.co/13fragments/kurrent-transcriber-1b`, `CC BY-SA 4.0`, DOI `10.5281/zenodo.24342061`, release stack `re-v1`). Corpus audit (`data/dataset/corpus_audit.json`) verifies exact `1..canvas_count` sequences and flags `498` consecutive duplicate frames (`493` exact image-hash duplicates + `5` text near-duplicates; `25,827` unique pages).
2. **In-corpus accuracy evaluation (`30` pages, `30` distinct volumes):** LLM-agent blind image keying by Gemini 4 Carbon (High) (`4.33%` median `cer_norm`) plus word-for-word ink adjudication (`3.45%` median `cer_norm`, `2.99%` on `25` running-prose sheets) under the `Kurrent Pages Benchmark` protocol (`data/dataset/in_corpus_accuracy_eval.{csv,json}`).
3. **Image-verified structured epidemiology (`239` canonical districts across 7 regions):** `data/dataset/verified_bavaria_1860_infant_feeding.csv` and `map_bavaria_1860_infant_feeding.geojson` (separating `imr_pct_of_births` from `infant_share_of_all_deaths_pct` with stillbirth/approximate/age-window flags), `data/dataset/epidemiology_summary_stats.json` (strict sensitivity slices + Mann-Whitney `AUC = 0.922`), and `data/dataset/verification_viewer.html`.
4. **Passage-level evidence and folk-medicine tables:** `data/dataset/verified_bavaria_1860_folk_medicine.csv` (`57` verified accounts) and `data/dataset/verified_passages.csv` (every primary and secondary quotation cited in Articles 1 and 2).
5. **Publication drafts and figures:** `publication/FACTS.md`, `publication/article_1_infant_feeding_draft.md`, `publication/article_2_folk_medicine_outline_and_quotes.md`, and `publication/figures/` (eight cropped manuscript strips plus the rendered archival map `fig_bavaria_1860_feeding_map.png`).

## Pipeline scripts

- `scripts/harvest_catalog.py`: Discovers digitized `BSB Cgm 6874` volumes via B3Kat SRU and MDZ IIIF manifests, verifies `Public Domain Mark 1.0`, and writes `data/catalog/volumes.{jsonl,csv}`.
- `scripts/colab_worker.py`, `scripts/deploy_colab.py`, and `scripts/prepare_shards.py`: Provisions Google Colab GPU shards running the `re-v1` stack (supports `KURRENT_MODEL_REVISION` pinning) and saves per-volume transcripts under `data/transcripts/`.
- `scripts/audit_corpus.py`: Validates exact `1..canvas_count` sets across all `212` volumes and distinguishes exact image-hash duplicates from text near-duplicates.
- `scripts/evaluate_corpus_accuracy.py`: Draws a `30`-page volume-clustered random sample (`seed=18580421`) and scores both blind keyings and ink-adjudicated references with bootstrap `95%` confidence intervals.
- `scripts/district_gazetteer_data.py` and `scripts/extract_epidemiology_candidates.py`: Splits collective volumes into `239` canonical 1860 districts and extracts candidate infant-feeding, mortality, and folk-medicine passages using dialect-tolerant patterns.
- `scripts/build_verification_download_manifest.py` and `scripts/download_iiif_targets.py`: Downloads full-resolution IIIF page images locally for image verification.
- `scripts/compile_verified_datasets.py`: Validates all `239` district shards against `districts_index.json` and builds the final `CSV`, `GeoJSON`, `verified_passages.csv`, sensitivity JSON, and `verification_viewer.html`.
- `scripts/build_article_figures.py` and `scripts/render_bavaria_map.py`: Generates cropped manuscript strips and the static archival map under `publication/figures/`.
- `scripts/build_zenodo_package.py`: Deterministically (`mtime=0`) stages the complete Zenodo and Hugging Face bundle in `dist/zenodo_package/` from a strict required allowlist with `SHA256SUMS`.

## Licensing, archival coverage, and verification status

- **Archival coverage:** `BSB Cgm 6874` covers seven of Bavaria's eight historical *Regierungsbezirke*. Upper Bavaria (*Oberbayern*) passed to the *Historischer Verein von Oberbayern* and is preserved as a deposit in the **Stadtarchiv München**.
- **Original archival images:** Bayerische Staatsbibliothek (Munich), `Public Domain Mark 1.0`.
- **Pipeline code:** `MIT License` (`LICENSE-CODE.txt`).
- **Transcriptions, verified tables, and evaluation references:** `13fragments`, `CC BY-SA 4.0` (`LICENSE-DATA.txt`; citation metadata in `CITATION.cff`).
- **Verification note:** All structured records and quotations marked `Agent-checked` (`[A]`) were checked by LLM agents against local BSB IIIF images: Gemini 4 Carbon (High) for the first pass and Gemini 4 Neon (XHigh) for re-checks and post-audit corrections, run in Google's Antigravity CLI; independent review by a professional historical paleographer is still open. Corrections from that review will appear in a later version.
