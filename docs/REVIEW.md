# Första formförslaget: damaged_01

2026-09-12. **Visuellt granskat formexperiment; inte utskriftsklart.**

Öppna [originalscenen](../scenes/baseline.blend) eller
[varianten](../scenes/damaged_01.blend) i Blender.

| Vy | Original | Variant |
|---|---|---|
| Utsida | [Bild](../renders/baseline/exterior.png) | [Bild](../renders/damaged_01/exterior.png) |
| Insida | [Bild](../renders/baseline/interior.png) | [Bild](../renders/damaged_01/interior.png) |
| Fasad | [Bild](../renders/baseline/facade.png) | [Bild](../renders/damaged_01/facade.png) |

## Vad som ändrats

Ett ojämnt brott skär genom högra fasadens övre fönster i utsidesvyn.
Bröstvärnet ovanför har också kapats så att det följer den borttagna väggen.
De exponerade golvkanterna har fått större urtag. Bottenvåningen och hörnpelaren
är bevarade. Inga original har förenklats.

Insidesvyn visar att den översta golvplattan nu skjuter ut från den kvarvarande
väggen. Golvurtagen är fortfarande ganska geometriska, och brottytorna har
enklare struktur än originalets skulpterade skador. Det är möjliga områden för
nästa estetiska iteration; inga nya rasmassor eller materialfärger har lagts till.

## Verifierat och kvarstående

- Alla sex före/efter-bilder har granskats. Samma kameror, ljus och bildstorlek.
- Samtliga original-STL har oförändrad SHA256.
- Bottenvåningen använder samma mesh som den bevarade källscenen.
- Skyddad region x<185: samma unika punkter efter avrundning till 0,0001 mm,
  1 371 834 punkter på firstFloor och 405 338 på secondFloor.
- Två STL-exporter har återimporterats: ändliga koordinater, rätt mått och
  minsta XYZ på 0. Förskjutningarna är registrerade i rapporten.
- **Nätkvaliteten är försämrad av skärningarna.** Återimporterad firstFloor har
  272 öppna kanter och 1 694 kanter med fler än två angränsande ytor;
  secondFloor har 172 respektive 1 647. Baslinjen hade 25/22 och 5/37.
  Exporterna är till för vidare bearbetning, inte färdiga utskriftsfiler.
- Självskärningar, lösa komponenter, minsta väggtjocklek, stödbehov och fysisk
  passning är inte fullständigt verifierade. Ingen provutskrift eller slicing gjord.

[Byggrapport](../reports/damaged_01.json) och
[oberoende återimportskontroll](../reports/damaged_01-verification.json).

För nästa instruktion räcker det att ange vy och område, exempelvis:
”På insidesbilden: gör det översta golvet mindre och brottkanten ojämnare.”
