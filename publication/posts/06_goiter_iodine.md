# Post 6: The doctor who weighed the iodine theory and set it aside

- **Type:** quick post with map, or short thread.
- **Status:** quotes checked against the page images (verification log: `verification/goiter.md`). The map uses the goiter column, `goiter_status`, of the image-verified district table (`data/dataset/verified_bavaria_1860_infant_feeding.csv`). Cretinism has its own column, `cretinism_status`, and is not on the map. Both columns are not yet in a published dataset version (see Caveats). One page from the first keyword search failed: Vilseck says scrofula (*Scropheln*), not goiter, and is left out.
- **Image 1:** `publication/figures/fig_bavaria_1860_goiter_map.png` (district seats colored by how the physician described goiter).
- **Image 2:** Wiesentheid, `bsb00146483` canvas 265, crop of "der Jodgehalt der Luft und der Nahrungsmittel ist vorerst noch zweifelhaft, sein Einfluß aber jedenfalls untergeordnet." Viewer: https://www.digitale-sammlungen.de/de/view/bsb00146483?page=265

## Single post

Franconia, around 1860. The Wiesentheid doctor weighs every theory of cretinism, iodine included: "the iodine content of the air and of food is for now still doubtful, but its influence is in any case secondary." He blamed the hard water. The answer was iodine.

## Short thread

1. Goiter and cretinism were common in parts of Bavaria around 1860. The district physicians described them, district by district. The map shows goiter: where they called it endemic or frequent (red), rare or local (amber), or absent (blue).

2. Their explanations fit their time. Uffenheim: "in the female sex the carrying of heavy loads on the head is a not uncommon cause of the development of goiter." Zeil, near Eltmann: goiters, especially in women, "may come from heavy work, births, the carrying of heavy loads."

3. The doctor of Wiesentheid gave cretinism a section of its own, because the cretins of his region lived in one small area: the villages of Castell, Wiesenbronn and Rüdenhausen.

4. He weighed the theories: deep valleys, lack of light, hard water, lack of iodine. His villages are open and sunny, so he rejected valleys and darkness. On iodine: "the iodine content of the air and of food is for now still doubtful, but its influence is in any case secondary."

5. His verdict: "With us the lime content of the water is without doubt an essential factor," above all in Castell and Wiesenbronn, where the hard water "is a known calamity."

6. Today we know that iodine deficiency is the main cause of endemic goiter and cretinism. Iodized salt now prevents both. The answer was on his desk around 1860, in the theory he set aside.

7. Weiler, in the Allgäu: women "are often disfigured by fat necks and goiters", and "there are some families in which nearly all the children approach cretinism." Schillingsfürst: in the upper Tauber valleys, "cretinism occurs here in all its variations."

8. Source: the 1858-1861 Bavarian district physicians' reports (Bayerische Staatsbibliothek, Cgm 6874), open data: https://doi.org/10.5281/zenodo.24523213

## Original German

- Wiesentheid (`bsb00146483` canvas 263-264): "Weil aber eben nur jener kleine und eng begränzte Bezirk die Heimath der Cretinen in unsrer Gegend ist, so darf eine nähere Erörterung der möglichen Ursache davon, so wie ein Blick auf die bisherige Lehre vom Cretinismus hier nicht umgangen werden!"
- Wiesentheid (canvas 265): "[...] der Jodgehalt der Luft und der Nahrungsmittel ist vorerst noch zweifelhaft, sein Einfluß aber jedenfalls untergeordnet."
- Wiesentheid (canvas 267): "Bei uns ist ohne Zweifel der Kalkgehalt des Wassers ein wesentliches Moment und es ist nicht nöthig, den ersten Grund der Entstehung jener Bildungsanomalie wo anders zu suchen, als eben in dem harten Wasser, welches zumal in Castell und Wiesenbronn eine bekannte Calamität ist [...]"
- Uffenheim (`bsb00143120` canvas 43): "beim weiblichen Geschlechte ist das Tragen schwerer Lasten auf dem Kopfe eine nicht seltene Ursache zur Entstehung des Kropfes und zu Lageveränderungen der Gebärmutter."
- Eltmann, section on Zeil (`bsb00140606` canvas 362): "Kröpfe [...] sind besonders bei dem weiblichen Geschlechte nicht selten, was von schweren Arbeiten, Geburten, Tragen schwerer Lasten etc herkommen mag."
- Weiler (`bsb00028867` canvas 24): "[...] während die dem lymphatischen Habitus hinneigenden Weiber häufig von Fetthälsen und Kröpfen entstellt sind. Von ausgebildetem Cretinismus ist mir übrigens kein Fall bekannt, wohl gibt es einzelne Familien, wo bereits sämtliche Kinder dem Cretinismus sich annähern."
- Schillingsfürst (`bsb00146478` canvas 44-45): "[...] indem hier der Cretinismus in allen seinen Variationen vorkömmt, und, wie schon gesagt, auf die Befreiung vom Militärdienste wegen Gebrechen Einfluß übt."

## Caveats

- **Dataset version.** `goiter_status` and `cretinism_status` are not in the published version `0.9.0-pre-paleographer-review` (DOI `10.5281/zenodo.24523214`), which has only the combined column `goiter_cretinism_status`. Publish the next dataset version before this post, so that the source link holds the data on the map. Part 8 links the concept DOI, which resolves to the newest version.
- **The map is thin.** Only 34 of 239 districts have a goiter statement in the image-verified pages (13 endemic or frequent, 20 rare or local, 1 absent: Nittenau). The verification pass looked for infant feeding first, so a hollow point means "not captured", not "no goiter". Say so in the post or the alt text. The old combined column marked 74 districts; 27 of them are hollow now because the recorded evidence does not settle either condition. They are queued for image checks (`DATACARD.md`, section 8).
- **Goiter only.** Cretinism is in its own column (5 endemic or frequent, 17 rare or local, 5 absent) and is not on the map. Wiesentheid and Schillingsfürst are quoted on cretinism. Wiesentheid is a hollow point because no goiter statement from its pages was verified; Schillingsfürst is red for goiter. Dingolfing (no cretins, nothing on goiter) and Herzogenaurach (almost no goiter among men, nothing on women) are hollow. Bayreuth Stadt (almost no goiter) is amber.
- **Uffenheim, resolved.** The table now records goiter as present (`sporadic_or_localized`, canvas 43) and cretinism as absent (`explicitly_absent`, canvas 21). Its point is amber. The physician calls heavy loads "a not uncommon cause" of goiter in women; he does not say that goiter is frequent.
- The list of theories on canvas 264 is the Wiesentheid physician's summary of another author, cited from an 1858 journal. The iodine sentence on canvas 265 is his own judgment.
- Weiler: "bereits" is the Swabian sense "nearly", so "nearly all the children".
- Thread part 6 is modern medical context, not in the reports.
