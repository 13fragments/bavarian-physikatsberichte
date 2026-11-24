# Feeding and survival in 1860 Bavaria: mapping 239 districts across 212 handwritten medical volumes

- **Target:** `13fragments` blog (flagship research report from the complete `BSB Cgm 6874` transcription run).
- **Status:** Second draft after dual-CLI audit (`2026-11-24`). Every `[A]` fact, count, and German quotation comes from `publication/FACTS.md` and `data/dataset/verified_passages.csv` and was checked by an LLM agent against Bayerische Staatsbibliothek archival page images. Independent review by a professional historical paleographer is open before public release; remove `[A]` tags once that review passes.
- **Repository and staged companion dataset:** `https://github.com/13fragments/bavarian-physikatsberichte` (`dist/zenodo_package/` staged locally for Zenodo/Hugging Face release).
- **Figures:** `figures/fig_bavaria_1860_feeding_map.png`, `fig_roggenburg_schnaps_pacifier.jpg`, `fig_greding_mieder_natural_experiment.jpg`, `fig_landshut_mieder_nipples.jpg`, `fig_roggenburg_syphilis_pacifier.jpg`, `fig_bischofsheim_schnaps_opium.jpg`, `fig_landstuhl_poppy_decoction.jpg`.

---

**Subtitle:** In 1858, Bavaria ordered royal district physicians to record how families fed newborns. Reading all 26,325 surviving manuscript pages maps a sharp cultural boundary between Franconia and Swabia where first-year infant mortality jumped by roughly 16 percentage points.

In 1860, the royal district physician in Roggenburg, a rural Swabian jurisdiction south of the Danube, finished a passage on infant care with three exclamation marks. First-year infants in his district, he wrote, rarely received breast milk. Families fed newborns coarse, paste-like flour gruel (*Mehlbrei*) and bread softened in water or pre-chewed and tied into a cloth rag (*Schnullerbrod*). In heavy-drinking households, parents dipped that pacifier straight into schnapps "so that they should sleep faster and longer!" (the ink ends with three exclamation marks). [A]

Farther north and west inside the very same kingdom, the pattern flipped. In Uffenheim in Middle Franconia (roughly 140 km north of Roggenburg), the physician reported that nearly every mother nursed her child through the first year and often well into the second; `17.6%` of born children died in their first year. [A] In Landstuhl in the Bavarian Palatinate (roughly 230 km to the northwest), where breastfeeding also predominated, `14.4%` of live-born infants died before age one (`16.3%` when stillbirths are added to both deaths and births). [A] Across four birth-cohort records in Swabia and Lower Bavaria (`Burgau`, `Göggingen`, `Ottobeuren`, and a verbal estimate for `Eggenfelden`), between `40%` and `50%` of newborns died inside twelve months. [A]

*[Figure 1: `figures/fig_roggenburg_schnaps_pacifier.jpg` - Roggenburg (`BSB Cgm 6874(153)`, `bsb00007355`, page 15; `roggenburg_p15_schnaps` and `inf_roggenburg_p15`). Credit: Bayerische Staatsbibliothek, PDM 1.0. Reading: "Allein das Aller Empörendste ist, daß in solchen versoffenen Familien schon die Säuglinge an dieses gefährliche Getränk gewöhnt, u ihre Schnuller in Schnaps eingetaucht werden, damit sie schneller u länger schlafen sollen! [triple exclamation mark in ink] ... Die erste Ernährung der Kinder im 1ten Lebensjahre geschieht in der Regel durch grobe u kleisterartige Mehlbreie, durch in Wasser aufgeweichtes oder durch Kauen verkleinertes u in einen Fleck gebundenes Schnullerbrod u nur in den seltensten Fällen durch Muttermilch."]*

Historical demographers have mapped southern Germany's non-breastfeeding infant-mortality belt since John Knodel and Etienne van de Walle's 1967 *Population Studies* analysis and Hallie Kintner's 1985 regional series. Between 1858 and 1861, Bavarian district physicians recorded the ground-level testimony across hundreds of individual jurisdictions, yet most of those handwritten reports were never published or indexed in full. Almost every page is written in *Kurrent*, the nineteenth-century German cursive that few modern readers can decipher without specialist training.

## One royal rescript, 26,325 pages

On 21 April 1858, King Maximilian II's interior ministry issued a royal rescript instructing every district physician (*Gerichtsarzt*) in Bavaria to compile a standardized medical, topographic, and ethnographic description (*Physikatsbericht*) of his jurisdiction: soil, climate, housing, clothing, diet, infant care, endemic illness, mortality tables, and popular superstition.

For seven of Bavaria's eight historical administrative regions (*Regierungsbezirke*), `212` bound manuscript volumes survive at the Bayerische Staatsbibliothek in Munich under call number `BSB Cgm 6874` (`Public Domain Mark 1.0`). Upper Bavaria (*Oberbayern*) is absent from this collection because its reports passed to the *Historischer Verein von Oberbayern* and are preserved as a deposit in the Stadtarchiv München (Munich Municipal Archive). Splitting eleven collective volumes from Lower Franconia and the Palatinate along their internal report boundaries yields `239` canonical 1860 *Physikatsbezirke*.

To index the entire surviving collection rather than rely on a few printed excerpts, we ran `Kurrent Transcriber 1B` (release stack `re-v1`) across all `26,325` digitized pages (`10.23` million completion tokens; `8.54` seconds median per-page latency under batch concurrency). Consecutive-frame auditing flagged `498` duplicate or re-shot frames across seven volumes (`363` in Bissingen and `130` in Lauingen; `493` share identical processed-image hashes), leaving `25,827` unique pages. On a deterministic volume-clustered sample of `30` text-bearing interior pages across `30` distinct volumes, an LLM agent keyed every image blind (`4.33%` median normalized character error rate) and then adjudicated differences against the ink (`3.45%` median; `2.99%` across `25` running-prose sheets; full design and limitations in the appendix). [A]

Machine transcription served for corpus-wide candidate discovery, never as unchecked evidence. For each of the `239` canonical jurisdictions, we pulled top candidate pages on infant feeding, gruel, pacifiers, sedatives, mortality, and goiter, downloaded the archival images locally, and had an LLM agent check every coded field and quotation directly against the ink. `226` reports had relevant archival pages checked (`13` had no infant-feeding or mortality section retrieved in the initial candidate pass), yielding `191` documented infant-feeding accounts and `217` `Agent-checked` rows with logged ink corrections to the machine text. [A]

## Two kingdoms of infancy

Mapped across all seven regions, the `191` documented infant-feeding reports divide Bavaria along a sharp cultural boundary separating Franconia and the Palatinate from Swabia and Old Bavaria. It is not a simple river line: four Swabian Ries jurisdictions (`Nördlingen`, `Wemding`, `Öttingen`, and `Wallerstein`) lie north of the Danube yet follow the Swabian non-breastfeeding regime, while `Bissingen` and `Donauwörth (Land)` on the river breastfed. [A]

*[Figure 2: `figures/fig_bavaria_1860_feeding_map.png` - Archival map of breastfeeding regimes and birth-cohort infant mortality across all 239 canonical districts in `BSB Cgm 6874` (with Palatinate inset and shaded Stadtarchiv München gap for Upper Bavaria). Source data: `map_bavaria_1860_infant_feeding.geojson`.]*

| Region (1860 *Regierungsbezirk*) | Canonical districts | Feeding documented | Predominantly breastfed | Mixed or short | Rarely or not breastfed | *Mehlbrei* predominant | Pacifier noted | Birth-cohort IMR median (n) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Unterfranken und Aschaffenburg | 48 | 37 | 33 (89%) | 3 | 0 (0%) | 0 (0%) | 7 | 23.4% (6) |
| Pfalz (Palatinate) | 25 | 20 | 17 (85%) | 2 | 0 (0%) | 0 (0%) | 4 | 19.7% (5) |
| Oberfranken | 32 | 26 | 21 (81%) | 1 | 0 (0%) | 1 (4%) | 7 | 22.8% (4*) |
| Mittelfranken | 32 | 29 | 18 (62%) | 8 | 2 (7%) | 4 (14%) | 4 | 30.2% (10) |
| Oberpfalz und Regensburg | 32 | 22 | 15 (68%) | 5 | 1 (5%) | 3 (14%) | 12 | 40.5% (4*) |
| Niederbayern | 32 | 27 | 15 (56%) | 6 | 5 (19%) | 7 (26%) | 11 | 41.8% (2*) |
| Schwaben und Neuburg | 38 | 30 | 3 (10%) | 11 | 15 (50%) | 22 (73%) | 16 | 38.3% (6) |
| **All seven regions** | **239** | **191** | **122 (64%)** | **36 (19%)** | **23 (12%)** | **37 (19%)** | **61** | **29.5% (37)** |

*Table note: `*` marks small regional mortality samples (`n < 5`). Birth-cohort mortality covers only the `37` reports providing birth denominators across observation periods ranging from 1 to nearly 50 years (excluding `18` reports that give only infant share of all deaths). Oberpfalz's `40.5%` median rests on `n = 4`, pulled up by two unclassified Regensburg rows (`Regensburg Land` `46.06%` includes stillbirths in the numerator) and `Wörth a.d. Donau` (`47.4%`, declining breastfeeding). Niederbayern's `41.8%` rests on `n = 2` (`Bogen` `33.69%` and approximate `Eggenfelden` `~50%`). Pacifier counts depend partly on regional dialect vocabulary in candidate retrieval.*

Combine the three northern and western regions (Lower Franconia, Upper Franconia, and the Palatinate): out of `83` documented jurisdictions, `71` (`86%`) were predominantly breastfed, none were rarely or never breastfed (`0 / 83`), and only one (`Burgebrach`) relied on *Mehlbrei* as the predominant early diet. [A] Cross into Swabia (`30` documented jurisdictions) and the distribution inverts: only `3` (`10%`, including Alpine `Sonthofen`) were predominantly breastfed, `15` (`50%`) rarely or never breastfed, and `22` (`73%`) raised newborns primarily on *Mehlbrei*. [A]

Twenty-two of the `23` rarely-breastfed districts sit in Swabia (`15`), Lower Bavaria (`5`: `Abensberg`, `Landshut Stadt`, `Rottenburg`, `Straubing Land`, `Straubing Stadt`), southern Upper Palatinate (`Riedenburg`), and southern Middle Franconia (`Greding`). The lone northern outlier is industrial `Fürth` in Middle Franconia, where mothers skipped both nursing and rural flour gruel in favor of bread, rusk, biscuit in milk, and commercial chicory or beetroot "surrogate coffee" (*SurrogatCaffé*). [A]

The doctors' prose puts texture behind those counts. In Augsburg, the district physician wrote that infant food "is and has always been here flour gruel, whose toughness not infrequently rivals that of the mothers' prejudice against breastfeeding," washed down with rock-candy sugar water through a rag pacifier or sucking-pot. [A] In Ottobeuren, a numerical tally found that barely one-third of mothers nursed while `1,637` of `4,024` babies (`40.68%`) died in year one. [A] In Riedenburg on the Altmühl, mothers often weaned after six weeks onto fresh water and *Muß*, watching healthy infants waste away from atrophy ("not exactly to the sorrow of the parents," the doctor remarked); infants under age one accounted for `54.78%` of all deaths in the district. [A] In Eggenfelden in Lower Bavaria, where the physician estimated that nearly half of children died in year one, households cooked oversized pots of gruel and re-fed the leftovers a second and third time after sour fermentation, "as often as the child cries and as long as it keeps gulping it down." [A]

## Sixteen to seventeen percentage points

Nineteenth-century physicians reported infant mortality under several non-equivalent definitions: postnatal deaths under age one per `100` live births (`n = 29`, including `Eggenfelden`'s verbal `"fast die Hälfte"` estimate), composite ratios per `100` total births (`n = 8`, two of which include stillbirths in the numerator, `Landstuhl` `16.3%` and `Regensburg Land` `46.06%`, and one of which, `Ebermannstadt` `20.78%`, counts deaths before compulsory smallpox vaccination), or infant deaths as a share of all deaths (`n = 18`). Pooling death shares with birth-cohort rates distorts comparisons, so the dataset separates them into distinct columns (`imr_pct_of_births` and `infant_share_of_all_deaths_pct`) with explicit stillbirth, approximate, and age-window flags.

Across the `26` districts reporting both breastfeeding practice and a birth-cohort mortality rate (a nonrandom subset of the `239` jurisdictions), the feeding-survival gap holds across every stricter sensitivity cut:

| Mortality slice | Predominantly breastfed | Mixed, short, or rare | Median gap |
| --- | --- | --- | ---: |
| All birth-cohort rates (`n = 26`, Mann-Whitney `AUC = 0.922`) | `23.03%` (`n = 17`, range `16.3%-33.7%`) | `40.00%` (`n = 9`, range `24.8%-50.0%`) | `+16.97 pp` |
| Strict `live_births` rows only (`n = 22`) | `24.05%` (`n = 15`, range `17.6%-33.7%`) | `40.00%` (`n = 7`, range `24.8%-50.0%`) | `+15.95 pp` |
| Strict `live_births` excl. approximate `Eggenfelden` (`n = 21`) | `24.05%` (`n = 15`, range `17.6%-33.7%`) | `39.45%` (`n = 6`, range `24.8%-47.4%`) | `+15.40 pp` |
| Within `Mittelfranken` alone (`live_births`, `n = 8`) | `24.93%` (`n = 6`, range `17.6%-30.3%`) | `39.45%` (`Roth 40.0%`, `Weißenburg 38.9%`) | `+14.53 pp` |

Even on the strictest `live_births` subset excluding `Eggenfelden`, infant mortality rose by roughly two-thirds where breastfeeding weakened (`24.05%` to `39.45%`), and no predominantly breastfed district in the corpus exceeded `33.7%`. [A] Because the breastfed sample clusters heavily in Franconia and the Palatinate, regional factors such as illegitimacy rates, maternal agricultural labor, climate, housing density, water supply, and sanitation also vary across the map. That makes the within-province and within-district contrasts especially revealing.

Inside Middle Franconia alone, the six predominantly breastfed districts with live-birth rates cluster between `17.6%` (`Uffenheim`) and `30.3%` (`Altdorf`, median `24.9%`), whereas southern border districts with mixed feeding jump to `38.9%` (`Weißenburg i. B.`) and `40.0%` (`Roth`). [A] Within `Roth` itself, the physician contrasted his two halves side by side: around Roth, mothers nursed for `18` to `20` months and first-year mortality ran `30%` to `36%`; around the neighboring parish of Spalt, natural feeding belonged to "the rare exceptions," artificial hand-feeding was the rule, and `50%` of live-born infants died before age one. [A] Farther south in `Greding`, the district physician documented a second within-district contrast between `Gruppe Greding` and `Gruppe Stauf` and proposed a surprising mechanical explanation.

These reports must also be read with source criticism. Royal district physicians were state-appointed, university-trained men answering a mandatory ministerial rubric. They frequently wrote with exasperation or disdain toward rural mothers, midwives, and poorer households, and observational contrasts like `Roth`/`Spalt` or `Greding`/`Stauf` cannot isolate feeding from confession, settlement structure, wealth, or sanitation. Their manuscripts are rich nineteenth-century clinical witnesses, not controlled trials.

## Stiff bodices, sour rags, and sedatives

In the Greding half of his district, the physician blamed traditional stiff *Mieder* bodices (manuscript page 129, archival canvas 131). Those garments, he argued, did not merely constrict the ribcage: they pressed against the breasts and pushed the nipples so far inward that nursing became impossible or unbearably painful, driving mothers toward thick, half-cooked, lumpy *Mehlbrei*. In the Stauf half of the exact same district, women wore *Leibchen* of a different shape, and "this defect disappears because of the shape of the *Leibchen*." [A]

*[Figure 3: `figures/fig_greding_mieder_natural_experiment.jpg` - Greding (`BSB Cgm 6874(57,1)`, `bsb00141175`, canvas 131 / ms p. 129; `greding_p131_mieder`). Credit: Bayerische Staatsbibliothek, PDM 1.0. Reading: "In der Gruppe Greding kommt dazu noch eine sehr beachtenswerthe Schädlichkeit durch die Mieder. Diese schnüren nicht blos den Brustkasten zusammen u hemmen die ganze Ausbildung desselben, sie drücken auch noch speciell die Brüste, hindern deren Entwicklung u pressen die Warzen so hinein, daß sie zum Säugen untauglich werden oder das Säugen für die Mutter so schmerzhaft machen, daß sie es unterlassen muß. In der Gruppe Stauf fällt dieser Mißstand durch die Form der Leibchen weg."]*

Across in Lower Bavaria, the physician for `Landshut (Land)` offered the same anatomical hypothesis independently, blaming stiff *Mieder* for flattening mothers' nipples until they were "no longer suitable for nursing," while noting that fewer than half of mothers in his district breastfed. [A]

*[Figure 4: `figures/fig_landshut_mieder_nipples.jpg` - Landshut Land (`BSB Cgm 6874(97)`, `bsb00111891`, canvas 33; `landshut_land_p33_mieder`). Credit: Bayerische Staatsbibliothek, PDM 1.0. Reading: "Die steifen Mieder üben übrigens auf die Brust eine sehr nachtheilige Wirkung, die Warze wird eingedrückt und zum Stillen nicht mehr geeignet; während in späteren Jahren die heruntergedrängte weibliche Brust häßlich hängt."]*

Where breast milk retreated, the cloth pacifier stepped in. Sixty-one verified reports note the *Schnuller*, *Zulp*, *Zulze*, *Sauglappen*, or *Saugschlozer*: a linen scrap stuffed with chewed bread, sugar, flour gruel, or in Alpine `Sonthofen` the crust scraped from the sides and bottom of the gruel pot. [A] In `Abensberg`, the physician found these rags "in sour, almost putrid fermentation in the infants' mouths right after birth." [A] In `Burgau` (`44.55%` first-year mortality), pacifiers dropped in the dirt went straight back into babies' mouths. [A]

A margin footnote in Roggenburg records the worst consequence of adults pre-moistening a pacifier. Some years earlier, a housemaid with syphilitic throat chancres moistened (*annezte*) her employers' newborn's pacifier in her own mouth. The baby developed chancres at both corners of the mouth and on the tip of the tongue, and while nursing infected its mother's nipples with deep-eating chancres. [A]

*[Figure 5: `figures/fig_roggenburg_syphilis_pacifier.jpg` - Roggenburg (`BSB Cgm 6874(153)`, `bsb00007355`, canvas 27, margin note `*2`; `roggenburg_p27_syphilis`). Credit: Bayerische Staatsbibliothek, PDM 1.0. Reading: "Vor einigen Jahren steckte eine solche Magd mit Chancres im Halse, die dem neugeborenen Kinde ihrer Dienstherrschaft den Schnuller annezte, dieses an, indem es Chancres in beiden Mundwinkeln u an der Zungenspitze bekam, u das Kind, welches an der Mutter trank, inficirte die mütterlichen Brustwarzen, die mit tief fressenden Chancres bedeckt wurden."]*

When babies still cried, some households reached for stronger quieters. Fifteen verified infant-feeding reports across Bavaria document alcohol given directly to infants or toddlers: schnapps-dipped pacifiers or bread crusts in `Roggenburg`, `Bischofsheim (Rhön)`, `Münchberg`, `Ludwigsstadt`, `Otterberg`, and `Markt Erlbach`, and beer given from the mother's mug or after weaning in `Bayreuth (Land)` ("six-month-old children drinking alternately from the breast and from the mother's beer glass" at public vaccinations), `Amberg (Land)` ("small children seen completely intoxicated already in the forenoon"), `Haßfurt`, and `Burgau`. [A]

In `Bischofsheim` in the Rhön mountains, the physician drew a direct parallel to urban wet-nurses: "just as in big cities many reckless wet-nurses mix opium into the milk to calm the infants in their care, mothers here put schnapps under the pacifier, which produces the same effect." [A]

*[Figure 6: `figures/fig_bischofsheim_schnaps_opium.jpg` - Bischofsheim v. d. Rhön (`BSB Cgm 6874(14)`, `bsb00140582`, canvas 146; `inf_bischofsheim_rhoen_p146`). Credit: Bayerische Staatsbibliothek, PDM 1.0. Reading: "Leider bekommen auch schon ganz kleine Kinder von dem gebrannten Wasser zu trinken. Und sowie in großen Städten manche leichtsinnige Ammen ihren Pflegbefohlenen zur Beruhigung Opium unter die Milch mischen, so geben die hiesigen Mütter Schnaps unter den Schnuller, welcher auch diese Wirkung hervorbringt."]*

Two reports recorded poppy seeds or poppy-head decoctions given to infants for sleep. In `Markt Erlbach` in Middle Franconia, peasant women gave infants seeds of *Papaver somniferum* on bread or boiled to induce sleep. [A] In `Landstuhl` in the Palatinate, despite high breastfeeding rates and low overall infant mortality, the physician warned that some mothers gave infants a decoction of poppy heads (*Abkochung von Mohnköpfen*) to quiet them, "through which cases of severe intoxication have already come before me." [A]

*[Figure 7: `figures/fig_landstuhl_poppy_decoction.jpg` - Landstuhl (`BSB Cgm 6874(98)`, `bsb00145118`, canvas 58; `inf_landstuhl_p58`). Credit: Bayerische Staatsbibliothek, PDM 1.0. Reading: "mancher Mütter, ihren Kindern zur Beruhigung eine Abkochung von Mohnköpfen zu verabreichen, wodurch mir schon Fälle hochgradiger Intoxication vorgekommen sind."]*

## Thirty years of warnings

In the high-mortality districts of Swabia and southern Upper Palatinate (`Göggingen` `47.2%` of live births, `Wörth an der Donau` `47.4%`, `Regensburg Land` `46.06%` including stillbirths, `Burgau` `44.55%`), district physicians were neither ignorant of the toll nor silent about it. [A] In `Öttingen` in northern Swabia, where thirty years of parish figures (`1830-1860`) put first-year mortality at `35.92%` of live births (`359.23` deaths per `1,000`), the aging physician summed up three decades of campaigning against thick flour gruel and the rag pacifier in a single sentence: "All efforts made for 30 years by the undersigned against this pernicious habit through instruction and admonitions in private and at public vaccination, as well as through the influence of pastors and midwives, have hitherto remained fruitless." [A]

---

## Appendix

### How we read 26,325 pages

Every page image in `BSB Cgm 6874` (`212` volumes, `26,325` archival canvases, `Public Domain Mark 1.0`) was fetched via the Munich Digitization Center IIIF API and transcribed using `Kurrent Transcriber 1B` (`13fragments`, `CC BY-SA 4.0`, DOI `10.5281/zenodo.24342061`) running the `re-v1` release stack (`vllm==0.23.0`, `transformers==5.13.0`, `pillow==12.3.0`, `numpy==2.4.6`) with `fp-v16` margin-surround masking.

The run produced `10,231,643` completion tokens at `8.54` seconds median per-page latency under batch concurrency (Google Colab account balance decreased by `32.60` compute units across the run). Repetition guards cut `176` pages (`0.67%`), `143` pages (`0.54%`) had run artifacts stripped, and `264` (`1.00%`) returned empty outputs. Consecutive-frame auditing flagged `498` duplicate or re-shot frames across seven volumes (`363` in Bissingen and `130` in Lauingen; `493` share identical processed-image hashes).

To measure in-corpus accuracy, we drew a volume-clustered random sample of `30` text-bearing interior pages (`canvas > 2`, `80-450` model words, digit share `< 0.12`, non-duplicate) across `30` distinct volumes (`seed=18580421`). Because eligibility filters on model output, blank sheets and catastrophic short/long failures are excluded from this slice. An LLM agent keyed all `30` pages blind from the images (`4.33%` median `cer_norm`, 95% CI `[2.96%, 7.14%]`, `19.02%` mean) and then adjudicated differences against the ink (`28,929` reference characters, `4,129` words), scored under the exact `Kurrent Pages Benchmark` protocol: median adjudicated `cer_norm` was `3.45%` (95% bootstrap CI `[2.54%, 5.98%]`; median `cer_dipl` `3.88%`; median `wer_norm` `15.73%`, 95% CI `[10.87%, 19.86%]`). Across the `25` running-prose sheets, adjudicated median `cer_norm` was `2.99%` (`3.19%` blind; mean `4.41%`, range `0.37%` in Neumarkt to `18.46%` in Lauf). Five non-prose sheets pulled the overall mean up to `18.27%`: one hand-drawn district map (`Wertingen`, `68.66%`), one ruled two-column trade table where the model emitted HTML `<table>` tags (`Fürth`, `217.95%`), and three dense tabular spreads (`Kastl Lit. B`, `Herzogenaurach`, `Ludwigshafen`, `44.17%` to `53.85%`). [A]

### What the model got wrong

Machine transcription enabled corpus-wide candidate discovery across `26,325` pages, but checking the ink caught real errors in nearly every hard hand (`217` of `226` `Agent-checked` district entries log explicit ink corrections). Examples from the quotations in this article:

- **Roggenburg (page 15):** the model read `Empörendste` as `Emperor este`, `versoffenen` as `vorhöffenen`, `Schnaps` as `Schmack`, `Kauen` (chewing) as `Rauen`, and `Schnullerbrod` as `Schnullerbeer`.
- **Roggenburg (page 27):** it read `annezte` (moistened) as `anmugte` and `beiden` as `leuen`.
- **Landstuhl (page 58):** it read `Mohnköpfen` (poppy heads) as `Mohntöpfen`, `Beruhigung` (calming) as `Berührung` (touching), and `Mißbrauch` as `Maßbrauch`.
- **Markt Erlbach (page 124):** it read `Branntwein` as `Beamtwein`, `Bauersweiber` as `Bauersväter`, `Brod` as `baxd`, and `gekocht` as `gekraft`.
- **Dense pages and tables:** on several tightly written sheets (`Bayreuth Land` page 42, `Otterberg` page 33), the model stopped short of the bottom four or five lines; on ruled tables (`Fürth` page 43), it emitted HTML markup.

Those errors are why every quotation, count, and mortality rate in this article and its companion tables was checked directly against the BSB archival images.

### What we have not confirmed yet

- **Independent professional paleographer review is open.** Every `[A]` quotation, mortality row, and `30`-page evaluation reference was checked by an LLM agent against the archival images, not yet by a human paleographer. Any changes found during professional review will be logged in the dataset changelog.
- **Upper Bavaria (*Oberbayern*) is absent.** Because `BSB Cgm 6874` holds only the seven other *Regierungsbezirke*, Upper Bavaria's reports (held as a deposit of the *Historischer Verein von Oberbayern* in the Stadtarchiv München) are outside this dataset.
- **Candidate retrieval recall is unmeasured.** Regex candidate retrieval retained top pages per district (`13` districts had no infant-feeding or mortality section retrieved in the initial pass; a widened post-audit dialect search later surfaced unchecked candidate paragraphs in `Hilpoltstein` and `Immenstadt`). Regional pacifier counts may undercount dialect-specific terms.
- **Ecological correlation is not single-cause proof.** Regional covariates noted in the reports themselves (illegitimate birth shares, maternal field work, altitude, water quality, and sanitation) also varied alongside infant feeding.

### Links and open dataset

- **Original manuscripts:** Bayerische Staatsbibliothek, `BSB Cgm 6874(1)`-`Cgm 6874(207)`, Munich Digitization Center (`Public Domain Mark 1.0`).
- **Model:** `Kurrent Transcriber 1B`, `https://huggingface.co/13fragments/kurrent-transcriber-1b` (`CC BY-SA 4.0`, Zenodo DOI `10.5281/zenodo.24342061`).
- **Code and companion dataset repository:** `https://github.com/13fragments/bavarian-physikatsberichte` (Zenodo/Hugging Face release bundle staged locally in `dist/zenodo_package/`, including `cgm6874_pages.jsonl.gz`, `verified_bavaria_1860_infant_feeding.csv`, `verified_passages.csv`, `map_bavaria_1860_infant_feeding.geojson`, `verified_bavaria_1860_folk_medicine.csv`, `in_corpus_accuracy_eval.{csv,json}`, `eval_sample_references.tar.gz`, `DATACARD.md`, `LICENSE-CODE.txt`, `LICENSE-DATA.txt`, `CITATION.cff`, and `SHA256SUMS`; public Zenodo DOI to be inserted upon release).
- **Follow-up piece:** `publication/article_2_folk_medicine_outline_and_quotes.md` (chair legs, childbed sabres, boiled dog meat, and `25` verified folklore and healer quotations indexed in `verified_passages.csv`).
