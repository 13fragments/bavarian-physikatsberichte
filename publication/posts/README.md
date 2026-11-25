# Social-media posts from the 1858-1861 Bavarian medical reports

These are ready-to-edit drafts for short posts and threads. Each one is built on passages from `BSB Cgm 6874` that were checked against the Bayerische Staatsbibliothek page images.

| Post | Topic | Type | Main image |
| --- | --- | --- | --- |
| [01](01_malaria_danube.md) | Malaria on the Danube and its retreat after river regulation | thread | Lauingen, `bsb00009733` canvas 174 |
| [02](02_famine_conscripts.md) | An 1860 test of the 1816-1817 famine cohort: a null result | thread | Erlangen Stadt, `bsb00140610` canvas 68 |
| [03](03_marriage_permits.md) | Marriage permits, illegitimacy, and "Franconian American women" | thread | Marktheidenfeld, `bsb00145124` canvas 179 |
| [04](04_coffee_without_coffee.md) | Chicory and beet "coffee" of the poor | thread | Kronach, `bsb00145114` canvas 123 |
| [05](05_trud_sleep_paralysis.md) | The *Trud* and sleep paralysis | thread | Parsberg, `bsb00003359` canvas 131 |
| [06](06_goiter_iodine.md) | Goiter, cretinism, and the doctor who set iodine aside | quick post with map | `figures/fig_bavaria_1860_goiter_map.png` |
| [07](07_sunday_beer.md) | Water on workdays, 6-8 Maß of beer on Sundays | quick post | Oberdorf, `bsb00146468` canvas 32 |
| [08](08_bramble_tea.md) | Blackberry leaves exported to America, probably to fake green tea | quick post | Klingenberg, `bsb00145112` canvas 101 |
| [09](09_reading_26325_pages.md) | How a 1-billion-parameter model read 26,325 page images | quick post | existing figure or verification viewer |
| [10](10_civil_war_emigration.md) | Emigration fever cools after the American Civil War begins | quick post | Rothenfels, `bsb00145146` canvas 67 |

## Release schedule

Two pieces were released on 2026-11-25: Article 1, "Feeding and Survival in 1860 Bavaria", and the case study "Reading a Kingdom's Medical Survey". The folk medicine article (draft: `publication/article_2_folk_medicine_outline_and_quotes.md`) is not released yet. The plan below publishes at most two posts each week, so that readers are not overwhelmed. Threads go out on Tuesdays and quick posts on Thursdays.

| Date | Post | Reason for this slot |
| --- | --- | --- |
| Tue 2026-12-01 | [09](09_reading_26325_pages.md) Reading 26,325 pages (thread version) | Social version of the case study. Link to it, and do not repeat its launch post. |
| Thu 2026-12-03 | [07](07_sunday_beer.md) Sunday beer | Short and light. |
| Tue 2026-12-08 | [02](02_famine_conscripts.md) Famine conscripts | Ready. Its external context is general knowledge. |
| Thu 2026-12-10 | [08](08_bramble_tea.md) Bramble tea | Quick post. |
| Tue 2026-12-15 | [04](04_coffee_without_coffee.md) Coffee without coffee | Food topic, one week after Post 07. |
| Thu 2026-12-17 | [10](10_civil_war_emigration.md) Civil War emigration | Quick post before the holiday pause. |
| 2026-12-21 to 2027-01-03 | Pause | Holidays, low reach. |
| Tue 2027-01-05 | [06](06_goiter_iodine.md) Goiter and map | Publish the dataset version with the goiter column first (see the dataset issue below). |
| Tue 2027-01-12 | [03](03_marriage_permits.md) Marriage permits | Four weeks after Post 10, which also covers emigration. Confirm the Knodel citation first. |
| Tue 2027-01-19 | [01](01_malaria_danube.md) Malaria | Confirm the external malaria dates first. |
| A few days before the folk medicine article | [05](05_trud_sleep_paralysis.md) *Trud* | Folk belief, so it works as a teaser for the folk medicine article. |

The order follows these rules:

- Posts that need no external checks go first. Posts 06, 03, 01, and 05 each have an open item, so they come later.
- Posts on the same subject are at least one week apart: the emigration posts (10 and 03) and the food posts (07 and 04).
- To publish less, skip the Thursday slots. The result is one post each week, finishing around mid-February 2027.
- The release date of the folk medicine article sets the date of Post 05. Post 01 (willow bark as a fever remedy) can also move next to that article.

## How the quotes were checked

1. A keyword search of the machine transcription (`data/transcripts/`) found candidate pages.
2. For each topic, one Claude Fable 5.2 agent (`claude-fable-5-2`) read the full-resolution page images in enlarged crops and transcribed the quoted passages from the ink. The brief is in [`verification/PROTOCOL.md`](verification/PROTOCOL.md). The logs, one per topic, are in [`verification/`](verification/). They record each correction against the machine text and a confidence level.
3. The drafts quote only passages marked `high` or `medium` confidence. Where a check failed, the draft says so in its status line and leaves the claim out.

The verifying agents are LLMs, like the Gemini agents that checked the dataset tables. Independent review by a professional historical paleographer is still open. Treat these drafts as `Agent-checked`, not as a scholarly edition.

## Before you post

- Read the **Caveats** section of each post. It lists what the physician did not say, which numbers are estimates, and which sentences are modern context that needs a source.
- Lines marked "check before posting" contain external facts (dates, prices, citations) that were not verified in this pass.
- Viewer links use the dataset canvas number as `?page=`. In volumes where the library manifest lists images twice (`bsb00009733` Lauingen, `bsb00009735` Bissingen), the viewer counts canvases, so these links are still correct.
- Credit the images as "Bayerische Staatsbibliothek München, Cgm 6874, Public Domain Mark 1.0" and the transcription as "13fragments, CC BY-SA 4.0".

## Dataset issue found during the checks (closed)

The verified district table had one column, `goiter_cretinism_status`, for two conditions. Uffenheim showed the problem. The table marked it `explicitly_absent` because canvas 21 says cretinism is absent, but canvas 43 calls carrying heavy loads on the head "a not uncommon cause" of goiter in women. One value could not record both statements.

The column is now split into `goiter_status` and `cretinism_status`. Uffenheim has goiter `sporadic_or_localized` and cretinism `explicitly_absent`. The goiter map and Post 06 show goiter only. The release notes are in `DATACARD.md`, section 8, and the evidence for each district is in `data/dataset/goiter_cretinism_status_mapping.csv`.

The split is not yet in a published dataset version. The owner publishes the next version on Zenodo and Hugging Face. Do this before Post 06, because the post links the dataset as the source of the map.
