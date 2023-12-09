Minimum Score anhand der verschienden Karten zu den Kategorien:

- Trumpf
    - Rosen
    - Schilten
    - Eicheln
    - Schellen
- Obe abe
- Unde ufe

sonst schieben.

Beispiel: Für Trump braucht es minimal 35 Punkte in Karten die man besitzt. (45 Score von "Jassen auf Basis der Spieltheorie")

Für obe abe oder unde ufe mindestens 22 Punkte. (obeabe 25 score, uneufe 21 Score)

Features Trumpf:
- Anzahl Karten der Farben
- Anzahl hoher Karten der Farben (A-10)
- Anzahl tiefer Karten der Farben (6-9)
- hat Buur von Farben
- hat nell von Farben
- Forehand


Features Spielen:
Alles was wir zum Trainieren brauchen muss uns während dem Turnier bekannt sein.

Attribut|Gamestate|In Labels
------------|--------------|-----
eigene Hand | state.hands|True
wer sagt an | state.declared_trump|True
forehand| state.forehand|True
trump| state.trump|True
gespielte / nicht gespielte karten (hot encoded array)| state.hands|True
Anzahl Trumpfkarten auf Hand| 
Anzahl Trumpfkarten gespielt / nicht gespielt | 
Anzahl vergangener Spielzüge| state.nr_tricks|True
bereits gespielte Karten diese Runde| state.nr_cards_in_trick|True
buur / nell von Trumpf bereits gelegt|
erlaubte zu spielende Karten|