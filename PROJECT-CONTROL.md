# Project control log

- Protocol: `project-control/v0.1`

## PCR-2026-09-12-001

- Record type: review
- Date: 2026-09-12
- Mode: checkpoint
- Trigger: Första tre Wotan-uppgifterna slutförda; exekveringskön är tom.
- Control judgement: evaluate
- Current gate: Användarens estetiska bedömning; dessutom krävs nätlagning om
  en variant ska gå vidare till utskrift.
- Recommendation: Bedöm det konkreta formförslaget i Blender eller från fasta
  vyer innan fler automatiska varianter eller generell infrastruktur byggs.
  Välj därefter en riktad visuell iteration eller nätlagning för en vald form.
- Owner decision required: Ingen för att avsluta det utförda arbetet. Nästa
  kreativ riktning och eventuell prioritering av utskrift är ännu inte valda.
- Evidence: `README.md`, `docs/REVIEW.md`, `wotan/dev-log/T-0002.md`,
  `wotan/dev-log/T-0003.md`, `reports/damaged_01-verification.json`.
- Uncertainty: Arbetssättet fungerar för lokal visuell iteration, men automatisk
  skärning av dessa täta nät ger fler topologifel. Fysisk utskrift ej verifierad.
- Resulting Wotan tasks: Ingen ny READY-uppgift. T-0004 bevarar nätlagning som IDEA.
- Portfolio signal: Projektet har fått en konkret första leverans att bedöma.
- Revisit when: Användaren ger visuella instruktioner, väljer en form för utskrift
  eller vill prova en annan kreativ riktning.

Detta är agentens rekommendation, inte ett nytt ägarbeslut.

## PCD-2026-09-12-001

- Record type: decision
- Date: 2026-09-12
- Decides review: PCR-2026-09-12-001
- Owner: Sverker
- Decision: Vänta med utskriftsberedningen; initiera Git och spegla hela projektet
  privat på GitHub i stället. Det korta önskemålet om printberedning ersattes
  innan några nätändringar eller reparationsprocesser hade påbörjats.
- Disposition: modified
- Resulting Wotan tasks: T-0006. T-0004 kvarstår som parkerad IDEA.
- Portfolio signal: Projektet bevaras och speglas; ingen aktiv utskriftsberedning.
- Revisit when: Användaren ber att återuppta modellering eller utskriftsberedning.
