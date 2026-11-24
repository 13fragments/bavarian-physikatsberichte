# The 1858-1861 Bavarian medical survey (BSB Cgm 6874)

End-to-end harvesting, transcription, accuracy evaluation, and image-verified extraction pipeline for the 1858-1861 Bavarian district medical, topographic, and ethnographic reports (*Medizinisch-topographische und ethnographische Beschreibung der Physikatsbezirke Bayerns*, Bayerische Staatsbibliothek shelfmarks `BSB Cgm 6874(1)` through `BSB Cgm 6874(207)`).

## Summary of outputs

1. **Complete transcription (`212` volumes, `26,325` pages):** Compressed per-volume `JSONL` files under `data/transcripts/`, produced with `Kurrent Transcriber 1B` (`huggingface.co/13fragments/kurrent-transcriber-1b`, `CC BY-SA 4.0`, DOI `10.5281/zenodo.24342061`, release stack `re-v1`). Corpus audit (`data/dataset/corpus_audit.json`) flags `498` double-exposed microfilm frames (`25,827` unique pages).
2. **In-corpus accuracy evaluation (`30` pages, `30` distinct volumes):** Blind image keying plus ink adjudication (`data/eval_sample/references/`), scored with the `Kurrent Pages Benchmark` protocol (`3.45%` median `cer_norm`, `2.99%` across `25` running-prose pages; full per-page table in `data/dataset/in_corpus_accuracy_eval.csv`).
3. **Image-verified structured epidemiology (`239` canonical districts across 7 regions):** `data/dataset/verified_bavaria_1860_infant_feeding.csv`, `data/dataset/map_bavaria_1860_infant_feeding.geojson`, `data/dataset/epidemiology_summary_stats.json`, and `data/dataset/verification_viewer.html`.
4. **Image-verified folk-medicine passages (`57` confirmed accounts):** `data/dataset/verified_bavaria_1860_folk_medicine.csv`.
5. **Publication drafts and cropped figures:** `publication/FACTS.md`, `publication/article_1_infant_feeding_draft.md`, `publication/article_2_folk_medicine_outline_and_quotes.md`, and `publication/figures/`.

## Pipeline scripts

- `scripts/harvest_catalog.py`: Discovers digitized `BSB Cgm 6874` volumes via B3Kat SRU and MDZ IIIF manifests, verifies `Public Domain Mark 1.0`, and writes `data/catalog/volumes.{jsonl,csv}`.
- `scripts/colab_worker.py` and `scripts/deploy_colab.py` / `scripts/prepare_shards.py`: Provisions Google Colab GPU shards running the pinned `re-v1` stack and saves per-volume transcripts under `data/transcripts/`.
- `scripts/audit_corpus.py`: Audits completeness across all `212` volumes and flags consecutive duplicate microfilm frames.
- `scripts/evaluate_corpus_accuracy.py`: Samples `30` stratified pages (`seed=18580421`) and scores verified references with bootstrap `95%` confidence intervals.
- `scripts/district_gazetteer_data.py` and `scripts/extract_epidemiology_candidates.py`: Splits collective volumes into `239` canonical 1860 districts and extracts candidate infant-feeding, mortality, and folk-medicine passages.
- `scripts/build_verification_download_manifest.py` and `scripts/download_iiif_targets.py`: Downloads full-resolution IIIF page images locally for image verification.
- `scripts/compile_verified_datasets.py`: Compiles verified JSON shards into final `CSV`, `GeoJSON`, summary JSON, and `verification_viewer.html`.
- `scripts/build_article_figures.py`: Crops verified manuscript passage strips into `publication/figures/`.
- `scripts/build_zenodo_package.py`: Stages the Zenodo and Hugging Face release bundle in `dist/zenodo_package/` with `SHA256SUMS`.

## Licensing and verification status

- **Original archival images:** Bayerische Staatsbibliothek (Munich), `Public Domain Mark 1.0`.
- **Code, transcriptions, and verified datasets:** `13fragments`, `CC BY-SA 4.0`.
- **Verification note:** All structured records and quotations marked `Agent-checked` (`[A]`) were checked against local BSB IIIF images; independent review by a professional historical paleographer is open before public release.
