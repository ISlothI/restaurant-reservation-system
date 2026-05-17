# AI használat dokumentáció

Ez a mappa a projekt fejlesztése során alkalmazott mesterséges intelligencia használatát dokumentálja.
Itt találhatók a felhasznált promptok, a kapcsolódó munkamenetek, valamint azok rövid értékelése abból a szempontból, hogy az AI mely fejlesztési fázisokban bizonyult hasznosnak, és mely pontokon volt szükség erősebb emberi döntéshozatalra.

## Kapcsolódó fájl

A `prompts/Refine Reservation System Features.md` fájl tartalmazza a projekt során használt részletes promptot és az ahhoz kapcsolódó feladatleírást.

## Az AI használatának célja

Az AI elsődleges szerepe a fejlesztési folyamat gyorsítása, a kezdeti tervezés támogatása, az implementáció felgyorsítása, valamint a hibák feltárásának és javításának segítése volt.

A cél nem az volt, hogy az AI önállóan tervezze és készítse el a teljes rendszert, hanem az, hogy fejlesztést támogató eszközként működjön: segítsen az ismétlődő vagy időigényes feladatokban, miközben a fontosabb szerkezeti és szakmai döntések továbbra is emberi kontroll alatt maradnak.

## A promptolás folyamata

A fejlesztés során az a tapasztalat alakult ki, hogy a legfontosabb lépés a jó minőségű kezdő prompt megírása. Ha az első prompt elegendő kontextust, pontos követelményeket és világos technikai korlátokat tartalmaz, akkor az AI már az első válaszokban is lényegesen jobb minőségű eredményt tud adni.

Ez különösen fontos akkor, ha nemcsak egy működő megoldás a cél, hanem egy olyan rendszer kialakítása is, amely szerkezetileg átlátható, bővíthető, valamint biztonsági és adatmodellezési szempontból is megfelelő.

## A kezdő prompt felépítése

A kiinduló prompt négy fő részre volt bontva Markdown címsorok segítségével.

### 1. Segédtudás
Ebben a részben a releváns tananyag és háttérinformációk tömörített, célzott kivonata szerepelt. A cél az volt, hogy az AI csak a feladathoz szükséges kontextust kapja meg, a felesleges információk nélkül.

### 2. Követelmények
Itt a konkrét feladathoz tartozó elvárások szerepeltek. A nem releváns vagy ismétlődő részek ki lettek hagyva, hogy a prompt fókuszált maradjon.

### 3. Technikai specifikációk
Ebben a szakaszban lettek rögzítve a megvalósítás technológiai keretei. Ezek közé tartozott például:

- a teljes rendszer Docker Compose segítségével indítható legyen,
- a backend Pythonra és FastAPI-ra épüljön,
- Pydantic modellek legyenek használva,
- a hitelesítés JWT-alapú legyen,
- a jelszavak bcrypttel legyenek hash-elve,
- az adatbázis MongoDB konténerben fusson,
- a frontend Angular alapú legyen router használattal.

### 4. Feladat
Ebben a részben a konkrét megvalósítandó funkció vagy fejlesztési feladat leírása szerepelt.

## Miben volt hasznos az AI

Az AI különösen hasznosnak bizonyult az alábbi területeken:

- a projekt kezdeti felépítésének gyors kialakításában,
- a backend és frontend alapfunkciók létrehozásában,
- kisebb implementációs feladatok automatizálásában,
- hibák feltárásában és javításában,
- iteratív finomhangolásban és refaktorálásban.

Külön előnyt jelentett, hogy egy-egy kisebb módosítás vagy hiba javítása célzott promptokkal gyorsan végrehajtható volt, így a fejlesztési ciklus lerövidült.

## Emberi kontroll és döntési pontok

Bár az AI több területen is hasznos támogatást adott, nem minden javaslata volt közvetlenül elfogadható. Különösen az adatmodell és az architektúra területén volt szükség emberi kontrollra.

Előfordult például, hogy az AI javaslatot tett az adatbázis sémájára, de a végső megoldás nem ezt követte, mert a saját tervezés jobban illeszkedett a kívánt működéshez és a rendszer logikájához.

Ez alapján az AI leginkább támogató eszközként bizonyult hasznosnak, nem pedig teljesen önálló tervezőként.

## Iteratív fejlesztés

Miután elkészült az alkalmazás első működő verziója, a további fejlesztés főként tesztelésből, hibakeresésből és kisebb módosításokból állt. A feltárt problémák alapján újabb, egyre célzottabb promptok készültek, amelyek már egy-egy konkrét funkcióra vagy hibára koncentráltak.

Ez a megközelítés hatékonynak bizonyult, mert a nagy kezdő prompt után a további feladatok már kisebb, jól körülhatárolható egységekre bonthatók voltak.

## Tapasztalatok és tanulságok

A projekt során szerzett legfontosabb tapasztalatok a következők voltak:

- a jól megírt kezdő prompt jelentősen javítja a későbbi eredmények minőségét,
- a pontos technikai korlátok csökkentik a félreértések esélyét,
- az AI jól használható implementációs támogatásra és hibajavításra,
- az architekturális és domain-specifikus döntéseket továbbra is embernek kell meghoznia,
- az iteratív, kis lépésekben történő finomítás eredményesebb, mint a túl általános utólagos korrekció.

A projekt során nem volt olyan prompt, amely ne eredményezte volna a várt eredményt.

## Összegzés

Az AI a projekt során akkor működött a leghatékonyabban, amikor világos kontextust, részletes követelményeket és egyértelmű technikai elvárásokat kapott. A fejlesztési folyamatban így nem önálló fejlesztőként, hanem jól használható szakmai segédeszközként vett részt.

Összességében az AI jelentősen hozzájárult a fejlesztési folyamat gyorsításához, de a projekt minőségét döntően az határozta meg, hogy a generált eredmények minden fontosabb ponton emberi ellenőrzésen és szakmai felülvizsgálaton mentek keresztül.