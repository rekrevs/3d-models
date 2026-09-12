# Imperial Ruins – visuell modellverkstad

Vi utgår från tre befintliga STL-filer och gör variationer genom en återkommande
process: rendera → granska → ändra geometri → rendera samma vyer → kontrollera.
Användaren kan styra med text, referensbilder och markerade bilder. Blender är
arbetsmiljön; Bambu Studio används vid behov för granskning inför utskrift.

## Versionshantering

Privat GitHub-spegel: `rekrevs/3d-models`. Original, foton, skript,
arbetsmodeller, exporter, granskningsbilder och Wotan-loggar versionshanteras.
STL- och Blender-filer lagras med Git LFS. Installera Git LFS före kloning:

```sh
git lfs install
git clone git@github.com:rekrevs/3d-models.git
```

Utskriftsberedningen (T-0004) är tills vidare parkerad på användarens begäran.
Den nya varianten är fortfarande ett formförslag, inte utskriftsklar.

## Förutsättningar

- Original i `sources/stl/`: `groundFloor.stl`, `firstFloor.stl`, `secondFloor.stl`. Bevara dessa
  oförändrade; arbetsfiler och exporter läggs i egna kataloger.
- Källa: [Imperial Ruins](https://makerworld.com/en/models/2724302-imperial-ruins#profileId-3018397),
  Two goblins in a trench coat. Sidtext och tre fotografier tillhandahölls av
  användaren. Sidan anger publicering 2026-04-27 och Standard Digital File License.
  Fullständiga licensvillkor har inte granskats; publicering ingår inte i arbetet.
- Referensbilder i `sources/photos/`: `0b94653d0d731293.webp` (utsida),
  `57e02a57318e662e.webp` (insida), `c8f5c06c1c3bb0e7.webp` (fasad).
- Bilderna visar en gotisk byggnadshörna med spetsbågar, stödpelare, två
  exponerade golvplan, övre bröstvärn och avbrutna vägg-/golvkanter.
  Målningens färger finns inte i STL; granskning sker med neutralt material.
- Cirka 10,59 miljoner trianglar totalt. Förenkling får endast göras i separata
  arbetskopior och måste granskas för förlust av ornament och skarpa kanter.
- STL anger inte enhet. Vi antar millimeter för dessa terrängmodeller och
  registrerar antagandet. Inga exakta spelregelkrav eller miniatyrbasmått är satta.
- Källornas koordinater har cirka 13 enheters vertikalt mellanrum mellan delar.
  Stora anliggningsytor visar ett 15 mm mellanrum; 2 mm uppstickande detaljer
  förklarar skillnaden mot bounding box. Visuellt granskad montering använder
  Z-förskjutning 0/-15/-30 mm, vilket ger våningsnivåer 0/70/140 mm.
  Originalplacering bevaras i en egen scen.
- Lokal Blender: `/Applications/Blender.app/Contents/MacOS/Blender`, verifierad
  version 5.2.1 LTS. Bambu Studio finns också installerat.

## Arbetssätt och första omfattning

Arbetet organiseras i [Wotan](wotan/backlog.json), med besluts- och
verifieringslogg per uppgift i `wotan/dev-log/`.

Första leveransen är en granskbar originalscen och därefter en asymmetriskt
skadad övervåning: bevarad hörnpelare, brott genom en fönsterbåge och ett större
ras i golvkanten. Exakt skärning bestäms efter granskning av importerad geometri.
Detta är ett första formexperiment, inte en bekräftat utskriftsklar modell.

`sources/stl/` innehåller originalmodeller och `sources/photos/` referensfoton.
`scripts/` innehåller reproducerbara Blender-skript, `scenes/` arbetsmodeller,
`renders/` granskningsbilder, `reports/` mätningar och `exports/` nya STL-filer.
Kontrollera källornas hash, mått, delarnas placering och renderade vyer. För en
export kontrolleras även ändrad geometri och nätets öppna/icke-manifold kanter.

Blender styrs initialt via bakgrundsskript; detta är inte en anslutning som ser
användarens live-vy. Fasta kameror gör före/efter jämförbart. Sparade bilder kan
granskas av agenten och annoteras av användaren.

## Öppna och återskapa

Första varianten finns i `scenes/damaged_01.blend`.
[Granskning med före/efter-bilder och begränsningar](docs/REVIEW.md).
STL-filerna i `exports/damaged_01/` är formprototyper för vidare bearbetning;
skärningarna har ökat antalet nätfel och behöver lagas inför utskrift.

Öppna `scenes/baseline.blend` i Blender. Scenen `Assembled` visar monteringen;
scenen `Source coordinates` visar importerad originalplacering. Växla scen i
Blenders övre fält. Numpad 0 visar aktiv kamera; vanlig 3D-navigering fungerar.

Från projektkatalogen:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --threads 8 --python-exit-code 1 --python scripts/build_baseline.py
/Applications/Blender.app/Contents/MacOS/Blender --background --threads 8 --python-exit-code 1 --python scripts/inspect_baseline.py
/Applications/Blender.app/Contents/MacOS/Blender --background --threads 8 --python-exit-code 1 --python scripts/build_variant.py
/Applications/Blender.app/Contents/MacOS/Blender --background --threads 8 --python-exit-code 1 --python scripts/verify_variant.py
```

Skripten skriver om sina egna genererade resultat vid omkörning. De skriver aldrig
över STL-originalen. Blender kan behöva köras utanför agentsandboxen: här
kraschade dess Metal-initiering inne i sandboxen. Rendering använder Cycles CPU,
8 trådar och 24 samples; ett komplett originalbygge tar ungefär en halv minut.

Originalvyer: [utsida](renders/baseline/exterior.png),
[insida](renders/baseline/interior.png), [fasad](renders/baseline/facade.png).
Källinventering: [mått och SHA256](reports/source_inventory.json).
Nätkontroll: [baslinje](reports/baseline-mesh.json).

Importören tog bort 22 duplicerade och 106 degenererade trianglar i arbetskopiorna.
De importerade näten har dessutom ett mindre antal öppna kanter och kanter med
fler än två angränsande ytor. Originalscenen är en visuell baslinje, inte ett
intyg om vattentäta nät. Överlappningar, väggtjocklek och fysisk passning behöver
bedömas separat inför faktisk utskrift.
