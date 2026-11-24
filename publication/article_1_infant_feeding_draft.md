# The line along the Danube: infant feeding and survival in 212 Bavarian doctors' reports from 1860

- **Target:** `13fragments` blog (flagship research report from the complete `BSB Cgm 6874` transcription run).
- **Status:** First draft for owner review (`2026-11-24`). Every `[A]` fact, count, and German quotation comes from `publication/FACTS.md` and was checked against the original Bayerische Staatsbibliothek archival images. Independent review by a professional historical paleographer is open before publication; remove `[A]` tags once that review passes.
- **Companion dataset:** `dist/zenodo_package/` (`26,325` transcribed pages, `239`-district verified epidemiology table, GeoJSON map layer, `57` verified folk-medicine passages, and `30`-page accuracy evaluation).
- **Figures:** `publication/figures/fig_roggenburg_schnaps_pacifier.jpg`, `fig_greding_mieder_natural_experiment.jpg`, `fig_landshut_mieder_nipples.jpg`, `fig_roggenburg_syphilis_pacifier.jpg`, `fig_landstuhl_poppy_decoction.jpg`, `fig_bischofsheim_schnaps_opium.jpg`.

---

**Subtitle:** In 1858, Bavaria ordered every royal district physician to report how mothers fed their newborns. Reading all 26,325 manuscript pages maps a sharp cultural boundary where first-year infant mortality nearly doubled.

In 1860, the royal district physician in Roggenburg, a rural Swabian jurisdiction south of the Danube, underlined a heading in his official report and added three exclamation marks. First-year infants in his district, he wrote, rarely received breast milk. Families fed newborns coarse, paste-like flour gruel (*Mehlbrei*) and bread softened in water or pre-chewed and tied into a cloth rag (*Schnullerbrod*). In heavy-drinking households, parents dipped that pacifier straight into schnapps "so that they should sleep faster and longer!" (the manuscript ends the sentence with three exclamation marks). [A]

Two hundred kilometers to the north, inside the very same kingdom, the picture reversed. In Landstuhl in the Palatinate, and in Uffenheim in Middle Franconia, district physicians reported that nearly every mother nursed her child through the first year and often well into the second. In Landstuhl, `16.3%` of all births ended in first-year death (including stillbirths); in Uffenheim, `17.6%` of live-born babies died before age one. [A] Across Swabia and Lower Bavaria, physicians in district after district recorded `40%` to `50%` of newborns dying inside twelve months. [A]

*[Figure 1: `figures/fig_roggenburg_schnaps_pacifier.jpg` - Roggenburg (`BSB Cgm 6874(153)`, `bsb00007355`, page 15). Crop above verified reading: "Allein das Aller Empörendste ist, daß in solchen versoffenen Familien schon die Säuglinge an dieses gefährliche Getränk gewöhnt, u ihre Schnuller in Schnaps eingetaucht werden, damit sie schneller u länger schlafen sollen! [triple exclamation mark in ink] ... Die erste Ernährung der Kinder im 1ten Lebensjahre geschieht in der Regel durch grobe u kleisterartige Mehlbreie, durch in Wasser aufgeweichtes oder durch Kauen verkleinertes u in einen Fleck gebundenes Schnullerbrod u nur in den seltensten Fällen durch Muttermilch."]*

Historians of European demography have known about Bavaria's high nineteenth-century infant mortality since contemporary statisticians began tabulating parish deaths. What stayed locked away was the ground-level testimony written by the doctors themselves across hundreds of individual districts. Most of those manuscripts have never been published in full, and almost every page is written in *Kurrent*, the pointed German cursive that few modern readers can decipher without specialist training.

## One royal order, 26,325 pages

On 21 April 1858, King Maximilian II's interior ministry sent a detailed questionnaire to every district physician (*Gerichtsarzt*) in the Kingdom of Bavaria. Each doctor was instructed to write a medical, topographic, and ethnographic description (*Physikatsbericht*) of his district: soil, weather, housing, clothing, diet, infant care, local illnesses, mortality tables, and popular superstition.

For seven of Bavaria's eight historical administrative regions (*Regierungsbezirke*), `212` bound manuscript volumes survive at the Bayerische Staatsbibliothek in Munich under call number `BSB Cgm 6874` (`Public Domain Mark 1.0`). Upper Bavaria (*Oberbayern*) is not part of this series because its reports went to the Staatsarchiv München. Once eleven collective volumes from Lower Franconia and the Palatinate are split along their internal report boundaries, the `212` shelfmarks cover `239` canonical 1860 *Physikatsbezirke*.

To read the entire surviving collection instead of cherry-picking a handful of printed excerpts, we ran `Kurrent Transcriber 1B` (release stack `re-v1`) across all `26,325` digitized pages (`10.23` million completion tokens, median `8.54` seconds per page, costing `32.60` Google Colab compute units). An automated pass flagged `498` double-exposed microfilm frames across seven volumes (`363` in Bissingen and `130` in Lauingen alone), leaving `25,827` unique pages. On a deterministic `30`-page stratified evaluation sample across `30` distinct volumes, the model reached `3.45%` median normalized character error rate (`2.99%` across the `25` running-prose sheets; details in the appendix). [A]

Machine transcription turned `212` unindexed manuscripts into a searchable map, not an unchecked source. For every one of the `239` canonical jurisdictions, we pulled the top candidate pages on infant feeding, gruel, pacifiers, sedatives, mortality, and goiter, downloaded the full-resolution archival images locally, and checked each entry directly against the handwriting. `226` reports had relevant archival pages checked word-for-word (`13` lacked an infant-care or mortality section in the digitized manuscript), yielding `191` documented infant-feeding accounts and `216` logged ink-level corrections to the machine text. [A]

## Two kingdoms of infancy

Mapped across all seven regions, the `191` documented infant-feeding reports split Bavaria along a stark geographic line. North of the Danube, breastfeeding was the norm. South of it, hand-feeding with *Mehlbrei* (thick flour-and-milk or flour-and-water gruel) took over. [A]

| Region (1860 *Regierungsbezirk*) | Canonical districts | Feeding documented | Predominantly breastfed | Mixed or short | Rarely or not breastfed | *Mehlbrei* predominant | Pacifier noted | Median 0-1 yr mortality (n) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Unterfranken und Aschaffenburg | 48 | 37 | 33 (89%) | 3 | 0 (0%) | 0 (0%) | 7 | 23.4% (6) |
| Pfalz (Palatinate) | 25 | 20 | 17 (85%) | 2 | 0 (0%) | 0 (0%) | 4 | 19.7% (5) |
| Oberfranken | 32 | 26 | 21 (81%) | 1 | 0 (0%) | 1 (4%) | 7 | 22.8% (4) |
| Mittelfranken | 32 | 29 | 18 (62%) | 8 | 2 (7%) | 4 (14%) | 4 | 30.2% (10) |
| Oberpfalz und Regensburg | 32 | 22 | 15 (68%) | 5 | 1 (5%) | 3 (14%) | 12 | 40.5% (4) |
| Niederbayern | 32 | 27 | 15 (56%) | 6 | 5 (19%) | 7 (26%) | 11 | 41.8% (2) |
| Schwaben und Neuburg | 38 | 30 | 3 (10%) | 11 | 15 (50%) | 22 (73%) | 16 | 38.3% (6) |
| **All seven regions** | **239** | **191** | **122 (64%)** | **36 (19%)** | **23 (12%)** | **37 (19%)** | **61** | **29.5% (37)** |

*Note: Mortality column includes only verified birth-cohort rates (deaths aged 0-1 per 100 live or total births). Full geocoded coordinates and quotes are in `map_bavaria_1860_infant_feeding.geojson`.*

Combine the three northern and western regions (Lower Franconia, Upper Franconia, and the Palatinate): out of `83` documented jurisdictions, `71` (`86%`) were predominantly breastfed, not a single one was classified as rarely or never breastfed (`0 / 83`), and only one (`Burgebrach`) relied on *Mehlbrei* as the predominant early diet. [A] Cross into Swabia (`30` documented jurisdictions) and the map flips upside down: only `3` (`10%`, including Alpine `Sonthofen`) were predominantly breastfed, `15` (`50%`) rarely or never breastfed, and `22` (`73%`) raised newborns primarily on *Mehlbrei*. [A]

Every single one of the `23` rarely-breastfed districts in the entire corpus sits either along or south of the Franconian-Danube border: `15` in Swabia, `5` in Lower Bavaria (`Abensberg`, `Landshut Stadt`, `Rottenburg`, `Straubing Land`, `Straubing Stadt`), `1` on the Danube edge of the Upper Palatinate (`Riedenburg`), and `2` in Middle Franconia (`Greding` on the southern border and industrial `Fürth`). [A]

The prose matches the statistics. In Augsburg, the district physician observed that infant food "is and has always been here flour gruel, whose toughness not infrequently rivals that of the mothers' prejudice against breastfeeding," washed down with rock-candy sugar water through a rag pacifier or sucking-pot. [A] In Ottobeuren, a numerical tally showed that barely one-third of mothers nursed, while `1,637` of `4,024` babies (`40.68%`) died in their first year. [A] In Riedenburg on the Altmühl, mothers often stopped nursing after six weeks and switched newborns to fresh water and *Muß*, watching healthy infants waste away from atrophy ("not exactly to the sorrow of the parents," the physician added bitterly); infants under one year accounted for `54.78%` of all deaths in the district. [A]

In Eggenfelden in Lower Bavaria, where the physician estimated that nearly half of all children died in year one, families cooked gruel in batches too large for a single meal and fed the leftovers a second and third time after sour fermentation, "as often as the child cries and as long as it keeps gulping it down." [A] In industrial Fürth, the one urban exception in northern Franconia, factory mothers skipped both nursing and rural gruel, feeding babies bread, rusk, and commercial chicory or beetroot "surrogate coffee" (*SurrogatCaffé*). [A]

## Seventeen percentage points

Nineteenth-century doctors reported infant mortality in two distinct ways: deaths under age one per `100` births, or deaths under age one as a share of all deaths in the parish. Pooling the two distorts the numbers, so we separated every verified percentage by its explicit denominator (`live_births`, `total_births_incl_stillborn`, or `all_deaths`).

Thirty-seven reports give a verifiable birth-cohort infant mortality rate (`29.5%` median overall, spanning `16.3%` in `Landstuhl` to `50.0%` in `Eggenfelden`). [A] Twenty-six of those thirty-seven also document local breastfeeding practice clearly enough to classify:

- **Predominantly breastfed (`n = 17`):** median first-year mortality **`23.0%`** (mean `24.5%`, range `16.3%` in `Landstuhl` to `33.7%` in `Bogen`). Not a single predominantly breastfed jurisdiction exceeded `34%`. [A]
- **Mixed, short, or rarely breastfed (`n = 9`):** median first-year mortality **`40.0%`** (mean `39.1%`, range `24.8%` in `Hof` to `50.0%` in `Eggenfelden`). [A]

That gap of `17.0` percentage points is not an artifact of distant provinces with different climates. Contemporary doctors saw the exact same cliff inside single border regions. In Scheinfeld, the physician cited medical statistician Carl Friedrich Majer's 1851-1856 figures for Middle Franconia alone: `34.70%` infant mortality in the province's Danube watershed versus `27.33%` in its Rhine-Main watershed. [A]

Two Middle Franconian reports captured natural experiments inside a single administrative jurisdiction. In `Roth`, the physician contrasted his two halves side by side: around Roth itself, mothers nursed for `18` to `20` months and first-year mortality ran `30%` to `36%`; around the neighboring enclave of Spalt, natural feeding belonged to "the rare exceptions," artificial hand-feeding was the rule, and `50%` of live-born infants died before age one. [A]

Farther south in `Greding`, on the cultural frontier between Franconia and Old Bavaria, the district physician split his own territory into two groups (`Gruppe Greding` and `Gruppe Stauf`) and pinpointed an unexpected mechanical cause.

## Stiff bodices, sour rags, and sedatives

In the Greding half of the district, women wore stiff traditional Bavarian *Mieder* bodices. Those garments, the physician wrote on manuscript page 129, did not merely constrict the ribcage: they pressed directly against the breasts and pushed the nipples so far inward that nursing became impossible or unbearably painful, forcing mothers to give up and rely on thick, half-cooked, lumpy *Mehlbrei*. In the Stauf half of the exact same district, women wore softer Franconian *Leibchen*, and "this defect disappears because of the shape of their bodices." [A]

*[Figure 2: `figures/fig_greding_mieder_natural_experiment.jpg` - Greding (`BSB Cgm 6874(57,1)`, `bsb00141175`, page 131). Crop above verified reading: "In der Gruppe Greding kommt dazu noch eine sehr beachtenswerthe Schädlichkeit durch die Mieder. Diese schnüren nicht blos den Brustkasten zusammen u hemmen die ganze Ausbildung desselben, sie drücken auch noch speciell die Brüste, hindern deren Entwicklung u pressen die Warzen so hinein, daß sie zum Säugen untauglich werden oder das Säugen für die Mutter so schmerzhaft machen, daß sie es unterlassen muß. In der Gruppe Stauf fällt dieser Mißstand durch die Form der Leibchen weg."]*

He was not alone. Across in Lower Bavaria, the physician for `Landshut (Land)` independently blamed stiff *Mieder* for flattening mothers' nipples until they were "no longer suitable for nursing," adding that fewer than half of mothers in his district breastfed. [A]

*[Figure 3: `figures/fig_landshut_mieder_nipples.jpg` - Landshut Land (`BSB Cgm 6874(97)`, `bsb00111891`, page 33). Crop above verified reading: "Die steifen Mieder üben übrigens auf die Brust eine sehr nachtheilige Wirkung, die Warze wird eingedrückt und zum Stillen nicht mehr geeignet; während in späteren Jahren die heruntergedrängte weibliche Brust häßlich hängt."]*

Where breast milk retreated, the cloth pacifier stepped in. Sixty-one verified reports describe the *Schnuller*, *Zulp*, *Zulze*, *Sauglappen*, or *Saugschlozer*: a linen scrap stuffed with chewed bread, sugar, flour gruel, or in Alpine `Sonthofen` the burnt crust scraped from the sides and bottom of the gruel pot. [A] In `Abensberg`, the physician found these rags "in sour, almost putrid fermentation in the infants' mouths right after birth." [A] In `Burgau` (where `44.55%` of newborns died in year one), pacifiers dropped in the dirt went straight back into babies' mouths. [A]

A margin footnote in Roggenburg records the worst consequence of adults pre-moistening a pacifier. Some years earlier, a housemaid with syphilitic throat chancres moistened (*annezte*) her employers' newborn's pacifier in her own mouth. The baby developed chancres at both corners of the mouth and on the tip of the tongue, and while nursing infected its mother's nipples with deep-eating chancres. [A]

*[Figure 4: `figures/fig_roggenburg_syphilis_pacifier.jpg` - Roggenburg (`BSB Cgm 6874(153)`, `bsb00007355`, page 27, margin note `*2`). Crop above verified reading: "Vor einigen Jahren steckte eine solche Magd mit Chancres im Halse, die dem neugeborenen Kinde ihrer Dienstherrschaft den Schnuller annezte, dieses an, indem es Chancres in beiden Mundwinkeln u an der Zungenspitze bekam, u das Kind, welches an der Mutter trank, inficirte die mütterlichen Brustwarzen, die mit tief fressenden Chancres bedeckt wurden."]*

When babies still cried, some households reached for stronger quieters. Fifteen verified infant-feeding reports across Bavaria document alcohol given directly to infants or toddlers: schnapps-dipped pacifiers or bread crusts in `Roggenburg`, `Bischofsheim (Rhön)`, `Münchberg`, `Ludwigsstadt`, `Otterberg`, and `Markt Erlbach`, and beer given from the mother's mug or after weaning in `Bayreuth (Land)` ("six-month-old children drinking alternately from the breast and from the mother's beer glass" at public vaccinations), `Amberg (Land)` ("small children seen completely intoxicated before noon"), `Haßfurt`, and `Burgau`. [A]

In `Bischofsheim` in the Rhön mountains, the physician drew a direct parallel to urban wet-nurses: "just as in big cities many reckless wet-nurses mix opium into the milk to calm the infants in their care, mothers here put schnapps under the pacifier, which produces the same effect." [A]

*[Figure 5: `figures/fig_bischofsheim_schnaps_opium.jpg` - Bischofsheim v. d. Rhön (`BSB Cgm 6874(14)`, `bsb00140582`, page 146). Crop above verified reading: "Leider bekommen auch schon ganz kleine Kinder von dem gebrannten Wasser zu trinken. Und sowie in großen Städten manche leichtsinnige Ammen ihren Pflegbefohlenen zur Beruhigung Opium unter die Milch mischen, so geben die hiesigen Mütter Schnaps unter den Schnuller, welcher auch diese Wirkung hervorbringt."]*

Two reports caught direct opiate use in rural households. In `Markt Erlbach` in Middle Franconia, peasant women fed infants seeds of *Papaver somniferum* (opium poppy) on bread or boiled to induce sleep. [A] In `Landstuhl` in the Palatinate, despite high breastfeeding rates and low overall infant mortality, the physician warned that some mothers gave infants a decoction of poppy heads (*Abkochung von Mohnköpfen*) to quiet them, "through which cases of severe intoxication have already come before me." [A]

*[Figure 6: `figures/fig_landstuhl_poppy_decoction.jpg` - Landstuhl (`BSB Cgm 6874(98)`, `bsb00145118`, page 58). Crop above verified reading: "manche Mütter, ihren Kindern zur Beruhigung eine Abkochung von Mohnköpfen zu verabreichen, wodurch mir schon Fälle hochgradiger Intoxication vorgekommen sind."]*

## Thirty years of warnings

In the Danube-adjacent districts with the highest mortality (`Göggingen` `47.2%` of live births, `Wörth an der Donau` `47.4%`, `Regensburg Land` `46.06%` of total births, `Burgau` `44.55%`), district doctors were neither ignorant of the pattern nor silent about it. [A] They argued with families during home visits, lectured mothers at compulsory smallpox vaccinations, and enlisted parish priests and midwives.

In `Öttingen` in northern Swabia, where thirty years of parish figures (`1830-1860`) put first-year mortality at `35.92%` of live births (`359.23` deaths per `1,000`), the aging district physician summed up three decades of campaigning against thick flour gruel and the rag pacifier in a single sentence: "All efforts made for 30 years by the undersigned against this pernicious habit through instruction and admonitions in private and at public vaccination, as well as through the influence of pastors and midwives, have hitherto remained fruitless." [A]

---

## Appendix

### How we read 26,325 pages

Every page image in `BSB Cgm 6874` (`212` volumes, `26,325` archival canvases, `Public Domain Mark 1.0`) was fetched via the Munich Digitization Center IIIF API and transcribed using `Kurrent Transcriber 1B` (`13fragments`, `CC BY-SA 4.0`, DOI `10.5281/zenodo.24342061`) running the pinned `re-v1` release stack (`vllm==0.23.0`, `transformers==5.13.0`, `pillow==12.3.0`, `numpy==2.4.6`) with `fp-v16` margin-surround masking.

The entire corpus took `32.60` Google Colab compute units (`8.54` seconds median per page; `10,231,643` completion tokens). Repetition guards cut `176` pages (`0.67%`; `99.33%` clean completions), `143` pages (`0.54%`) had run artifacts stripped, and `264` (`1.00%`) were blank covers or endpapers. Consecutive-frame text comparison flagged `498` double-exposed microfilm frames across seven volumes (`363` in Bissingen and `130` in Lauingen).

To measure in-corpus accuracy directly, we drew `30` pages across `30` distinct volumes (`seed=18580421`), keyed them blind from the images, adjudicated every word against the ink (`28,929` reference characters, `4,129` reference words), and scored them under the exact `Kurrent Pages Benchmark` protocol. Median normalized character error rate (`cer_norm`) was `3.45%` (95% bootstrap CI `[2.54%, 5.98%]`; median `cer_dipl` `3.88%`; median `wer_norm` `15.73%`, 95% CI `[10.87%, 19.86%]`). On the `25` running-prose pages, median `cer_norm` was `2.99%` (mean `4.41%`, range `0.37%` in Neumarkt to `18.46%` in Lauf). Five non-prose pages pulled the overall mean `cer_norm` up to `18.27%`: one hand-drawn district map (`Wertingen`, `68.66%`), one ruled two-column trade table where the model emitted raw HTML `<table>` tags (`Fürth`, `217.95%`), and three dense multi-column tables (`Kastl Lit. B`, `Herzogenaurach`, `Ludwigshafen`, `44.17%` to `53.85%`). [A]

### What the model got wrong

Machine transcription was reliable enough to find every passage across `26,325` pages, but checking the ink caught real errors in almost every hard hand (`216` of `239` entries carry explicit correction notes). Examples from the quotations in this article:

- **Roggenburg (page 15):** the model read `Empörendste` as `Emperor este`, `versoffenen` as `vorhöffenen`, `Schnaps` as `Schmack`, `Kauen` (chewing) as `Rauen`, and `Schnullerbrod` as `Schnullerbeer`.
- **Roggenburg (page 27):** it read `annezte` (moistened) as `anmugte` and `beiden` as `leuen`.
- **Landstuhl (page 58):** it read `Mohnköpfen` (poppy heads) as `Mohntöpfen`, `Beruhigung` (calming) as `Berührung` (touching), and `Mißbrauch` as `Maßbrauch`.
- **Markt Erlbach (page 124):** it read `Branntwein` as `Beamtwein`, `Bauersweiber` as `Bauersväter`, `Brod` as `baxd`, and `gekocht` as `gekraft`.
- **Dense pages and tables:** on several tightly written sheets (`Bayreuth Land` page 42, `Otterberg` page 33), the model stopped short of the bottom four or five lines; on ruled tables (`Fürth` page 43), it switched into HTML markup.

Those errors are why every quotation, count, and mortality figure in this article and its companion CSV tables was checked directly against the BSB page images.

### What we have not confirmed yet

- **Independent professional review is open.** Every `[A]` passage and the `30`-page evaluation references were checked by an agent against the archival images, not yet by a human historical paleographer. Any changes found during professional review will be published in the dataset changelog.
- **Upper Bavaria (*Oberbayern*) is absent.** Because `BSB Cgm 6874` holds only the seven other *Regierungsbezirke*, Upper Bavaria's reports (held at Staatsarchiv München) are not included in these counts.
- **Correlation is not a single-cause proof.** The `17.0` percentage-point gap in median first-year mortality between predominantly breastfed (`23.0%`) and non-predominantly breastfed (`40.0%`) districts matches what contemporary Bavarian physicians observed. Other regional variables noted in the reports also varied across Bavaria, including illegitimate birth shares, maternal field work, winter altitude, water supply, and sanitation.

### Links and open dataset

- **Original manuscripts:** Bayerische Staatsbibliothek, `BSB Cgm 6874(1)`-`Cgm 6874(207)`, Munich Digitization Center (`Public Domain Mark 1.0`).
- **Model:** `Kurrent Transcriber 1B`, `https://huggingface.co/13fragments/kurrent-transcriber-1b` (`CC BY-SA 4.0`, Zenodo DOI `10.5281/zenodo.24342061`).
- **Companion dataset (staged locally in `dist/zenodo_package/`):** `cgm6874_pages.jsonl.gz` (all `26,325` pages with `duplicate_of_canvas` flag), `cgm6874_volumes.csv`, `districts_index.csv`, `verified_bavaria_1860_infant_feeding.csv`, `map_bavaria_1860_infant_feeding.geojson`, `verified_bavaria_1860_folk_medicine.csv`, `in_corpus_accuracy_eval.csv`, `DATACARD.md`, and `SHA256SUMS`.
- **Follow-up piece:** `publication/article_2_folk_medicine_outline_and_quotes.md` (chair legs, childbed sabres, boiled dog meat, and `25` verified folk-medicine quotations from the same `26,325`-page run).
