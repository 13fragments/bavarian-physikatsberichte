# Post 9: A small model read 26,325 page images

- **Type:** quick post (method and dataset).
- **Status:** ready to post. This is the social version of the case study "Reading a Kingdom's Medical Survey" (13fragments.com, published 2026-11-25). Link to it, and do not repeat the launch post for it. Every number comes from `publication/FACTS.md`, `data/dataset/corpus_audit.json`, and `data/dataset/in_corpus_accuracy_eval.json`. No new quotation, so no image check is needed.
- **Image:** a page of Kurrent next to its transcription. Use an existing figure from `publication/figures/` (for example `fig_roggenburg_schnaps_pacifier.jpg`) or a screenshot of `data/dataset/verification_viewer.html`.

## Single post

In 1858 the Bavarian interior ministry ordered every district physician to describe his district: food, housing, disease, superstition. The 212 surviving volumes were scanned as 26,325 page images. A 1-billion-parameter model read all of them. The text is now open data.

## Thread

1. In 1858 the Bavarian interior ministry ordered every district physician to describe his district: food, housing, child care, disease, superstition. The 212 surviving volumes were scanned as 26,325 page images, almost all in Kurrent, the old German cursive few can still read.

2. We ran Kurrent Transcriber 1B, a 1-billion-parameter handwriting-recognition model, over every page. It wrote 10.2 million tokens of text. The whole run cost about 33 Google Colab compute units.

3. How good is it? On a random sample of 30 pages from 30 volumes, the median character error rate was 3.45%, measured against a reference text keyed by an LLM agent, not by a human. On running prose it was 2.99%: about three wrong characters in a hundred.

4. Tables and maps are another story. On one ruled table the model invented HTML markup, and the error rate passed 200%. A machine transcript is a search index, not evidence.

5. So every quotation we publish is checked against the page image. Of 226 district entries we checked, 217 needed at least one correction to the machine reading. Typical slips: *Schnaps* read as *Schmack*, *Mohnköpfen* (poppy heads) as *Mohntöpfen* (poppy pots).

6. Everything is open: the page images (public domain, Bayerische Staatsbibliothek), the full transcription and checked tables (CC BY-SA 4.0). Zenodo: https://doi.org/10.5281/zenodo.24523214 · Hugging Face: https://huggingface.co/datasets/13fragments/bavarian-physikatsberichte

7. The full story of the run, the accuracy test, and the checks: https://13fragments.com/blog/bavarian-medical-survey/

## Caveats

- "About 33 compute units" is the drop in the Colab account balance across the run (1,437.29 to 1,404.69). It is not a per-machine receipt. If you want a dollar figure, check the current Colab price per compute unit before you post it.
- The 30-page reference texts were keyed and adjudicated by an LLM agent, not by a human. The error rates measure agreement with that reference. A professional paleographer review is still open.
- 26,325 is the number of page images. It includes 498 duplicate or re-shot frames, so the volumes hold 25,827 distinct pages (`publication/FACTS.md`).
- Upper Bavaria is missing from this collection. Its reports are in the Stadtarchiv München.
