# Image verification: goiter and cretinism in 27 districts

This log records the image check of the `27` districts whose `goiter_status` and `cretinism_status` were both `not_documented` after the split of `goiter_cretinism_status`, because the recorded evidence did not settle either condition (`DATACARD.md`, section 8). Each changed value in `verified_shards/`, `goiter_cretinism_status_mapping.csv`, and the compiled tables traces to a passage below.

Result: `25` of the `27` districts now have a value for at least one condition. Goiter: `9` endemic or frequent, `14` sporadic or localized, `4` not documented. Cretinism: `1` endemic or frequent, `9` sporadic or localized, `3` explicitly absent, `14` not documented. `Simbach` and `Thiersheim` stay `not_documented` in both columns.

- Reader: Claude Opus 5.5 (`claude-opus-5-5`), 2026-11-25. The same agent read every passage; no page was handed to a subagent.
- Method: `publication/posts/verification/PROTOCOL.md` (on branch `claude/dataset-popsci-ideas-bd60b3`). Pages were found with a keyword search of `data/transcripts/` (*Kropf*, *Kröpfe*, *kropfig*, *Satthals*, *Struma*, *Schilddrüse*, *Cretin*, *Kretin*, *Idiot*, *Blödsinn*, and misread forms). The machine text served only as a finding aid. Full-resolution IIIF images (`https://api.digitale-sammlungen.de/iiif/image/v2/<bsb_id>_<canvas:05d>/full/full/0/default.jpg`) were downloaded to `data/verification_scans/goiter_status/` (git-ignored) and read in crops.
- Value definitions: `DATACARD.md`, section 5. *Blödsinn* (idiocy), *Idiotismus*, and *Taubstummheit* (deaf-mutism) are not counted as cretinism. *Scropheln* (scrofula) is not goiter.
- Transcription: 1860 spelling and punctuation kept; `[...]` marks an omission, `[?]` a doubtful word.
- Confidence: high (every quoted word read), medium (one or two words marked `[?]`), low (not fit to publish). No passage is low.

## Coding rules applied

The section 5 definitions leave three cases open. The rules below follow the coding of the `47` rows already settled in `goiter_cretinism_status_mapping.csv`.

1. **Frequent, but only in named towns or villages: `sporadic_or_localized`.** The definition of `sporadic_or_localized` includes "limits it to some places". This follows `Kitzingen`, `Königshofen im Grabfeld`, `Landshut (Land)`, and `Eltmann`. It applies to `Bergzabern` (the town only), `Markt Bibart` cretinism (three places), `Marktbreit` cretinism (Bullenheim), and `Miltenberg` (four places). One settled row, `Kandel` (endemic cretinism in Hagenbach and Rheinzabern, `endemic_or_frequent`), does not follow this rule; it was not changed here.
2. **Frequent in a whole natural region of the district: `endemic_or_frequent`.** This follows `Deggendorf` (goiter frequent in the *Waldgegend*). It applies to `Wörth a.d. Donau` goiter.
3. **Conscription defects: `endemic_or_frequent` when the physician names goiter among the main defects, or when his own count makes it the largest cause of unfitness.** This follows `Griesbach`, `Kemnath`, and `Hofheim`. It applies to `Ottobeuren`, `Rehau`, `Windsheim`, and `Amberg (Stadt)`. Counts in which goiter is a minor cause are `sporadic_or_localized`, as in `Fürth` and `Regensburg (Land)`. This applies to `Amberg (Land)` and `Markt Erlbach`.
4. **"Nicht selten" (not rare) is not "frequent": `sporadic_or_localized`.** This follows `Eltmann` (Zeil) and `Uffenheim`. It applies to `Sulzbach`.
5. **Cretin-like or near-cretinous persons count as cretinism evidence**, as in `Rothenfels` and `Weiler`. This applies to `Bergzabern`, `Miltenberg`, and `Wolfstein i. Pf.`

## Passages

### amberg_land_c225  (Amberg (Land), Oberpfalz und Regensburg; bsb00026307 canvas 224-225; https://www.digitale-sammlungen.de/de/view/bsb00026307?page=225)
- Coding: goiter `sporadic_or_localized`; cretinism `not_documented`.
- German (ink), canvas 225: "Dabei ist es jedoch gleichfalls Thatsache, daß die Tuberkulose der Kropf und der Blödsinn nur sehr selten vorkommen [...]"
- English: "At the same time it is likewise a fact that tuberculosis, goiter, and idiocy occur only very rarely [...]"
- German (ink), canvas 224, causes of total unfitness among conscripts: "Kropf 3 [mal] " " " 0,5 %"
- English: "Goiter 3 times, or in 0.5%" (sixth of seven listed causes).
- Corrections against the machine text: canvas 224 "können als Ursachen" -> "kommen als Ursachen", "Tüberkilose" -> "Tuberkulose", "blösime" -> "Blödsinn".
- Confidence: high.
- Caveats: the ink has no comma after "Tuberkulose". *Blödsinn* is not counted as cretinism.

### amberg_stadt_c89  (Amberg (Stadt), Oberpfalz und Regensburg; bsb00026308 canvas 89; https://www.digitale-sammlungen.de/de/view/bsb00026308?page=89)
- Coding: goiter `endemic_or_frequent`; cretinism `not_documented`.
- German (ink): "Von 738 Conscribirten waren im zehnjährigen Durchschnitte 122. untauglich, demnach der 6te Theil u. zwar wegen Mangel des Maaßes 16. wegen Satthals u. Kropf . 39. wegen Brustleiden . 23. [...]"
- English: "Of 738 conscripts, on the ten-year average, 122 were unfit, thus the sixth part, namely for lack of height 16, for fat neck and goiter 39, for chest ailments 23 [...]"
- Corrections against the machine text: "Säthelt u. Kropf" -> "Satthals u. Kropf"; "122. 129 untäglich" -> "122. untauglich" (the ink has "129" struck through in the margin, corrected to "122").
- Confidence: high.
- Caveats: the physician gives counts, not a word such as "frequent". Goiter with fat neck is the largest of the `16` listed causes (`39` of `122` unfit), so rule 3 applies. *Taubstummheit* (1 case) is not counted as cretinism.

### augsburg_c90  (Augsburg, Schwaben und Neuburg; bsb00140577 canvas 90-91; https://www.digitale-sammlungen.de/de/view/bsb00140577?page=90)
- Coding: goiter `sporadic_or_localized`; cretinism `not_documented`.
- German (ink): "Man findet bei ihr in der Regel einen wenig ebenmäßigen Gliederbau, eckige Schädelbildung, insbesondere stark prominirende Backenknochen, hervorstehende Unterkiefer, auffallend schlechte Beschaffenheit der Zähne, Satthals und Kropf in allen erdenklichen Formen; Schlaffheit der Muskulatur und nicht selten auch Ausdruckslosigkeit der Physiognomien."
- English: "In it one finds as a rule a poorly proportioned build, angular skull, especially strongly prominent cheekbones, protruding lower jaws, strikingly bad teeth, fat neck and goiter in every conceivable form; slack muscles and not rarely also expressionless faces."
- Corrections against the machine text: "proximirende" -> "prominirende"; canvas 91 "Brophelin" -> "Scropheln".
- Confidence: high.
- Caveats: "ihr" is the older generation descended from the old imperial-city population and its offspring, as distinct from newcomers. Goiter is therefore limited to one group. Canvas 91 speaks of "eine Menge Blödsinniger" around 1800; that is idiocy, and historical.

### bergzabern_c30  (Bergzabern, Pfalz; bsb00140585 canvas 28 and 30; https://www.digitale-sammlungen.de/de/view/bsb00140585?page=30)
- Coding: goiter `sporadic_or_localized`; cretinism `sporadic_or_localized`.
- German (ink), canvas 28: "Nur die Wohnungsverhältnisse der Stadt Bergzabern sind entschieden ungünstig. Der Grund hievon liegt sowohl in der Bodenlage als im Baumateriale."
- English: "Only the housing conditions of the town of Bergzabern are decidedly unfavourable. The reason lies both in the site and in the building material."
- German (ink), canvas 30: "Die Folgen dieser Mißstände zeigen sich besonders in Scrophel-Anlagen, & in dem häufigen Vorkommen von Kröpfen & sonstigen dem Cretinismus nahe kommenden Erscheinungen, selbst die unverhältnißmäßig große Sterblichkeit in Bergzabern (denn in den 10 Jahren 1850/51 – 1859/60 kamen[?] auf 714 Geburten 736 Sterbefälle) läßt sich nur hieraus genügend erklären;"
- English: "The consequences of these ills show above all in scrofulous dispositions, and in the frequent occurrence of goiters and other phenomena close to cretinism; even the disproportionately high mortality in Bergzabern (in the 10 years 1850/51 – 1859/60 there were 736 deaths to 714 births) can only be explained sufficiently by this;"
- Corrections against the machine text: "Grosspred. Anlagen" -> "Scrophel-Anlagen"; "heutigen Vordeinen" -> "häufigen Vorkommen"; "demy Cactinismus" -> "dem Cretinismus"; "Bergpalast" -> "Bergzabern"; "Sterbe stelle" -> "Sterbefälle".
- Confidence: medium.
- Caveats: "diese Mißstände" are the damp, crowded houses of the walled town (canvas 28-29). The physician limits frequent goiter and near-cretinism to the town of Bergzabern, so rule 1 applies. The cretinism evidence is "close to cretinism" (rule 5).

### graefenberg_c70  (Gräfenberg, Oberfranken; bsb00140619 canvas 70; https://www.digitale-sammlungen.de/de/view/bsb00140619?page=70)
- Coding: goiter `not_documented`; cretinism `explicitly_absent`.
- German (ink): "[...] obgleich auch bei diesem Personen, welche auf einer sehr niedrigen Stufe geistiger Entwicklung stehen, sehr selten sind, Cretinismus nicht vorkommt, und Blödsinnige eine sehr vereinzelte Erscheinung sind."
- English: "[...] although in this [sex] too persons at a very low level of mental development are very rare, cretinism does not occur, and idiots are a very isolated phenomenon."
- Corrections against the machine text: "Cretinimus" -> "Cretinismus"; "kürzerlich und geistig fäischem" -> "körperlich und geistig frischem" (next sentence).
- Confidence: high.
- Caveats: the keyword search found no goiter statement in this report (only botanical *Scrophularineae*).

### herzogenaurach_c101  (Herzogenaurach, Oberfranken; bsb00144879 canvas 101-103; https://www.digitale-sammlungen.de/de/view/bsb00144879?page=101)
- Coding: goiter `sporadic_or_localized`; cretinism `not_documented`.
- German (ink), canvas 101: "Unter den Männern kommen Kröpfe fast gar nicht vor, – umso häufiger aber Brüche, gegen welche nur selten Bandagen getragen werden."
- English: "Among the men goiters hardly occur at all, but hernias all the more often, against which trusses are only rarely worn."
- German (ink), canvas 102: "Auch bei Weibspersonen sind Kröpfe eine Seltenheit, [...]"
- English: "Among women, too, goiters are a rarity, [...]"
- Corrections against the machine text: "dem Männern" -> "den Männern"; "mir selben Landagen" -> "nur selten Bandagen"; canvas 103 "Eigensen der Gebannten" -> "Eigensinn der Hebammen".
- Confidence: high.
- Caveats: the women's sentence goes on to say that goiter is seen in women only after excessive labour in childbirth ("in Folge übermäßiger Geburtsanstrengungen", canvas 102-103); the clause lacks a verb in the ink. With canvas 102 the statement covers both sexes, which settles the split-branch question.

### kempten_land_c63  (Kempten (Land), Schwaben und Neuburg; bsb00079161 canvas 63-64 and 149; https://www.digitale-sammlungen.de/de/view/bsb00079161?page=63)
- Coding: goiter `endemic_or_frequent`; cretinism `not_documented`.
- German (ink), canvas 63-64: "Nicht ohne allen Einfluß bleibt der Nordabfall der Alpen indem dadurch der[?] Idiotismus – Endemischer Blödsinn – in sporadischen Fällen gerade nicht selten ist. Im Landgerichtsbezirke Kempten befinden sich unter 26 Irren 4 männliche u. 8 weibliche Derselben. Zahlreich sind auch die Satthälse und Kröpfe vertreten, wie das Ergebniß der ärztlichen Visitation der Conscriptionspflichtigen Jünglinge alljährlich ausweist."
- English: "The northern slope of the Alps is not without influence, in that idiocy – endemic imbecility – in sporadic cases is by no means rare. In the Kempten district there are, among 26 insane, 4 male and 8 female of these. Fat necks and goiters are also numerous, as the medical examination of the conscripts shows every year."
- German (ink), canvas 149: "[...] so dürfte vor allem eine größere Abnahme des endemischen Blödsinnes und des Kropfes zu hoffen sein, davon schon im ersten Theile Erwähnung geschah."
- English: "[...] then above all a greater decline of endemic imbecility and of goiter may be hoped for, which was already mentioned in the first part."
- Corrections against the machine text: "Indemischer-blösin" -> "Endemischer Blödsinn"; "sperakischen" -> "sporadischen"; "Erren" -> "Irren"; "Satt-halse" -> "Satthälse"; "Konfektionspflichtigen" -> "Conscriptionspflichtigen"; "Aidsinnes und der Knopfes" -> "Blödsinnes und des Kropfes".
- Confidence: medium.
- Caveats: the physician calls the imbecility "endemic", but *Blödsinn* is not counted as cretinism, so cretinism stays `not_documented`.

### markt_bibart_c40  (Markt Bibart, Mittelfranken; bsb00145123 canvas 40-42; https://www.digitale-sammlungen.de/de/view/bsb00145123?page=40)
- Coding: goiter `endemic_or_frequent`; cretinism `sporadic_or_localized`.
- German (ink), canvas 40-41: "In drei Orten des Gerichtsbezirkes Mkt. Bibart kommen häufig Cretinen vor; am allermeisten in Iphofen, bei weitem minder in Einersheim und Nordheim. Der Cretinismus geht in der Regel mit Kröpfen und Skropheln Hand in Hand, doch habe ich denselben in Iphofen und Nordheim auch ohne Kropf und Skropheln beobachtet."
- English: "In three places of the Markt Bibart court district cretins occur frequently; most of all in Iphofen, far less in Einersheim and Nordheim. Cretinism as a rule goes hand in hand with goiters and scrofula, but in Iphofen and Nordheim I have also observed it without goiter and scrofula."
- German (ink), canvas 42: "Uebrigens sind auch ohne Cretinismus Kröpfe und Skropheln besonders in Iphofen heimisch und diese letzteren Leiden beeinträchtigen besonders [...]"
- English: "Moreover, even without cretinism, goiters and scrofula are at home especially in Iphofen, and these latter ailments impair especially [...]"
- Corrections against the machine text: "Izhofen" -> "Iphofen"; "Eimersheim" -> "Einersheim"; "Cretinismaus" -> "Cretinismus"; "Wroscheln" -> "Skropheln".
- Confidence: high.
- Caveats: cretinism is frequent in three named places only (rule 1). Goiter is called "heimisch" (native, endemic), "besonders" (especially) in Iphofen, which does not limit it to Iphofen; this is a judgment call between `endemic_or_frequent` and `sporadic_or_localized`.

### markt_erlbach_c57  (Markt Erlbach, Mittelfranken; bsb00143123 canvas 57 and 107; https://www.digitale-sammlungen.de/de/view/bsb00143123?page=57)
- Coding: goiter `sporadic_or_localized`; cretinism `not_documented`.
- German (ink), canvas 57, on Neuhof: "Frühere Beobachter wollten nach dem Verlaufe des Gemeindebaches[?] häufiger vorkommende Kröpfe und Neigung zum Cretinismus bemerkt haben. In der That fand sich in Neuhof eine Familie mit 1 weiblichen [mit Klumpfüßen behafteten] und 2 männlichen Cretinen höheren Grades, die längst gestorben sind, außerdem aber weder ein häufigeres Vorkommen von Kröpfen als anderwärts, noch auch eine anderweitige Spur von Cretinismus [...]"
- English: "Earlier observers claimed to have noticed goiters occurring more often, and a tendency to cretinism, along the course of the village brook[?]. Indeed there was in Neuhof a family with 1 female [club-footed] and 2 male cretins of higher degree, who died long ago; but apart from that neither a more frequent occurrence of goiters than elsewhere, nor any other trace of cretinism [...]"
- German (ink), canvas 107, conscription table for the age classes 1836-1839: column "Satthals mit Athembeschwerde", total `4`; column "Kropf", total `1`; "Summe der Visitirten" `346`, unfit `79`.
- English: fat neck with breathing difficulty 4, goiter 1, out of 346 examined.
- Corrections against the machine text: "Brotechter" -> "Beobachter"; "Krüpe" -> "Kröpfe"; "Continentus" -> "Cretinismus"; "Neudorf" -> "Neuhof"; "Ortänen" -> "Cretinen". The machine text of the canvas 107 table is unusable; the two columns were read from the ink.
- Confidence: medium.
- Caveats: the conscription counts are small (rule 3), and the Neuhof passage says goiter is not more frequent there than elsewhere. The cretin family is long dead and the physician names no living case, so cretinism stays `not_documented`. The table is from 1836-1839, older than the report.

### marktbreit_c20  (Marktbreit, Unterfranken und Aschaffenburg; bsb00145124 canvas 20; https://www.digitale-sammlungen.de/de/view/bsb00145124?page=20)
- Coding: goiter `endemic_or_frequent`; cretinism `sporadic_or_localized`.
- German (ink): "Nicht übergehen darf ich hier den Cretinismus, der in Bullenheim endemisch ist. [...] Interessant ist auch noch das im Landgerichtsbezirk sehr häufige Vorkommen der Kröpfe, besonders in Bullenheim. [...] Der Kalkgehalt des Trinkwassers und der zugleich endemische Cretinismus mögen zur Häufigkeit dieser Neubildung beitragen. Der Jodgehalt der Atmosphäre differirt gewiß nichts gegen andere von Kropf freie Gegenden."
- English: "I must not pass over here cretinism, which is endemic in Bullenheim. [...] Also of interest is the very frequent occurrence of goiters in the court district, especially in Bullenheim. [...] The lime content of the drinking water and the cretinism endemic at the same time may contribute to the frequency of this growth. The iodine content of the atmosphere surely does not differ at all from other goiter-free regions."
- Corrections against the machine text: "Rentismus" / "Rentinismus" -> "Cretinismus"; "Boxpfän" -> "Koryphäe[?]" (omitted sentence on Virchow); "Kers" -> "Vers"; "hypetrophicum" -> "hypertrophicum"; "Stalkgehalt" -> "Kalkgehalt"; "Lodgehalt" -> "Jodgehalt".
- Confidence: high for the quoted sentences; the omitted folk verse ("[...] von Iphof, hat er kein Buckel, hat [...] Kropf") has doubtful words and is not quoted.
- Caveats: goiter is very frequent in the whole district; cretinism is endemic in Bullenheim only (rule 1). The omitted sentence names Rudolf Virchow's monograph on cretinism. The last sentence is a second physician who dismisses iodine; it may interest Post 06.

### memmingen_c43  (Memmingen, Schwaben und Neuburg; bsb00145125 canvas 43; https://www.digitale-sammlungen.de/de/view/bsb00145125?page=43)
- Coding: goiter `sporadic_or_localized`; cretinism `not_documented`.
- German (ink): "Allein wie der Schlag in Beziehung auf Schönheit des Körperbaues überhaupt kein guter ist, so sind auch diese alten Weiber oft ungewöhnlich häßlich, und tragen die Spuren der Scrophulosis, wie Kröpfe, Zahnlosigkeit[?] und Kahlköpfigkeit oft aus den besten Jahren des mittlern Lebensalters bis in das höchste Alter."
- English: "But as the stock is not a good one in beauty of build, so these old women too are often unusually ugly, and bear the traces of scrofula, such as goiters, toothlessness[?], and baldness, often from the best years of middle age into the highest age."
- Corrections against the machine text: "Suroplosis" -> "Scrophulosis"; "Gahelosigkeit" -> "Zahnlosigkeit[?]".
- Confidence: medium.
- Caveats: the split branch read this page as scrofula, not goiter. The ink names goiter ("Kröpfe") as one sign of scrofula, a theory of the time. It concerns old women, so goiter is limited to one group.

### miltenberg_c537  (Miltenberg, Unterfranken und Aschaffenburg; bsb00145124 canvas 537 and 546; https://www.digitale-sammlungen.de/de/view/bsb00145124?page=537)
- Coding: goiter `sporadic_or_localized`; cretinism `sporadic_or_localized`.
- German (ink), canvas 537: "Wo Wohlhabenheit herrscht, und Ordnung und Sinn für Reinlichkeit besteht, da ist auch die physische Constitution besser, doch kommen auch sehr viele verkrüppelte kretinartige Gestalten vor, so besonders in Bürgstadt, dann auch Miltenberg, Eichenbühl und Rüdenau letzterer Ort zu den ärmsten gehörend; so sieht man sehr Viele mit Kröpfen und mit großem Umfange behaftet mit stupiden kretinartigen Gesichtern."
- English: "Where prosperity prevails, and order and a sense of cleanliness exist, the physical constitution is also better; but there are also very many crippled, cretin-like figures, especially in Bürgstadt, then also Miltenberg, Eichenbühl, and Rüdenau, the last being among the poorest places; there one sees very many afflicted with goiters, and of large size, with dull cretin-like faces."
- German (ink), canvas 546: "[...] daher auch wohl diese Verkrüpplungen z B Kropf Cretinartiges Aussehen, [welche, struck through] in solchen Orten, wie schon erwähnt, häufig vorkommen."
- English: "[...] hence probably also these deformities, e.g. goiter, cretin-like appearance, which, as already mentioned, occur frequently in such places."
- Corrections against the machine text: "physikste" -> "physische"; "kretievartige" -> "kretinartige"; "Burgstadt" -> "Bürgstadt"; "Krüpfen" -> "Kröpfen"; canvas 546 "Lieder" -> "Kinder", "Lretierartiges" -> "Cretinartiges".
- Confidence: medium.
- Caveats: the first keyword search missed canvas 537 because of the misreadings "Krüpfen" and "kretievartige". Both conditions are frequent in four named places, one of them the town of Miltenberg (rule 1). The cretinism evidence is "cretin-like" (rule 5). The physician links it to poverty, poor diet, and carrying loads on the head.

### oberdorf_c64  (Oberdorf, Schwaben und Neuburg; bsb00146468 canvas 64-65; https://www.digitale-sammlungen.de/de/view/bsb00146468?page=65)
- Coding: goiter `sporadic_or_localized`; cretinism `not_documented`.
- German (ink): "Unter den angebornen Krankheiten kommen Kröpfe sehr selten vor. Der Blödsinn ist nur wenigen Individuen eigen, sodaß etwa 6–8 im ganzen Amtsbezirke sich befinden."
- English: "Among congenital diseases, goiters occur very rarely. Idiocy affects only a few individuals, so that there are about 6–8 in the whole district."
- Corrections against the machine text: none in the quoted sentences.
- Confidence: high.
- Caveats: *Blödsinn* is not counted as cretinism.

### oettingen_c25  (Öttingen, Schwaben und Neuburg; bsb00044079 canvas 25; https://www.digitale-sammlungen.de/de/view/bsb00044079?page=25)
- Coding: goiter `not_documented`; cretinism `explicitly_absent`.
- German (ink): "Die geistigen Fähigkeiten sind meist normal vorhanden und es giebt nur 3. Idioten, nämlich Personen, welche von Geburt aus wenig oder keine Verstandes- und intellektuellen Kräfte besitzen; Kretinen giebt es nicht."
- English: "Mental faculties are mostly normal, and there are only 3 idiots, that is, persons who from birth have little or no understanding and intellectual powers; there are no cretins."
- Corrections against the machine text: "Wirten" -> "Idioten"; "Verknüppelungen" -> "Verkrüppelungen" (earlier sentence).
- Confidence: high.
- Caveats: the keyword search found no goiter statement in this report.

### ottobeuren_c61  (Ottobeuren, Schwaben und Neuburg; bsb00145149 canvas 60-61; https://www.digitale-sammlungen.de/de/view/bsb00145149?page=61)
- Coding: goiter `endemic_or_frequent`; cretinism `not_documented`.
- German (ink): "Als tauglich wurden erklärt 821; als untauglich 268. Die am Meisten hervortretenden, die Untauglichkeit bedingenden Fehler und Gebrechen, waren außer dem seltenen Mangel an vorgeschriebenem Maaß: 1. Fehler der Extremitäten, Annäherung zum Plattfuß, Krampfadern; 2. Kurzsichtigkeit u. Harthörigkeit; 3. Satthals und Kropf; 4. Nächtliches Unvermögen den Harn zu halten."
- English: "821 were declared fit, 268 unfit. The most prominent faults and infirmities causing unfitness, apart from the rare lack of the prescribed height, were: 1. faults of the limbs, tendency to flat foot, varicose veins; 2. short sight and hardness of hearing; 3. fat neck and goiter; 4. nightly inability to hold urine."
- Corrections against the machine text: "seltene Mangel an vorgeschriebenen" -> "seltenen Mangel an vorgeschriebenem".
- Confidence: high.
- Caveats: rule 3 (main conscription defect). The former combined value was `sporadic_or_localized`. The next sentence says that conspicuous infirmities "visible to everyone" were rare.

### pottenstein_c36  (Pottenstein, Oberfranken; bsb00146472 canvas 36; https://www.digitale-sammlungen.de/de/view/bsb00146472?page=36)
- Coding: goiter `sporadic_or_localized`; cretinism `sporadic_or_localized`.
- German (ink): "An Krankheiten und Gebrechen, die in endemischen Verhältnissen in der Beschaffenheit und Lebensweise der Bevölkerung ihren Grund haben, sind Eingeweide-Brüche und Plattfüße, hervorzuheben. Der Kropf ist selten, eben so der Cretinismus."
- English: "Among diseases and infirmities rooted in endemic conditions in the constitution and way of life of the population, hernias and flat feet are to be stressed. Goiter is rare, as is cretinism."
- Corrections against the machine text: "Eingerweite Brüche und Plattfuhle" -> "Eingeweide-Brüche und Plattfüße"; "Centinissaus" -> "Cretinismus".
- Confidence: high.
- Caveats: none.

### rehau_c37  (Rehau, Oberfranken; bsb00146475 canvas 37; https://www.digitale-sammlungen.de/de/view/bsb00146475?page=37)
- Coding: goiter `endemic_or_frequent`; cretinism `not_documented`.
- German (ink): "Die Hauptgebrechen der Conscriptionspflichtigen sind allgemeine Schwächlichkeit, Ohrenkrankheiten, Satthaelse, Verunstaltungen des Koerpers und der Brust, Kröpfe, Ungelenkigkeit des Körpers."
- English: "The main infirmities of the conscripts are general weakness, ear diseases, fat necks, deformities of the body and chest, goiters, stiffness of the body."
- Corrections against the machine text: none in the quoted sentence; next sentence "Sropheln" -> "Scropheln".
- Confidence: high.
- Caveats: rule 3 (main conscription defect).

### roding_c48  (Roding, Oberpfalz und Regensburg; bsb00031112 canvas 48 and 50; https://www.digitale-sammlungen.de/de/view/bsb00031112?page=48)
- Coding: goiter `sporadic_or_localized`; cretinism `explicitly_absent`.
- German (ink), canvas 48: "Verkrüppelte, krumme, lahme, hinkende, schielende, bucklige und kropfige Personen kommen wohl vor, aber nicht häufig."
- English: "Crippled, crooked, lame, limping, squinting, hunchbacked, and goitrous persons do occur, but not frequently."
- German (ink), canvas 50: "Blödsinnige und Irren gibt es im ganzen Bezirke daher[?] nur 9 Individuen, Cretinismus kommt nicht vor."
- English: "Of idiots and insane there are only 9 individuals in the whole district; cretinism does not occur."
- Corrections against the machine text: "krimme" -> "krumme"; "bücklige" -> "bucklige"; "häufige" -> "häufig."; "Blössinnige und Jeren" -> "Blödsinnige und Irren"; "nicht von" -> "nicht vor".
- Confidence: medium.
- Caveats: canvas 94 repeats the cretinism statement ("aber eigentliche Cretinen nicht", machine text, not needed).

### rothenburg_ob_der_tauber_c129  (Rothenburg ob der Tauber, Mittelfranken; bsb00143122 canvas 54 and 129; https://www.digitale-sammlungen.de/de/view/bsb00143122?page=129)
- Coding: goiter `endemic_or_frequent`; cretinism `endemic_or_frequent`.
- German (ink), canvas 54: "Im Gegentheile finden sich im Bezirke gar mancherlei Mißbildungen, u. alle Abstufungen des Cretinismus, namentlich in den Orten, in denen das Trinkwasser aus Quellen über Gypslager kommt."
- English: "On the contrary, there are in the district all kinds of malformations, and all grades of cretinism, especially in the places where the drinking water comes from springs over gypsum beds."
- German (ink), canvas 129: "Endemisch kommt der Kropf und Cretinismus in Folge der aus den oben angeführten Gypslagern kommenden, viel schwefelsauren Kalk enthaltenden Quellen vor. Doch wird der Genuß des Wassers in neuester Zeit möglichst gemieden."
- English: "Goiter and cretinism occur endemically as a result of the springs that come from the gypsum beds named above and contain much calcium sulphate. But the drinking of this water has lately been avoided as far as possible."
- Corrections against the machine text: "Creatinismus" -> "Cretinismus"; canvas 54 "Offenheim" -> "Uffenheim".
- Confidence: high.
- Caveats: "namentlich" (especially) does not limit the condition to those places, so rule 1 does not apply. The cause is the physician's theory.

### scheinfeld_c27  (Scheinfeld, Mittelfranken; bsb00145145 canvas 27, 110, and 111; https://www.digitale-sammlungen.de/de/view/bsb00145145?page=27)
- Coding: goiter `sporadic_or_localized`; cretinism `sporadic_or_localized`.
- German (ink), canvas 27: "Vom endemischen Cretinismus und Kropf ist der Bezirk jedoch, aus Terrainursachen – wenigstens insofern, als man schwefelsauren Kalk beschuldigen könnte, fast frei, wenn derselbe auch aus andern Ursachen vorkommt [...]"
- English: "Of endemic cretinism and goiter, however, the district is almost free as far as terrain causes go – at least insofar as one could blame calcium sulphate – even though it does occur from other causes [...]"
- German (ink), canvas 110: "Größer ist dagegen die Zahl der Blöd- und Stumpfsinnigen. Sie beträgt gegenwärtig 13; auf 100 Seelen kommen 0,15 % oder auf 446,46 1 Blödsinniger. Ob diese Unglücklichen Cretins oder Idioten zu nennen seyen ist bei den verschiedenen darüber herrschenden Ansichten auch verschieden zu entscheiden."
- English: "Larger, on the other hand, is the number of the imbecile and dull-witted. It is at present 13; 0.15% of the population, or 1 imbecile per 446.46. Whether these unfortunates should be called cretins or idiots is decided differently according to the various views on the matter."
- German (ink), canvas 111: "An diese Definitionen anschließend sind die Mehrzahl im hiesigen Bezirke als Cretins zu betrachten. Denn der Blödsinn ist 9[?] mal angeboren und mit wenig Ausnahmen finden sich auch solche körperliche Zustände, die auf Rechnung von Boden- und Wohnungsverhältnissen gesetzt werden müssen, wie Kropf- und Zwergbildung, Knochenverkrümmungen & Taubstummheit und Sprachfehler."
- English: "Following these definitions [Virchow's], the majority in this district are to be regarded as cretins. For the imbecility is congenital in 9[?] cases, and with few exceptions there are also bodily conditions that must be put down to soil and housing, such as goiter and dwarfism, bone deformities and deaf-mutism, and speech defects."
- Corrections against the machine text: "kostensauren" -> "kohlensauren" (earlier sentence); "vorkanht" -> "vorkommt"; "Idirten" -> "Idioten"; "Zweigbildung" -> "Zwergbildung". "fast" before "frei" is an interlinear insertion in the ink.
- Confidence: medium.
- Caveats: the physician classes most of the `13` imbeciles as cretins, so this is a statement about cretinism. The district is "almost free" of endemic goiter and cretinism; goiter appears among the cretins. The former combined value was `endemic_or_frequent`.

### simbach_c107  (Simbach, Niederbayern; bsb00110698 canvas 107 and 109; https://www.digitale-sammlungen.de/de/view/bsb00110698?page=107)
- Coding: goiter `not_documented`; cretinism `not_documented`.
- German (ink), canvas 107, quoting Joseph Hazzi's statistics of 1804: "Eine kleine, unansehnliche, meist krüppelhaftige, kropfige oder mit andern Leibsschäden beschwerte Menschenrace bewohnt die Landschaft, wovon sie die treffende aber nie zu stellende Rekrutenzahl genugsam[?] zeigt."
- English: "A small, unsightly, mostly crippled, goitrous people, or one burdened with other bodily defects, inhabits the landscape, as its due but never delivered number of recruits sufficiently shows."
- German (ink), canvas 109: "Die Statistik des Josef Hazzi erschien im Jahre 1804 und nun nach 56 Jahren ist der Landgerichtsbezirk Simbach, früher Amt Julbach, eine der schönsten und fruchtbarsten Gegenden des Vaterlandes, und die Menschenrace ist von schöner Natur und kräftiger Körperkonstitution [...]"
- English: "Hazzi's statistics appeared in 1804, and now, after 56 years, the Simbach district, formerly the office of Julbach, is one of the most beautiful and fertile regions of the fatherland, and the people are of fine nature and strong bodily constitution [...]"
- Corrections against the machine text: canvas 109 "Seibach" -> "Simbach"; "Fulbach" -> "Julbach"; "Menschenruhe" -> "Menschenrace".
- Confidence: medium.
- Caveats: the only goiter word is in a quotation from 1804, which the physician sets against the strong population of 1860. It does not describe goiter at the time of the report. The former value `endemic_or_frequent` rested on this quotation.

### sulzbach_c53  (Sulzbach, Oberpfalz und Regensburg; bsb00105945 canvas 53; https://www.digitale-sammlungen.de/de/view/bsb00105945?page=53)
- Coding: goiter `sporadic_or_localized`; cretinism `not_documented`.
- German (ink): "Besondere Krankheiten kommen im hiesigen Landgerichte nicht vor; die Wechselfieber zeigen sich erst seit ein paar Jahren häufiger; Scropheln und Tuberkel sind nicht häufig; Kröpfe jedoch nicht selten."
- English: "No particular diseases occur in this district; intermittent fevers have become more frequent only in the last few years; scrofula and tubercles are not frequent; goiters, however, not rare."
- Corrections against the machine text: "Xiropheln" -> "Scropheln" (already logged in the shard).
- Confidence: high.
- Caveats: the split branch read this page as scrofula only. The ink names goiter in a separate clause. "Nicht selten" (not rare) is weaker than "frequent" (rule 4), and the sentence opens with "no particular diseases occur". The former combined value was `endemic_or_frequent`.

### thiersheim_c58  (Thiersheim, Oberfranken; bsb00145150 canvas 58; https://www.digitale-sammlungen.de/de/view/bsb00145150?page=58)
- Coding: goiter `not_documented`; cretinism `not_documented`.
- German (ink): "Die geistige Constitution der Bevölkerung ist im Allgemeinen gut, und nur ausnahmsweise finden sich einzelne krüppelhafte und blödsinnige Subjekte vor."
- English: "The mental constitution of the population is in general good, and only exceptionally are there individual crippled and idiotic subjects."
- Corrections against the machine text: "nun" -> "nur"; "Seuljekte" -> "Subjekte".
- Confidence: high.
- Caveats: no goiter or cretinism statement was found in this report. *Blödsinn* is not counted as cretinism. The former value `sporadic_or_localized` has no support in the pages found.

### wemding_c170  (Wemding, Schwaben und Neuburg; bsb00094605 canvas 170; https://www.digitale-sammlungen.de/de/view/bsb00094605?page=170)
- Coding: goiter `sporadic_or_localized`; cretinism `not_documented`.
- German (ink): "Dagegen sind Kröpfe hier eine große Seltenheit; die Schilddrüse ist nur bei Mehrgebärenden zuweilen leicht angeschwollen."
- English: "Goiters, on the other hand, are a great rarity here; the thyroid is only sometimes slightly swollen in women who have borne several children."
- Corrections against the machine text: "Dagen" -> "Dagegen".
- Confidence: high.
- Caveats: none.

### windsheim_c19  (Windsheim, Mittelfranken; bsb00143119 canvas 19-20, 25-26, and 28-29; https://www.digitale-sammlungen.de/de/view/bsb00143119?page=19)
- Coding: goiter `endemic_or_frequent`; cretinism `sporadic_or_localized`.
- German (ink), canvas 19-20: "In dieser Beschaffenheit des Trinkwassers, namentlich in dem Gypsgehalte desselben, möchte, wenn nicht allein, doch hauptsächlich die Ursache des häufigen Vorkommens des Kropfes im Bezirke, sowie des Idiotismus (unter diesem den angeborenen Schwachsinn vom niedrigsten Grade bis zum Cretinismus verstanden) zu suchen sein."
- English: "In this quality of the drinking water, above all in its gypsum content, the cause, if not the only one then the main one, of the frequent occurrence of goiter in the district, and of idiocy (meaning congenital feeble-mindedness from the lowest degree up to cretinism), may be sought."
- German (ink), canvas 25-26: "In manchen Ortschaften begegnet man allerdings häufig verkümmerten Gestalten und selbst Cretinen, doch im Ganzen findet man dergleichen Individuen bei Weitem nicht mehr so häufig vor, wie noch vor etwa 30 Jahren [...]"
- English: "In some localities one does often meet stunted figures and even cretins, but on the whole such individuals are by far not as frequent as about 30 years ago [...]"
- German (ink), canvas 28-29: "[...] von 100 Conscriptionspflichtigen sind jedoch 4. wegen Mangels an Größe und 32. wegen Gebrechen, unter welchen der Kropf oben an steht, untauglich."
- English: "[...] of 100 conscripts, however, 4 are unfit for lack of height and 32 for infirmities, among which goiter stands at the top."
- Corrections against the machine text: "Gyzsgehalte" -> "Gypsgehalte"; "(retinismus" -> "Cretinismus".
- Confidence: high.
- Caveats: *Idiotismus* is not counted as cretinism. Cretins are named in some localities only (rule 1).

### woerth_a_d_donau_c167  (Wörth a.d. Donau, Oberpfalz und Regensburg; bsb00003358 canvas 167, 171, and 173-174; https://www.digitale-sammlungen.de/de/view/bsb00003358?page=167)
- Coding: goiter `endemic_or_frequent`; cretinism `sporadic_or_localized`.
- German (ink), canvas 167: "Die physischen Anstrengungen des Landvolkes besonders in der frühesten Jugend, wie es bei den Waldbewohnern Usus ist, geben häufig Anlaß zu Kröpfen, Hernien und Verkrümmungen der Gliedmaßen, welche Gebrechen in der Waldgegend auffallend häufig vorzukommen pflegen."
- English: "The physical exertions of the country people, especially in earliest youth, as is the custom among the forest dwellers, often give rise to goiters, hernias, and deformed limbs, infirmities that are strikingly frequent in the forest region."
- German (ink), canvas 171: "Aus den Conscriptions-Listen von zehn Jahren ergibt sich, daß im Landgerichtsbezirke 4,86 wegen Kropf und Scrophulosis u. 1,40 wegen schwachen Brustbaus untauglich waren."
- English: "The conscription lists of ten years show that in the district 4.86 were unfit because of goiter and scrofula and 1.40 because of weak chest."
- German (ink), canvas 173-174: "Die höchste Stufe endlich der Scrophulosis bildet der Cretinismus, der daher[?] in Zeitldorn, welches eine ganz sonnige und gesunde Lage hat, in einigen Familien angetroffen wird."
- English: "The highest stage of scrofula, finally, is cretinism, which is found in some families in Zeitldorn, a place with a quite sunny and healthy site."
- German (ink), canvas 174: "Als Resumé unserer Erfahrung ergibt sich, daß allerdings in der Waldgegend, dessen Gebirgslager aus Granit besteht, die Kropfbildung vorherrschend ist [...]"
- English: "As a summary of our experience it follows that in the forest region, whose rock is granite, goiter is indeed predominant [...]"
- Corrections against the machine text: "Uthus" -> "Usus"; "Anla.3" -> "Anlaß"; "Hermen" -> "Hernien"; "Scrophulchis" -> "Scrophulosis"; "1,4o" -> "1,40"; "Presumé" -> "Resumé".
- Confidence: medium.
- Caveats: goiter is frequent in the forest region of the district (rule 2). Canvas 173 also says goiter is the most frequent form of scrofula, "besonders beim weiblichen Geschlechte". The unit of "4,86" is not stated (probably percent of conscripts). Cretinism is limited to some families in one village.

### wolfstein_i_pf_c71  (Wolfstein i. Pf., Pfalz; bsb00144890 canvas 65, 71-72, and 86; https://www.digitale-sammlungen.de/de/view/bsb00144890?page=71)
- Coding: goiter `sporadic_or_localized`; cretinism `sporadic_or_localized`.
- German (ink), canvas 65: "Durch die physischen Verhältnisse wahrscheinlich in ihrer Gesammtheit, welche eine Landschaft darbietet, werden endemische Krankheiten wie Kropfbildung, Steinkrankheit, Nierenblutung in manchen Landschaften in scharf abgegränzter Weise hervorgerufen; eine derartige Krankheit läßt sich in unserm Cantone nicht nachweisen; unsere Krankheitsverhältnisse haben nichts endemisch Absonderliches [...]"
- English: "Through the physical conditions of a landscape, probably taken as a whole, endemic diseases such as goiter, stone disease, and renal bleeding are produced in some landscapes in sharply bounded fashion; no such disease can be shown in our canton; our disease conditions have nothing endemically peculiar [...]"
- German (ink), canvas 71-72: "Was die Krankheiten des männlichen Geschlechtes u. der Erwachsenen überhaupt betrifft so kommen Anschwellungen u. Vergrößerungen im Bereiche der Schilddrüse von den einfachsten Formen bis zur steinharten Entartung vor und können wir eine sehr reichhaltige Musterkarte von Schilddrüsenkrankheiten aufstellen."
- English: "As for the diseases of the male sex and of adults in general, swellings and enlargements of the thyroid occur, from the simplest forms to stone-hard degeneration, and we could set up a very rich sample card of thyroid diseases."
- German (ink), canvas 86: "Was Störungen der Geisteskräfte u. Geisteskrankheiten betrifft so kommen angeborne Geistesschwäche, Blödsinn u. cretinismusartige Zustände im Kantone nicht häufig vor;"
- English: "As for disorders of the mental powers and mental diseases, congenital feeble-mindedness, idiocy, and cretinism-like states are not frequent in the canton;"
- Corrections against the machine text: "Erwechseln" -> "Erwachsenen"; "Schilddreisen" -> "Schilddrüsen"; "Westerichs" -> "Westrichs"; "Blödsin" -> "Blödsinn"; "ein Kantone" -> "im Kantone".
- Confidence: high.
- Caveats: canvas 65 denies endemic goiter, not goiter; canvas 71-72 reports thyroid swelling in all forms. The former value `explicitly_absent` is not supported. Cretinism evidence is "cretinism-like" (rule 5). Canvas 144 (machine text, not read) names goiter as a result of women carrying loads on the head.

## Summary

| District | Former combined | Goiter | Cretinism |
| --- | --- | --- | --- |
| Amberg (Land) | sporadic_or_localized | sporadic_or_localized | not_documented |
| Amberg (Stadt) | sporadic_or_localized | endemic_or_frequent | not_documented |
| Augsburg | sporadic_or_localized | sporadic_or_localized | not_documented |
| Bergzabern | endemic_or_frequent | sporadic_or_localized | sporadic_or_localized |
| Gräfenberg | explicitly_absent | not_documented | explicitly_absent |
| Herzogenaurach | explicitly_absent | sporadic_or_localized | not_documented |
| Kempten (Land) | endemic_or_frequent | endemic_or_frequent | not_documented |
| Markt Bibart | endemic_or_frequent | endemic_or_frequent | sporadic_or_localized |
| Markt Erlbach | sporadic_or_localized | sporadic_or_localized | not_documented |
| Marktbreit | endemic_or_frequent | endemic_or_frequent | sporadic_or_localized |
| Memmingen | sporadic_or_localized | sporadic_or_localized | not_documented |
| Miltenberg | endemic_or_frequent | sporadic_or_localized | sporadic_or_localized |
| Oberdorf | sporadic_or_localized | sporadic_or_localized | not_documented |
| Öttingen | explicitly_absent | not_documented | explicitly_absent |
| Ottobeuren | sporadic_or_localized | endemic_or_frequent | not_documented |
| Pottenstein | sporadic_or_localized | sporadic_or_localized | sporadic_or_localized |
| Rehau | endemic_or_frequent | endemic_or_frequent | not_documented |
| Roding | explicitly_absent | sporadic_or_localized | explicitly_absent |
| Rothenburg ob der Tauber | endemic_or_frequent | endemic_or_frequent | endemic_or_frequent |
| Scheinfeld | endemic_or_frequent | sporadic_or_localized | sporadic_or_localized |
| Simbach | endemic_or_frequent | not_documented | not_documented |
| Sulzbach | endemic_or_frequent | sporadic_or_localized | not_documented |
| Thiersheim | sporadic_or_localized | not_documented | not_documented |
| Wemding | sporadic_or_localized | sporadic_or_localized | not_documented |
| Windsheim | endemic_or_frequent | endemic_or_frequent | sporadic_or_localized |
| Wolfstein i. Pf. | explicitly_absent | sporadic_or_localized | sporadic_or_localized |
| Wörth a.d. Donau | endemic_or_frequent | endemic_or_frequent | sporadic_or_localized |

Four findings correct the split branch's reading of the shard notes. `Sulzbach` and `Memmingen` name goiter in the ink, next to scrofula. `Herzogenaurach` covers women too (canvas 102). `Wolfstein i. Pf.` was `explicitly_absent` in the combined column, but its physician denies only *endemic* goiter and reports thyroid swellings of all forms.

Judgment calls for review: `Amberg (Stadt)` and `Ottobeuren` (rule 3), `Markt Bibart` goiter ("heimisch"), `Sulzbach` (rule 4), `Wörth a.d. Donau` goiter (rule 2), and `Markt Erlbach` cretinism (a dead family, coded `not_documented`).

Strongest single hook for Post 06: Marktbreit, canvas 20. The physician calls goiter very frequent, blames the lime in the water, and adds: "Der Jodgehalt der Atmosphäre differirt gewiß nichts gegen andere von Kropf freie Gegenden." ("The iodine content of the atmosphere surely does not differ at all from other goiter-free regions.") A second doctor set iodine aside.
